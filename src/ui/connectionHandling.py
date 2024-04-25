""" connection to server handling """
import requests
import time
import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import API_SERVER

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
        r  = requests.get(f'{API_SERVER}/test')
        # time.sleep(0.5)
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
        # st.toast(f"Unable to connect to chat server, please try again. Error: {e}")
        print(f'error connect to server: {e}')
        return False

def checkServerConnection():
    """ Returns `True` if server is active, `False` otherwise """
    try:
        r = requests.get(f'{API_SERVER}/')
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def _retry():
    """ Returns `True` if connected to server or `False` otherwise"""
    with st.spinner('Connecting to chat server...'):
        # time.sleep(1)
        connectToServer.clear() # clear server status cache
        connect = connectToServer()
        print("retry conn result",connect)
        if connect == True:
            print(f'Server: {API_SERVER} is ready!')
            st.toast('Server is ready!')
            st.balloons()
            return True
        else:
            print("Unable to connect to chat server, please try again.")
            st.toast("Unable to connect to chat server, please try again.")
            return False

