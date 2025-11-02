<template> 
<!--
This is the template section.  Here is where you click on a button to start the conversation.   The startConversation refers to the function below in the scriptand interacts with the route set up in flask  flaskmaizey.py i.e. http://localhost:5000/message for message which starts the conversation and sends a message.  
-->

  <div>
    <button @click="startConversation" v-if="!conversationStarted">Start Conversation</button>
    <div v-if="conversationStarted">
      <input v-model="messageInput" @keyup.enter="sendMessage" placeholder="Type a message..." />
      <button @click="sendMessage">Send</button>
      <div v-for="(chat, index) in chatLog" :key="index" style="margin-top: 1em;">
        <div><strong>You:</strong> {{ chat.user }}</div>
        <div><strong>Maizey:</strong> {{ chat.maizey }}</div>
      </div>
    </div>
  </div>
<br>
<br>
<br>
<div>
<span> Here is the history:  </span>


<!--
This is the showHistory section.  There is a toggle button 
On  a key up sendMessage is called which sends the message and calls fetchHisory which is connected to the flask route http://localhost:5000/history which calls backend code in flaskmaizey.py which calls saveMaiseyHist.py to fetch the history.  This is a toggle button indicated by the v-if statement.   When showHistory is pressed the history log is displayed  
-->
<button @click="handleToggleHistory">
    {{ showHistory ? 'Hide' : 'Show' }} History
  </button>
  <div v-if="showHistory">
    <div v-for="(item, i) in historyLog" :key="i" style="margin:1em 0;">
      <div><strong>You:</strong> {{ item.user_message }}</div>
      <div><strong>Maizey:</strong> {{ item.maizey_response }}</div>
      <div><small>{{ item.timestamp }}</small></div>
    </div>
  </div>






</div>


</template>







<script setup>
import { ref } from 'vue'


const showHistory = ref(false)
const historyLog = ref([])

/*

The fetchHistory is the function that is called for the showHistory button above.  It fetches from the flask route http://localhost:5000/history set up in 
flaskmaizey.py which calls saveMaiseyHist.py to fetch the history.     
*/
const fetchHistory = async () => {
  const res = await fetch('http://localhost:5000/history')
  if (res.ok) {
    historyLog.value = await res.json()
  } else {
    historyLog.value = [ { user_message: 'Could not fetch history!', maizey_response: '' } ]
  }
}







const chatLog = ref([])
const messageInput = ref('')
const conversationStarted = ref(false)

const startConversation = async () => {
  const res = await fetch('http://localhost:5000/start', { method: 'POST' })
  const data = await res.json()
  if (data.success) {
    conversationStarted.value = true
  }
}

/*
The sendMessage is called whenever a message is typed and a keydown or enter is pressed.  It connects with the flask route in http://localhost:5000/message
in flaskmaizey.py and sends the message and waits for a response. The routine fetchHistory is called at the end so that when you send a message and get a response the history is refreshed. 

*/
const sendMessage = async () => {
  if (!messageInput.value.trim()) return
  const userMsg = messageInput.value
  const res = await fetch('http://localhost:5000/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userMsg })
  })
  const data = await res.json()
  chatLog.value.push({ user: userMsg, maizey: data.response || data.error || 'No reply' })
  messageInput.value = ''
   // Update history display
  if (showHistory.value) {
    await fetchHistory()
  }
}


const handleToggleHistory = () => {
  showHistory.value = !showHistory.value
  if (showHistory.value && historyLog.value.length === 0) {
    fetchHistory()
  }
}





</script>
