from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests
import os
#### use module saveMaiseyHist that interacts with the maizey_history in the postgres database.
from saveMaiseyHist import insert_history, get_history



#### run flask and cors.  Note CORS is needed for security and for communication 
#### between two different web applications on two different origins.
app = Flask(__name__)
CORS(app)  


API_TOKEN = os.environ.get('API_TOKEN')
PROJECT_PK = os.environ.get('PROJECT_PK')
BASE_URL = os.environ.get('BASE_URL')

conversation_pk = None  # Persist a single conversation for demo


# start a conversation set up the headers and post a response
def create_conversation():
    global conversation_pk
    url = f"{BASE_URL}/projects/{PROJECT_PK}/conversation/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(url, headers=headers) 

    ### if the response is successful in this case wither 200 or 201 then return success
    if response.status_code in [200, 201]:
        convo = response.json()
        conversation_pk = convo.get("pk")
        return True
    return False

######### send a message... post the message and return the resonse in jason.  Again check for 200 or 201
def send_message(message):
    url = f"{BASE_URL}/projects/{PROJECT_PK}/conversation/{conversation_pk}/messages/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"query": message}
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code in [200, 201] else {'error': response.text}


###################### This is an app route which means that this will be used in the vue file to start a conversation 
@app.route("/start", methods=["POST"])
def start_conversation():
    success = create_conversation()
    return jsonify({"success": success, "conversation_pk": conversation_pk})

######################This is  another route again it will be used in the vue file.  It sents a message and waits for the response.  If 
#####################there is a reponse it will insert the message ad the reply into the the maizey_history table in postgres.   
@app.route("/message", methods=["POST"])
def message():
    data = request.json
    msg = data.get("message")
    reply = send_message(msg)
    # Save to database before returning (if response is present)
    if 'response' in reply: 
        ## call the routine insert_history in saveMaiseyHist
        insert_history(msg, reply['response'])

    return jsonify(reply) 

#### setting up another route to be able to grab the history using saveMaiseyHist and call that in MaizeyChat.vue
@app.route("/history", methods=["GET"])
def history():
    records = get_history()
    # records should be a list of dicts: [{user_message: "...", maizey_response: "...", ...}, ...]
    return jsonify(records)



if __name__ == "__main__":
    app.run(debug=True)
