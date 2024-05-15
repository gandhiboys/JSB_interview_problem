import streamlit as st
import requests
import signal 
import sys
import re

def sigterm_handler(signum, frame):
    sys.exit(0)

#signal.signal(signal.SIGTERM, sigterm_handler)

def fetch_messages():
    try:
        response = requests.get('http://localhost:5002/get_messages')
        if response.status_code == 200:
            return response.json()["messages"]
        else:
            return []
    except Exception as e:
        st.error(f"Failed to fetch messages: {str(e)}")
        return []
    
def fetch_responses():
    try:
        response = requests.get('http://localhost:5002/get_responses')
        if response.status_code == 200:
            return response.json()["responses"]
        else:
            return []
    except Exception as e:
        st.error(f"Failed to fetch responses: {str(e)}")
        return []
    
def fetch_RAG_response():
    try:
        response = requests.get('http://localhost:5002/get_responses')
        if response.status_code == 200:
            return response.json()["responses"]
        else:
            return []
    except Exception as e:
        st.error(f"Failed to fetch responses: {str(e)}")
        return []

def display_messages(messages):
    for message in messages:
        st.write(f"<span style='color:red'>{message}</span>", unsafe_allow_html=True)

def display_responses(responses):
    for response in responses:
        st.write(response, unsafe_allow_html=True)

def clean_response(response):
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    response = ansi_escape.sub('', response)
    # Remove spinner animations
    response = re.sub(r'⠙|⠹|⠸|⠼|⠴|⠦|⠧|⠇|⠏|⠋', '', response)
    return response.strip()

def main():
    st.title('Terminal Text Display(Red) and LLM Response(Black)')

    # Mode selection
    mode = st.radio("Select Mode:", ("Llama3 Chat", "RAG Mode"))

    displayed_messages = []
    displayed_responses = []

    while True:
        messages = fetch_messages()
        new_messages = [msg for msg in messages if msg not in displayed_messages]
        
        if new_messages:
            display_messages(new_messages)
            displayed_messages.extend(new_messages)

        responses = fetch_responses()
        cleaned_responses = []
        for response in responses:
            response = clean_response(response)
            cleaned_responses.append(response)

        new_responses = [res for res in cleaned_responses if res not in displayed_responses]
        
        if new_responses:
            display_responses(new_responses)
            displayed_responses.extend(new_responses)
        
        st.rerun()
    
if __name__ == "__main__":
    main()