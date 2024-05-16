import streamlit as st
import requests
import signal 
import sys
import re
import time

# Dictionary to map messages to responses
mess_res_map = {}
# Dictionary to map RAG (Retrieval-Augmented Generation) messages to responses
mess_res_rag_map = {}

# Variables to track the current length of message-response dictionaries
curr_len_mess_res_map = 0
curr_len_rag_map = 0

# Handler for SIGTERM signal
def sigterm_handler(signum, frame):
    sys.exit(0)

# Function to fetch messages from the Flask server
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

# Function to fetch responses from the Flask server
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

# Function to fetch RAG messages from the Flask server
def fetch_rag_messages():
    try:
        response = requests.get('http://localhost:5002/get_rag_messages')
        if response.status_code == 200:
            return response.json()["rag_messages"]
        else:
            return []
    except Exception as e:
        st.error(f"Failed to fetch rag messages: {str(e)}")
        return []

# Function to fetch RAG responses from the Flask server
def fetch_rag_responses():
    try:
        response = requests.get('http://localhost:5002/get_rag_responses')
        if response.status_code == 200:
            return response.json()["rag_responses"]
        else:
            return []
    except Exception as e:
        st.error(f"Failed to fetch rag response: {str(e)}")
        return []

# Function to clean response text
def clean_response(response):
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    response = ansi_escape.sub('', response)
    # Remove spinner animations
    response = re.sub(r'⠙|⠹|⠸|⠼|⠴|⠦|⠧|⠇|⠏|⠋', '', response)
    return response.strip()

# Main function to display messages and responses in the Streamlit app
def main():
    st.title('Terminal Text Display(Red) and LLM Response(Black)')

    while True:
        # Fetch messages from the Flask server
        messages = fetch_messages()
        
        # Fetch responses from the Flask server
        responses = fetch_responses()

        # Check if RAG mode is activated
        if len(messages)>0 and messages[-1]=="RAG START":
            st.write(f"<span style='color:red'>{messages[-1]}</span>", unsafe_allow_html=True)
            while True:
                # Fetch RAG messages from the Flask server
                rag_messages = fetch_rag_messages()

                # Check if RAG mode is stopped
                if rag_messages and rag_messages[-1]=="RAG STOP":
                    st.write(f"<span style='color:red'>{rag_messages[-1]}</span>", unsafe_allow_html=True)
                    break

                # Fetch RAG responses from the Flask server
                rag_responses = fetch_rag_responses()

                # Check if new RAG message and response are received
                if len(rag_messages)>0 and len(rag_responses)>0 and len(rag_responses) == len(rag_messages) and len(rag_responses)>len(mess_res_rag_map.keys()):
                    global curr_len_rag_map
                    new_rag_msg = str(rag_messages[-1])
                    new_rag_res = str(rag_responses[-1])
                    mess_res_rag_map[new_rag_msg] = new_rag_res
                   
                    if len(mess_res_rag_map.keys())>curr_len_rag_map:                
                        st.write(f"<span style='color:red'>{new_rag_msg}</span>", unsafe_allow_html=True)
                        st.write(f"<span style='color:black'>{new_rag_res}</span>", unsafe_allow_html=True)
                        curr_len_rag_map += 1
        
                time.sleep(2)

        # Check if new message and response are received
        if len(messages)>0 and len(responses)>0 and len(responses) == len(messages) and len(responses)>len(mess_res_map.keys()):
            global curr_len_mess_res_map
            new_msg = str(messages[-1])
            new_res = clean_response(responses[-1])
            mess_res_map[new_msg] = new_res
 
            if len(mess_res_map.keys())>curr_len_mess_res_map:
                
                st.write(f"<span style='color:red'>{new_msg}</span>", unsafe_allow_html=True)
                st.write(f"<span style='color:black'>{new_res}</span>", unsafe_allow_html=True)
                curr_len_mess_res_map += 1
        
        time.sleep(2)

if __name__ == "__main__":
    main()
