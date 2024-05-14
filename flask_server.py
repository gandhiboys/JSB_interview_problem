from flask import Flask, request, jsonify
import subprocess
import logging
import sys

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def get_query():
    data = request.get_json()
    user_input = data['query']
    cmd = ['ollama', 'run', 'llama3', user_input]
    llm_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = llm_output.communicate()
    response = stdout.decode()
    return jsonify({'response': response})

try:
    if __name__ == '__main__':
        # Starting a thread for terminal input to not block the Flask app
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.WARNING)

        # stt = subprocess.Popen(["streamlit", "run" ,"streamlit_app.py"])

        # Starting Flask app
        app.run(port=5001)

except KeyboardInterrupt:
    # stt.terminate()
    sys.exit(0)
