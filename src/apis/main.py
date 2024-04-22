""" 
Run file of the APIs server """
from typing import Union
from .model import generate_response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import ast

app = FastAPI()

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
def readUserPrompt(prompt: Union[str, None] = None, hist: Union[str, None] = "[]"):
    history = ast.literal_eval(hist)
    res = generate_response(prompt, history)
    return {'res': res}


@app.get('/test')
def test(prompt: Union[str, None] = None, hist: Union[str, None] = "[]"):
    response = random.choice(
        [
            f"Hello there! I think i can assist you with that. prompt: {prompt}",
            f"Hi, human! This is an easy piece. prompt: {prompt}",
            f"Sorry, can't help with that. prompt: {prompt}",
        ]
    )
    print(prompt, type(ast.literal_eval(hist)), ast.literal_eval(hist))
    return {'res': response, 'hist': ast.literal_eval(hist)}
