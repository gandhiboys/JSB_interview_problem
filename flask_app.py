from flask import Flask, jsonify, request
import threading
import logging
import subprocess
import sys
from rag_mode import rag, rag_response
import speech_recognition as sr
from gtts import gTTS
import pygame
import re

app = Flask(__name__)

# List to store messages
messages = []
responses = []

user_query = ""
pdf_link = ""
# List to store rag messages and responses
rag_messages = []
rag_responses = []

stt = subprocess.Popen(["streamlit", "run" ,"streamlit_app.py"])

# Initialize pygame mixer
pygame.mixer.init()

def clean_response(response):
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    response = ansi_escape.sub('', response)
    # Remove spinner animations
    response = re.sub(r'⠙|⠹|⠸|⠼|⠴|⠦|⠧|⠇|⠏|⠋', '', response)
    return response.strip()

def input_thread():
    while True:
        text = input("Enter text to display on the web UI: ")
        if text == "RAG START":
            messages.append(text)
            pdf_link = input("Enter link to the pdf file: ")
            rag(pdf_link)
            while pdf_link:
                user_query = input("Enter your query: ")
                if user_query == "RAG STOP":
                    rag_messages.append(user_query)
                    break
                rag_messages.append(user_query)
                response = rag_response(user_query)
                rag_responses.append(response)
            messages.pop()
        elif text == "TALK":
            recognizer = sr.Recognizer()
        
            with sr.Microphone() as source:
                print("Say something:")
                audio = recognizer.listen(source)
            
            user_input = recognizer.recognize_google(audio)
            print("You said: " + user_input)
            cmd = ['ollama', 'run', 'llama3', user_input]
            llm_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, _ = llm_output.communicate()
            response = stdout.decode()
            print("LLM response: " + response)
            cleaned_response = clean_response(response)
            tts = gTTS(text=cleaned_response, lang='en')
            tts.save("temp.mp3")
            pygame.mixer.music.load("temp.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        
        else:
            messages.append(text)
            cmd = ['ollama', 'run', 'llama3', text]
            llm_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, _ = llm_output.communicate()
            response = stdout.decode()
            print("response: " + response)
            responses.append(response)
            
                
@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

@app.route('/get_responses', methods=['GET'])
def get_responses():
    return jsonify({"responses": responses})

@app.route('/get_rag_messages', methods=['GET'])
def get_RAG_messages():
    return jsonify({"rag_messages": rag_messages})

@app.route('/get_rag_responses', methods=['GET'])
def get_RAG_responses():
    return jsonify({"rag_responses": rag_responses})

try:
    if __name__ == '__main__':
        # Starting a thread for terminal input to not block the Flask app
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.WARNING)
        
        thread = threading.Thread(target=input_thread)
        thread.daemon = True
        thread.start()

        # Starting Flask app
        app.run(port=5002)

except KeyboardInterrupt:
    stt.terminate()
    sys.exit(0)