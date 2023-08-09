from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "<YOUR_API_KEY>"
API_VERSION = "2023-05-15"
API_BASE = "<YOUR_API_ENDPOINT>"
API_DEPLOYMENT = "<YOUR_DEPLOYMENT_NAME>"

conversation = [{"role": "system", "content": "<YOUR_SYSTEM_MESSAGE>"}] # Optional 

def send_chat_message(conversation):
    url = f"{API_BASE}/openai/deployments/{API_DEPLOYMENT}/chat/completions?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    data = {
        "messages": conversation
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            assistant_response = response_data['choices'][0]['message']['content']
            return assistant_response
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    user_input = request.form['question']
    conversation.append({"role": "user", "content": user_input})
    
    assistant_response = send_chat_message(conversation)
    if assistant_response is not None:
        conversation.append({"role": "assistant", "content": assistant_response})
        return jsonify({"answer": assistant_response})
    else:
        return jsonify({"answer": "Sorry, something went wrong. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True)
