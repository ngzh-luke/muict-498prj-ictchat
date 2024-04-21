""" 
Run file of the APIs server """
from typing import Union
from .model import generate_response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

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
def readUserPrompt(prompt: Union[str, None] = None):
    res = generate_response(prompt)
    return {'res': res}


@app.get('/test')
def test(prompt: Union[str, None] = None):
    response = random.choice(
        [
            f"Hello there! I think i can assist you with that. prompt: {prompt}",
            f"Hi, human! This is an easy piece. prompt: {prompt}",
            f"Sorry, can't help with that. prompt: {prompt}",
        ]
    )
    return {'res': response}
