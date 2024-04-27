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

M = "Mistral fine-tuned"
L = "Llama2 fine-tuned"

def logger(who, msg, verb='says'):
    """ log things out on the console """
    print(f"{who} {verb} '{msg}'")


def title():
    """ show chat title ui """
    TITLE = 'MUICT Chatbot'
    st.set_page_config(page_title=TITLE)
    st.title(TITLE)
    st.caption('ML project for ITCS498 at MUICT semester 2/2023 by group 4:\n- 6488011 Tawan Chaidee\
\n- 6488004 Kittipich Aiumbhornsin\
\n- 6488168 Linfeng Zhang\
')


def sendInput(prompt):  # sent a user input to API server
    """ send user prompt to server """
    global r

    if selectedModel == L:
        print(f'using {L}')
        r = requests.get(f'{API_SERVER}/{ENDPOINT}?model=L&prompt={prompt}')
    else:
        print(f'using {M}')
        r = requests.get(f'{API_SERVER}/{ENDPOINT}?model=M&prompt={prompt}')
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
        global selectedModel
        with st.sidebar:
            st.header("Model Selection")
            modelOptions = (M, L)
            selectedModel = st.selectbox(
            label="Choose your preferred Model:",
            options=modelOptions,
        )

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        # Accept user input
        if prompt := st.chat_input("Chat with MUICT Chatbot"):
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
 
                with st.spinner("Asking our intelligent assistant..."):
                    logger('user', prompt)
                    sendInput(prompt)
                    st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.write_stream(responseGen())

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

            

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
    