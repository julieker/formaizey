import requests
from saveMaiseyHist import insert_history

# --- Credentials ---
API_TOKEN = "bc2ff4fe71865f3a1b64224970d56a528ab31a6c06d26e0fb1c4dea81aa9ddc1"
PROJECT_PK = "20edd46a-8627-45fd-a861-d843e46813df"

# --- Endpoints ---
BASE_URL = "https://umgpt.umich.edu/maizey/api"

def create_conversation():
    url = f"{BASE_URL}/projects/{PROJECT_PK}/conversation/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.post(url, headers=headers)
    print ("RESONSE STATUS")
    print (response.status_code)
    if response.status_code == 201:
        convo = response.json()
        convo_pk = convo.get("pk")
        if convo_pk not in [None, '', 0]:
            print("Conversation created. PK:", convo_pk)
            return convo_pk
        else:
            print("Conversation creation returned an invalid PK!", convo)
            return None
    else:
        print("Error creating conversation:", response.text)
        return None

def send_message(conversation_pk, message):
    url = f"{BASE_URL}/projects/{PROJECT_PK}/conversation/{conversation_pk}/messages/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"query": message}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        reply = response.json()
        return reply.get("response")
    else:
        print("Error sending message:", response.text)
        return None

def main():
    conversation_pk = create_conversation()
    if not conversation_pk:
        print("Failed to start conversation. Exiting.")
        return

    print("\nStart chatting with Maizey! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Ending conversation.")
            break
        response = send_message(conversation_pk, user_input)
        if response:
            print("Maizey:", response)
            insert_history(user_input,  response) 
if __name__ == "__main__":
    main()
