""" Chat model """
from transformers import AutoTokenizer, BitsAndBytesConfig
from peft import AutoPeftModelForCausalLM
from torch.cuda import is_available as isCudaAva
from huggingface_hub import login
from ..config import myToken
from decouple import config

if myToken == None:
    myToken = config('token') # reassure the huggingface token is exists

login(token=myToken)


def getDevice():
    
    device = isCudaAva()
    return 'cuda' if device == True else 'cpu'


def loadModel():
    """ create or load a model """
    quantization_config = BitsAndBytesConfig(load_in_4bit=True)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

      
    model = AutoPeftModelForCausalLM.from_pretrained("maunoi/Mistral-qlora-finetunined-MUICT-Chatbot", device_map="auto", quantization_config = quantization_config).to(getDevice())
        # unwraped_model = unwrap_model(model)
        # unwrap_model.save_pretrained('model/chatModel')
        
    return model, tokenizer


# MODEL, token = loadModel()



# adapted
def generate_response(query, history=[]):
    # Prepare conversation history with context markers
    context = ""
    for i, prev_utterance in enumerate(history):
        if i % 2 == 0:
            context += f"<s>[USER] {prev_utterance}\n"
        else:
            context += f"<s>[ASSISTANT] {prev_utterance}\n"

    prompt = f"{context}[Mahidol ICT] {query}"

    model_inputs = token(prompt, return_tensors="pt").to(MODEL.device)
    outputs = MODEL.generate(**model_inputs, temperature=0.1, top_k=1, top_p=1.0, repetition_penalty=1.4, min_new_tokens=16, max_new_tokens=400, do_sample=True)

    decoded_text = token.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]

    # Remove input text and query from generated response
    decoded_text = decoded_text.splitlines(True)
    decoded_text = ''.join(decoded_text[:])
    start_index = decoded_text.find("[Mahidol ICT]") + len("[Mahidol ICT]") + len(query) + 1
    decoded_text = decoded_text[start_index:].strip()

    # Remove the 'me' tag
    cleaned_text = decoded_text.replace('me', '').strip()

    return cleaned_text