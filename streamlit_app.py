import streamlit as st
import requests
import signal 
import sys
import re
import time

# user_messages = []
# llm_responses = []

mess_res_map = {}
mess_res_rag_map = {}

# new_msg = ""
curr_len_mess_res_map = 0
curr_len_rag_map = 0

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

# def display_new_message_response():
#     # for message in mess_res_map:
#     #     if message == new_msg:

#         st.write(f"<span style='color:red'>{message}</span>", unsafe_allow_html=True)
#         # if mess_res_map[message] is not None:
#         st.write(f"<span style='color:black'>{mess_res_map[message]}</span>", unsafe_allow_html=True)
        # try: 
        #     if llm_responses[index] is not None:
        #         st.write(f"<span style='color:black'>{llm_responses[index]}</span>", unsafe_allow_html=True)
        # except Exception as e:
        #     pass
        # if index == len(responses)-1:
        #     st.write(f"<span style='color:black'>{responses[index]}</span>", unsafe_allow_html=True)
    # for message in messages:
    #     st.write(f"<span style='color:red'>{message}</span>", unsafe_allow_html=True)

# def display_responses(responses):
#     for response in responses:
#         st.write(f"<span style='color:blue'>{response}</span>", unsafe_allow_html=True)

def clean_response(response):
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    response = ansi_escape.sub('', response)
    # Remove spinner animations
    response = re.sub(r'⠙|⠹|⠸|⠼|⠴|⠦|⠧|⠇|⠏|⠋', '', response)
    return response.strip()

def main():
    st.title('Terminal Text Display(Red) and LLM Response(Black)')

    # displayed_messages = []
    # displayed_responses = []

    while True:
        messages = fetch_messages()
        # new_messages = [msg for msg in messages if msg not in displayed_messages]
        # if messages:
        #     user_messages.append(messages[-1])
        # if messages:
        #     mess_res_map.update({str(messages[-1]): None})
        #     new_msg = messages[-1]

        responses = fetch_responses()

        if len(messages)>0 and messages[-1]=="RAG START":
            st.write(f"<span style='color:red'>{messages[-1]}</span>", unsafe_allow_html=True)
            while True:
                rag_messages = fetch_rag_messages()

                if rag_messages and rag_messages[-1]=="RAG STOP":
                    # print('break')
                    st.write(f"<span style='color:red'>{rag_messages[-1]}</span>", unsafe_allow_html=True)
                    break

                rag_responses = fetch_rag_responses()

                if len(rag_messages)>0 and len(rag_responses)>0 and len(rag_responses) == len(rag_messages) and len(rag_responses)>len(mess_res_rag_map.keys()):
                    # print('inside rag if ')
                    # print(new_rag_msg)
                    # print(new_rag_res)
                    global curr_len_rag_map
                    new_rag_msg = str(rag_messages[-1])
                    new_rag_res = str(rag_responses[-1])
                    mess_res_rag_map[new_rag_msg] = new_rag_res
                    # print("new message: ", new_msg)
                    # print("new res: ", new_res)
                    if len(mess_res_rag_map.keys())>curr_len_rag_map:
                    # display_new_message_response()
                
                        st.write(f"<span style='color:red'>{new_rag_msg}</span>", unsafe_allow_html=True)
                        st.write(f"<span style='color:black'>{new_rag_res}</span>", unsafe_allow_html=True)
                        curr_len_rag_map += 1
        

                time.sleep(2)

        # print('inside main if')    
        


        
        # new_responses = [res for res in responses if res not in displayed_responses]
        # if responses:
        # #     llm_responses.append(responses[-1])
        #     mess_res_map.update({new_msg: str(responses[-1])})

        # if len(messages)>0 and messages[-1]=="bye":
        #     while len(responses)!=len(messages):
        #         responses = fetch_responses()
        #         time.sleep(2)
        #     st.write(f"<span style='color:red'>{messages[-1]}</span>", unsafe_allow_html=True)
        #     st.write(f"<span style='color:black'>{clean_response(responses[-1])}</span>", unsafe_allow_html=True)
        #     quit()

        # cleaned_responses = []
        if len(messages)>0 and len(responses)>0 and len(responses) == len(messages) and len(responses)>len(mess_res_map.keys()):
            global curr_len_mess_res_map
            new_msg = str(messages[-1])
            new_res = clean_response(responses[-1])
            mess_res_map[new_msg] = new_res
            # print("new message: ", new_msg)
            # print("new res: ", new_res)
            if len(mess_res_map.keys())>curr_len_mess_res_map:
                # display_new_message_response()
                
                st.write(f"<span style='color:red'>{new_msg}</span>", unsafe_allow_html=True)
                st.write(f"<span style='color:black'>{new_res}</span>", unsafe_allow_html=True)
                curr_len_mess_res_map += 1
        
        time.sleep(2)
        # if responses:
        #     for response in llm_responses:
        #         # print(responses)
        #         response = clean_response(response)
        #         # cleaned_responses.append(response)
        #         mess_res_map.update({new_msg: str(response)})

        # try:
        #     if mess_res_map[new_msg] is not None:
        #         display_new_message_response(new_msg)
        # except Exception as e:
        #     pass

        # if new_messages:
        #     display_messages(new_messages)
        #     displayed_messages.extend(new_messages)

        # responses = fetch_rag_responses()
        # # cleaned_responses = []
        # # for response in responses:
        # # print(responses)
        # #     response = clean_response(response)
        # #     cleaned_responses.append(response)

        # new_responses = [res for res in responses if res not in displayed_responses]
        
        # if new_responses:
        #     display_responses(new_responses)
        #     displayed_responses.extend(new_responses)
        
        # st.rerun()
    
if __name__ == "__main__":
    main()