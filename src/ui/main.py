""" Starting point of the UI """
import streamlit as st
import time
import requests
import json

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import ENDPOINT, API_SERVER


def logger(who, msg, verb='says'):
    """ log things out on the console """
    print(f"{who} {verb} '{msg}'")


def title():
    """ show chat title ui """
    TITLE = 'MUICT Chatbot'
    st.set_page_config(page_title=TITLE)
    st.title(TITLE)
    st.caption("By Group 4")
    logger(who='app title', verb='has been', msg='shown')


def sendInput(prompt):  # sent a user input to API server
    """ send user prompt to server """
    global r
    r = requests.get(f'{API_SERVER}/{ENDPOINT}?prompt={prompt}')
    if len(st.session_state.prompt) >= 1:
        r = requests.get(f'{API_SERVER}/{ENDPOINT}?prompt={prompt}&hist={st.session_state.prompt}')
    logger(f"prompt '{prompt}'", verb='has been sent', msg=f'to our server ({API_SERVER}/{ENDPOINT})')


def responseGen():  # Streamed response emulator
    """ Returns response from server """
    # response here
    r.encoding = 'utf-8'
    response = json.loads(r.text)
    response = response['res']
    logger('MUICT Chatbot', response, verb='responds')
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

@st.cache_data(show_spinner='Getting things prepared.')
def welcome():
    """ show welcome msg, 1 time msg """
    # display welcome msg
    welcome = st.chat_message('assistant')
    welcome.write('Hello, what would you like to know about MUICT?')
    welcome.caption('Please feel free to talk to me via chat box below.')
    return True


def main():
    """ chat point """
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # custom user input hist
    if 'prompt' not in st.session_state:
        st.session_state.prompt = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    # `Chat with MUICT Chatbot` is a placeholder
    if prompt := st.chat_input("Chat with MUICT Chatbot"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.prompt.append(prompt)
        # Display user message in chat message container
        with st.chat_message("user"):

            logger('user', prompt)
            sendInput(prompt)
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(responseGen())
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        # print(st.session_state.prompt)
        


# def checkServerConnection():
#     """ Returns `True, Response` if server is active, `False, Response` otherwise """
#     try:
#         r = requests.get(f'https://{API_SERVER}/')
#         if r.status_code == 200:
#             return True, r
#         else:
#             return False, r
#     except:
#         return False, r

@st.cache_data(show_spinner='Connecting to chat server...')
def connectToServer():
    """ connect to server 
    Returns `True` if connected, `False` otherwise
    
    """
    TXT = 'Connecting to chat server...'
    # st.toast(TXT)
    try:
        # with st.spinner(TXT):
            # status, r = checkServerConnection()
        r  = requests.get(f'{API_SERVER}/')
        time.sleep(0.5)
        print("connect to", API_SERVER, "with status code:",r.status_code)
        if r.status_code == 200:
            print(f'Server: {API_SERVER} is ready!')
            # st.toast('Server is ready!')
            # st.balloons()
            # st.success('Server is ready!', icon="✅")
            # st.empty()
            return True
        else:
            print("Unable to connect to chat server, please try again.")
            # st.toast("Unable to connect to chat server, please try again.")
            # st.error('Unable to connect to chat server.', icon="🚨")
            return False
    except Exception as e:
        st.toast(f"Unable to connect to chat server, please try again. Error: {e}")
        print(f'error connect to server: {e}')
        return False


def block():
    pass

# @st.cache_data()
def retry():
    """ Returns `True` if connected to server or `False` otherwise"""
    with st.spinner('Connecting to chat server...'):
        time.sleep(1)
        if connectToServer() ==True:
            print(f'Server: {API_SERVER} is ready!')
            st.toast('Server is ready!')
            st.balloons()
            return True
        else:
            print("Unable to connect to chat server, please try again.")
            st.toast("Unable to connect to chat server, please try again.")
            return False

title()
connectSuccess = connectToServer() # attempt to auto connect first, if success, run main """
if connectSuccess != True:
    st.toast("Unable to connect to chat server, please try again.")
    isRetry = st.button('Retry connection', type='primary')
    if isRetry == True: # if first attempt failed, attempt to connect at user pace """
        connectSuccess =  retry()
elif connectSuccess == True:
    welcome()
    main() # run chat stream after chat server is active