""" 
Run file of the APIs server """
from typing import Union
from .model import generate_response_llama2, generate_response_mistral
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import ast

app = FastAPI(title='MUICT Chatbot', description='ML project for ITCS498 at MUICT semester 2/2023 by group 4:\n- 6488011 Tawan Chaidee\
\n- 6488004 Kittipich Aiumbhornsin\
\n- 6488168 Linfeng Zhang\
', version='2')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
def read_root():
    return {"Hello": "From MUICT CHAT"}


@app.get('/chat')
def readUserPrompt(model: Union[str, None] = 'M', prompt: Union[str, None] = None, hist: Union[str, None] = "[]"):
    history = ast.literal_eval(hist)
    if model == 'L':
        # if selected Llama2
        res = generate_response_llama2(prompt, history)
    else:
        # default model is Mistral
        res = generate_response_mistral(prompt, history)
    return {'res': res}


@app.get('/test')
def test(model: Union[str, None] = 'M', prompt: Union[str, None] = None, hist: Union[str, None] = "[]"):
    history = ast.literal_eval(hist)
    if model == 'L':
        # if selected Llama2
        response = random.choice(
            [
                f"[L] Hello there! I think i can assist you with that. prompt: {prompt}",
                f"[L] Hi, human! This is an easy piece. prompt: {prompt}",
                f"[L] Sorry, can't help with that. prompt: {prompt}",
            ]
        )
    else:
        # default model is Mistral
        response = random.choice(
            [
                f"[M] Hello there! I think i can assist you with that. prompt: {prompt}",
                f"[M] Hi, human! This is an easy piece. prompt: {prompt}",
                f"[M] Sorry, can't help with that. prompt: {prompt}",
            ]
        )
    print(prompt, type(ast.literal_eval(hist)), ast.literal_eval(hist))
    return {'res': response, 'hist': history}
