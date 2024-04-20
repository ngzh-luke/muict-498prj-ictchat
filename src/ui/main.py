""" Starting point of the UI """
import streamlit as st
import random
import time
import requests


def logger(who, msg, verb='says'):
    print(f"{who} {verb} '{msg}'")


def sendInput(prompt):  # sent a user input to API server
    logger(f"prompt '{prompt}'", verb='has been sent', msg='to our server')
    pass


def responseGen():  # Streamed response emulator
    # need to request the response here
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    logger('MUICT Chatbot', response, verb='responds')
    for word in response.split():
        yield word + " "

        time.sleep(0.05)


st.title("MUICT Chatbot")
st.caption("By Group 4")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
# `Chat with MUICT Chatbot` is a placeholder
if prompt := st.chat_input("Chat with MUICT Chatbot"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
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
