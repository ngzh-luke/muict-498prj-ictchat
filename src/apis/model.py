""" Chat model """
from transformers import AutoTokenizer, BitsAndBytesConfig
from peft import AutoPeftModelForCausalLM
from torch.cuda import is_available as isCudaAva
from huggingface_hub import login
from ..config import myToken
from decouple import config
import re

if myToken == None:
    myToken = config('TOKEN')  # reassure the huggingface token is exists

login(token=myToken)


def getDevice():
    """ get activation device """
    device = isCudaAva()
    return 'cuda' if device == True else 'cpu'


def loadModelLlama():
    """ load a Llama2 fine tuned model """
    quantization_config = BitsAndBytesConfig(load_in_4bit=True)
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    model = AutoPeftModelForCausalLM.from_pretrained(
        "maunoi/llama2-qlora-finetunined-MUICT-Chatbot", device_map="auto", quantization_config=quantization_config).to(getDevice())
    return model, tokenizer


def loadModelMistral():
    """ load a Mistral fine tuned model """
    quantization_config = BitsAndBytesConfig(load_in_4bit=True)
    tokenizer = AutoTokenizer.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.2")
    model = AutoPeftModelForCausalLM.from_pretrained(
        "maunoi/Mistral-qlora-finetunined-MUICT-Chatbot", device_map="auto", quantization_config=quantization_config).to(getDevice())
    return model, tokenizer


L_MODEL, L_TOKEN = loadModelLlama()
M_MODEL, M_TOKEN = loadModelMistral()


def generate_response_llama2(query, history=[]):
    """ generates response using Llama2 fine tuned model """
    system_prompt = """
    <<SYS>>
    Welcome to your Mahidol University Information and Communication Technology (MUICT) program assistant!

    I can help you with:

    * **Finding information:** Ask me anything related to the Mahidol ICT program, including curriculum, faculty, admissions, credit requirements, and more.
    * **Course access:** Need help finding your courses? I can't directly access them myself, but I can guide you to the official platform for accessing your courses on the Mahidol ICT program website.

    **Accuracy Notice:**

    * If your question is unclear or I can't find the information, I'tll let you know and suggest official Mahidol ICT program resources for further assistance.
    * I aim to provide accurate and up-to-date information, but always refer to the official Mahidol ICT program website for the latest details.

    </SYS>>
    """
    # Prepare conversation history with context markers (only 4 newest conversation)
    # Note that the history is broken at the moment
    context = "\n".join(
        [f"<s>[USER] {prev_utterance}" for prev_utterance in history[-4:]])

    # Combine system prompt, context(history), and user query
    prompt = f"{system_prompt}\n{context}\n [Mahidol Information and Communication Technology Program] At Mahidol ICT program {query}"

    model_inputs = L_TOKEN(prompt, return_tensors="pt").to(L_MODEL.device)

    decoded_text = ''

    outputs = L_MODEL.generate(
        input_ids=model_inputs["input_ids"].to(L_MODEL.device), max_new_tokens=800)
    decoded_text = L_TOKEN.batch_decode(
        outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]

    # Remove input text from generated response by cutting the line
    decoded_text_lines = decoded_text.splitlines(True)
    decoded_text = ''.join(decoded_text_lines[20:])

    # Filter <> thing on first line
    decoded_text = re.sub(r'<.\*?>', '', decoded_text, count=1)

    return decoded_text


def generate_response_mistral(query, history=[]):
    """ generates response using Mistral fine tuned model """
    system_prompt = """
    <<SYS>>
    Welcome to your Mahidol University Information and Communication Technology (MUICT) program assistant!

    I can help you with:

    * **Finding information:** Ask me anything related to the Mahidol ICT program, including curriculum, faculty, admissions, credit requirements, and more.
    * **Course access:** Need help finding your courses? I can't directly access them myself, but I can guide you to the official platform for accessing your courses on the Mahidol ICT program website.

    **Accuracy Notice:**

    * If your question is unclear or I can't find the information, I'tll let you know and suggest official Mahidol ICT program resources for further assistance.
    * I aim to provide accurate and up-to-date information, but always refer to the official Mahidol ICT program website for the latest details.

    </SYS>>
    """
    # Prepare conversation history with context markers (only 4 newest conversation)
    # Note that the history is broken at the moment
    context = "\n".join(
        [f"<s>[USER] {prev_utterance}" for prev_utterance in history[-4:]])

    # Combine system prompt, context(history), and user query
    prompt = f"{system_prompt}\n{context}\n [Mahidol Information and Communication Technology Program] At Mahidol ICT program {query}"

    model_inputs = M_TOKEN(prompt, return_tensors="pt").to(M_MODEL.device)

    decoded_text = ''

    outputs = M_MODEL.generate(**model_inputs, temperature=0.05, top_k=1, top_p=1,
                               repetition_penalty=1.1, min_new_tokens=16, max_new_tokens=800, do_sample=True)
    decoded_text = M_TOKEN.batch_decode(
        outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]

    # Remove input text from generated response by cutting the line
    decoded_text_lines = decoded_text.splitlines(True)
    decoded_text = ''.join(decoded_text_lines[20:])

    # Filter <> thing on first line
    decoded_text = re.sub(r'<.\*?>', '', decoded_text, count=1)

    return decoded_text
