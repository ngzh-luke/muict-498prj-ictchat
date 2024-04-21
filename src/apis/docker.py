""" import config when build with docker """

""" 
main.py
Run file of the APIs server """
from typing import Union
from .model import generate_response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random


""" 
model.py
Chat model """
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import AutoPeftModelForCausalLM
from torch.cuda import is_available as isCudaAva
from huggingface_hub import login
from ..config import myToken
import joblib
