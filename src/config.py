""" Global config across the project """
from dotenv import find_dotenv, get_key


dotenv = find_dotenv()
dotdevenv = find_dotenv(filename='.dev.env')
if dotenv == '':
    """ use .dev.env"""
    myToken = get_key(dotenv_path=dotdevenv, key_to_get='token')
    API_SERVER = get_key(dotenv_path=dotdevenv, key_to_get='API_SERVER')
    ENDPOINT = get_key(dotenv_path=dotdevenv, key_to_get='endpoint')
else:
    """ use .env """
    myToken = get_key(dotenv_path=dotenv, key_to_get='token')
    API_SERVER = get_key(dotenv_path=dotenv, key_to_get='API_SERVER')
    ENDPOINT = get_key(dotenv_path=dotenv, key_to_get='endpoint')
