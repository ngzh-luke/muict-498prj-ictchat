""" Global config across the project """
from dotenv import find_dotenv, get_key
from decouple import config

dotenv = config('env', False)
dotdevenv = find_dotenv(filename='.dev.env')
if dotenv == False:
    """ use .dev.env"""
    myToken = get_key(dotenv_path=dotdevenv, key_to_get='token')
    API_SERVER = get_key(dotenv_path=dotdevenv, key_to_get='API_SERVER')
    ENDPOINT = get_key(dotenv_path=dotdevenv, key_to_get='endpoint')
else:
    """ use .env """
    myToken = config('token')
    API_SERVER = config('API_SERVER')
    ENDPOINT = config('ENDPOINT')
