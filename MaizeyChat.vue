<template>
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
