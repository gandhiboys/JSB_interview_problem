# LLM-RAG-WebUI Integration

This repository contains a Python-based software system that facilitates communication with Large Language Models (LLMs), focusing on both direct interaction and Retrieval-Augmented Generation (RAG) modes. Below is an overview of the project and its functionalities.

## Requirements
- Python 3.11.8
- CPU (GPU optional)
- Operating System Terminal (e.g., PowerShell, Bash)
- [ollama](https://github.com/langchain/ollama)
- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/)
- Other requirements can be found in requirements.txt file

## Overview
The software system consists of two primary modes:
1. **Back-and-Forth Communication:** Users can interact with the LLM by providing queries via the terminal. The LLM responds accordingly, maintaining context throughout the conversation.
2. **RAG Mode:** Users can input articles via links or PDFs, and subsequently query the LLM for information from these sources.

### Features
- Seamless mode switching without restarting the software.
- Web UI displaying user queries and LLM responses in different colors.
- Integration with ollama for LLM interaction.
- Basic Audio input support for user queries (extra credit).
- Basic Text-to-speech for LLM responses (extra credit).
- Use of a large LLM like llama3 with 8 billion parameters (extra credit).

## Usage
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the Flask server: `python flask_app.py`.
4. Access the Streamlit web interface in your browser.

### Mode Switching
- **Back-and-Forth Communication:** Input queries via the terminal.
- **RAG Mode:** Enter "RAG START" in the terminal, provide the PDF link, ask queries, and end with "RAG STOP".

## Extra Credit
- **Voice Interaction:** Speak queries instead of typing.
- **Text-to-Speech:** LLM responses are converted to speech.
- **Advanced LLM Models:** Utilize larger LLMs like llama3 70B.

## Video Demo
A video demonstration showcasing the functionality of the software and its various features has been provided. In the demo, the software is run from the terminal as per the requirements. The video covers mode switching, back-and-forth communication with the LLM, activation of RAG mode, interaction via audio input (extra credit), and text-to-speech output (extra credit).

You can watch the video demo here - https://drive.google.com/drive/folders/1h7xG_FeUPo5A1Um2U5ReD_ULPmRvuXWK?usp=sharing

For any further clarification or questions, please feel free to reach out.

## Contact
my email address - [mgandhi4512@sdsu.edu](mailto:mgandhi4512@sdsu.edu).
