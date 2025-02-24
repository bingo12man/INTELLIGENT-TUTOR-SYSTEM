<template>
  <div class="chat-wrapper">
    <div class="chat-container">
      <h1>Intelligent Tutor System</h1>
      <div class="chat-box" ref="chatBox">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
          <b>{{ msg.role === 'user' ? 'You' : 'Tutor' }}:</b> 
          <p>{{ msg.content }}</p>
        </div>
      </div>
      <div class="input-area">
        <input v-model="question" @keyup.enter="askQuestion" placeholder="Ask a question..." />
        <button @click="askQuestion">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userId: "12345", // Simulated user ID
      question: "",
      messages: [],
    };
  },
  methods: {
    async askQuestion() {
      if (!this.question.trim()) return; // Prevent empty messages
      this.messages.push({ role: "user", content: this.question });

      try {
        const response = await axios.post("http://127.0.0.1:5000/ask", {
          user_id: this.userId,
          question: this.question,
        });

        if (response.data.answer) {
          this.messages.push({ role: "assistant", content: response.data.answer });
        } else {
          this.messages.push({ role: "assistant", content: "Sorry, I couldn't process your request." });
        }
      } catch (error) {
        console.error("Error:", error);
        this.messages.push({ role: "assistant", content: "Error connecting to the server." });
      }
      this.question = "";

      // Auto-scroll to bottom
      this.$nextTick(() => {
        const chatBox = this.$refs.chatBox;
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    },
  },
};
</script>

<style>
/* General page styling */
body, html {
  background-color: #121212;
  color: white;
  font-family: "Arial", sans-serif;
  height: 100vh;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Centered wrapper */
.chat-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}

/* Chat container */
.chat-container {
  width: 450px;
  background: #1e1e1e;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 500px;
}

/* Header */
h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 15px;
}

/* Chat box */
.chat-box {
  width: 100%;
  border: 1px solid #444;
  background: #292929;
  padding: 10px;
  height: 350px;
  overflow-y: auto;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;
}

/* Messages */
.message {
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
  transition: all 0.3s ease-in-out;
}

.user {
  background: #007bff;
  color: white;
  align-self: flex-end;
}

.assistant {
  background: #3a3a3a;
  color: white;
  align-self: flex-start;
}

/* Input area */
.input-area {
  display: flex;
  margin-top: 10px;
  width: 100%;
  justify-content: space-between;
}

input {
  flex-grow: 1;
  padding: 14px;
  border: none;
  border-radius: 8px;
  background: #333;
  color: white;
  font-size: 16px;
  outline: none;
}

button {
  padding: 14px 18px;
  margin-left: 10px;
  border: none;
  border-radius: 8px;
  background: #007bff;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s ease;
}

button:hover {
  background: #0056b3;
}
</style>
