from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests
from saveMaiseyHist import insert_history, get_history




app = Flask(__name__)
CORS(app)  

API_TOKEN = "bc2ff4fe71865f3a1b64224970d56a528ab31a6c06d26e0fb1c4dea81aa9ddc1"
PROJECT_PK = "20edd46a-8627-45fd-a861-d843e46813df"
BASE_URL = "https://umgpt.umich.edu/maizey/api"

conversation_pk = None  # Persist a single conversation for demo

def create_conversation():
    global conversation_pk
    url = f"{BASE_URL}/projects/{PROJECT_PK}/conversation/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(url, headers=headers)
    if response.status_code in [200, 201]:
        convo = response.json()
        conversation_pk = convo.get("pk")
        return True
    return False

def send_message(message):
    url = f"{BASE_URL}/projects/{PROJECT_PK}/conversation/{conversation_pk}/messages/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"query": message}
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code in [200, 201] else {'error': response.text}

@app.route("/start", methods=["POST"])
def start_conversation():
    success = create_conversation()
    return jsonify({"success": success, "conversation_pk": conversation_pk})

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    msg = data.get("message")
    reply = send_message(msg)
    # Save to database before returning (if response is present)
    if 'response' in reply:
        insert_history(msg, reply['response'])

    return jsonify(reply) 


@app.route("/history", methods=["GET"])
def history():
    records = get_history()
    # records should be a list of dicts: [{user_message: "...", maizey_response: "...", ...}, ...]
    return jsonify(records)



if __name__ == "__main__":
    app.run(debug=True)
