""" Global config across the project """
from dotenv import find_dotenv, get_key
from decouple import config


dotdevenv = find_dotenv(filename='.dev.env')
if dotdevenv != '':
    """ use .dev.env"""
    print('load from .dev.env')
    myToken = get_key(dotenv_path=dotdevenv, key_to_get='token')
    API_SERVER = get_key(dotenv_path=dotdevenv, key_to_get='API_SERVER')
    ENDPOINT = get_key(dotenv_path=dotdevenv, key_to_get='endpoint')
else:
    """ use .env """
    print('load from .env')
    myToken = config('token')
    API_SERVER = config('API_SERVER')
    ENDPOINT = config('ENDPOINT')
