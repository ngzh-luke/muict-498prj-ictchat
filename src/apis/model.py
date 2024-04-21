""" Chat model """
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import AutoPeftModelForCausalLM
from torch.cuda import is_available as isCudaAva
from huggingface_hub import login
from ..config import myToken
import joblib


login(token=myToken)


def getDevice():
    device = isCudaAva()
    return 'cuda' if device == True else 'cpu'


def loadModel():
    """ create or load a model """
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2")
        model = joblib.load('chatModel.pkl')
        return model, tokenizer
    except FileNotFoundError:
        # quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2")

        # model = AutoModel.from_pretrained(
        #     "maunoi/Mistral-qlora-finetunined-MUICT-Chatbot").to(getDevice())
        # model = AutoPeftModelForCausalLM.from_pretrained(
        #     "maunoi/Mistral-qlora-finetunined-MUICT-Chatbot", offload_folder="offload_dir", adapter_name="adapter_config", device_map="auto",offload_state_dict=True).to(getDevice())
        model = AutoPeftModelForCausalLM.from_pretrained(
    "maunoi/Mistral-qlora-finetunined-MUICT-Chatbot", adapter_name="adapter_config").to(getDevice())
        joblib.dump(model, 'chatModel.pkl')
        return model, tokenizer


def generate_response(query, history=[]):
    # system_prompt = """
    # <s>[INST] <<SYS>>
    # **I am an assistant focused on Mahidol University's Information and Communication Technology (MUICT) program.**

    # **Goal:** Provide accurate and unbiased information of Mahidol University ICT program (MUICT).

    # **Safety:**
    # - Avoid harmful, unethical content and ensure positive, respectful responses.

    # **Accuracy:**
    # - If a question is unclear or information is unavailable about MUICT, clarify or suggest official MUICT resources.
    # - Ensure all information is factually correct, especially regarding MUICT.
    # </SYS>>
    # [/INST]
    # """

    # tokenizer_path = "mistralai/Mistral-7B-Instruct-v0.2"
    # model = AutoPeftModelForCausalLM.from_pretrained(
    #     "maunoi/Mistral-qlora-finetunined-MUICT-Chatbot",
    #       device_map="auto", quantization_config=quantization_config).to(getDevice())
    # tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    # Load model directly
    model, tokenizer = loadModel()

    system_prompt = """
<s>[INST] <<SYS>>
**I am your personal guide to Mahidol University's Information and Communication Technology (MUICT) program.**

**My expertise lies specifically with MUICT.** I can answer your questions about the program's faculty, curriculum, admissions process, career opportunities for graduates, and more!

Here's how I can help you:

*  **Faculty:** Want to know about MUICT professors' research areas or teaching styles? I can provide details on faculty profiles and expertise.
*  **Curriculum:** Curious about the courses offered, specializations available, or project requirements? I can give you an overview of the MUICT program structure.
*  **Admissions:** Wondering about eligibility criteria, application procedures, or scholarship opportunities? I can guide you towards official MUICT resources for admissions.
*  **Careers:** Unsure about job prospects after graduating from MUICT? I can share information on typical career paths for MUICT alumni.

If your question goes beyond MUICT's specific program, I'll let you know and suggest alternative resources from Mahidol University.

**Remember, I'm still under development, but I'm constantly learning.** I'll strive to provide you with accurate and up-to-date information directly related to MUICT.

**What would you like to know about MUICT today?**
[/INST]
</SYS>>
    """

    # Prepare conversation history with context markers (only 4 newest conversation)
    context = "\n".join(
        [f"<s>[USER] {prev_utterance}" for prev_utterance in history[-4:]])

    # Combine system prompt, context(history), and user query
    prompt = f"{system_prompt}\n{context}\n  [Mahidol ICT] {query}"

    model_inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    decoded_text = ''

    outputs = model.generate(**model_inputs, temperature=0.1, top_k=1, top_p=1.0,
                             repetition_penalty=1.4, min_new_tokens=16, max_new_tokens=400, do_sample=True)
    decoded_text = tokenizer.batch_decode(
        outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]

    # Remove input text from generated response
    decoded_text = decoded_text.splitlines(True)
    decoded_text = ''.join(decoded_text[15:])

    return decoded_text
