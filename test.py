# This is your existing code
import subprocess

def main():
    while True:
        user_input = input("Enter user query: ")
        if user_input == "stop":
            break
        cmd = ['ollama', 'run', 'llama3', user_input]
        llm_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = llm_output.communicate()  # Capture the output
        if stdout:
            print(stdout.decode())  # Decode bytes to string and print
        else:
            print("No llama output")

if __name__ == "__main__":
    main()
