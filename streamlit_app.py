import requests
import streamlit as st
import re

def clean_response(response):
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    response = ansi_escape.sub('', response)
    # Remove spinner animations
    response = re.sub(r'⠙|⠹|⠸|⠼|⠴|⠦|⠧|⠇|⠏|⠋', '', response)
    return response.strip()

def get_llama_response(query):
    data = {'query': query}
    try:
        response = requests.post('http://localhost:5001/query', json=data)
        response.raise_for_status()  # Raise an error for 4xx or 5xx status codes
        response_data = response.json()
        if 'response' in response_data:
            return response_data['response']
        else:
            return "Invalid response format"
    except requests.RequestException as e:
        return f"Request failed: {e}"
    except ValueError as e:
        return f"Failed to parse JSON: {e}"

st.title("Llama3 Chat")

# Initialize conversation history
conversation_history = []

user_input = st.text_input("Enter your query:", key=f"user_input")

if st.button("Submit"):
    if user_input == "":
        st.warning("Please enter a query.")
    else:
        llama_response = get_llama_response(user_input)
        cleaned_response = clean_response(llama_response)
        
        # Append the conversation to history
        conversation_history.append({'user_query': user_input, 'llama_response': cleaned_response})
        
        # Display conversation history
        for chat in conversation_history:
            st.write(f"<span style='color:red'>{chat['user_query']}</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:black'>{chat['llama_response']}</span>", unsafe_allow_html=True)
