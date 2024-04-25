""" Starting point of the UI """
import streamlit as st
import time
import requests
import json
import os
import sys
from connectionHandling import connectToServer, _retry, checkServerConnection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import ENDPOINT, API_SERVER

# Initialize connection state
if "connection" not in st.session_state:
    st.session_state.connection = False

def logger(who, msg, verb='says'):
    """ log things out on the console """
    print(f"{who} {verb} '{msg}'")


def title():
    """ show chat title ui """
    TITLE = 'MUICT Chatbot'
    st.set_page_config(page_title=TITLE)
    st.title(TITLE)
    st.caption("By Group 4")
    # logger(who='app title', verb='has been', msg='shown')


def sendInput(prompt):  # sent a user input to API server
    """ send user prompt to server """
    global r
    # if len(st.session_state.hist) >= 1:
    #     r = requests.get(f'{API_SERVER}/{ENDPOINT}?prompt={prompt}&hist={st.session_state.hist}')
    # else:
    r = requests.get(f'{API_SERVER}/{ENDPOINT}?prompt={prompt}')
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
    welcomeTxt = 'Hello, what would you like to know about MUICT?'
    welcome.markdown(welcomeTxt)
    welcome.caption('Please feel free to talk to me via chat box below.')
    return welcomeTxt



def main():
    """ chat point """
    if checkServerConnection() == False:
        st.session_state.connection = False
        connectToServerOp()
    else:

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # # custom conver hist
        # if 'hist' not in st.session_state:
        #     st.session_state.hist = []
        #     st.session_state.hist.append(welcome())

        # initialize chatbox state
        if 'disabled' not in st.session_state:
            st.session_state.disabled = False
        

        # initialize chatbox placeholder
        if 'placeholder' not in st.session_state:
            st.session_state.placeholder = 'Chat with MUICT Chatbot'
        

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if st.session_state.disabled :
            st.caption("true")


        while st.session_state.disabled == False:

            # Accept user input
            if prompt := st.chat_input(st.session_state.placeholder, disabled=st.session_state.disabled):
            
                st.session_state.disabled = True
                st.session_state.placeholder = 'Our interlligent assistant is thinking...'
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                # st.session_state.hist.append(prompt)
                # Display user message in chat message container
                with st.chat_message("user"):
                    # st.session_state.disabled = False
                    # st.session_state.placeholder = 'Chat with MUICT Chatbot'
                    with st.spinner("Asking our intelligent assistant..."):
                        logger('user', prompt)
                        sendInput(prompt)
                        st.markdown(prompt)

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.write_stream(responseGen())
                        # time.sleep(0.1)

                # Add assistant response to chat history
                st.session_state.messages.append(
                {"role": "assistant", "content": response})
                # st.session_state.hist.append(response)
                # print("hist", st.session_state.hist)
            

def connectToServerOp():
    connectToServer.clear() # clear server status cache
    connectSuccess = connectToServer() 
    if connectSuccess != True:
        st.toast("Unable to connect to chat server, please try again.")
        isRetry = st.button('Retry connection', type='primary')
        if isRetry == True: 
            connectSuccess =  _retry()
    elif connectSuccess == True:
        st.session_state.connection = True
        welcome()
        main()


title()
connectToServer.clear()
if st.session_state.connection == False:
    connectToServerOp()
elif st.session_state.connection == True:
    # welcome()
    main()
    