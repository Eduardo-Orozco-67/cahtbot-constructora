<template>
    <h1 class="chatbot-title">ChatBot de ayuda al cliente</h1>
    <div class="chat-container" ref="chatContainer">
      <div class="chat-messages" ref="chatMessages">
        <div v-for="message in messages" :key="message.id" class="message" :class="{ 'client-message': message.fromClient, 'bot-message': !message.fromClient }">
          {{ message.text }}
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Escribe un mensaje" />
      </div>
    </div>
  </template>
  
  <script>
  import io from 'socket.io-client';
  
  export default {
    data() {
      return {
        messages: [],
        newMessage: '',
      };
    },
    mounted() {
      const socket = io('http://127.0.0.1:3000');
  
      // Mostrar el mensaje de bienvenida al inicio
      this.messages.push({ text: "¡Bienvenido al Chatbot de Ayuda! ¿En qué puedo ayudarte hoy?", fromClient: false });
  
      socket.on('message', (text) => {
        this.messages.push({ text, fromClient: false });
        this.$nextTick(() => {
          this.scrollChatToBottom();
        });
      });
  
      // Saludar al servidor al conectarse
      socket.emit('saludo', 'Hola, soy un cliente de Vue.js');
    },
    methods: {
      sendMessage() {
        const socket = io('http://127.0.0.1:3000');
        socket.emit('message', this.newMessage);
        this.messages.push({ text: this.newMessage, fromClient: true });
        this.newMessage = '';
        this.$nextTick(() => {
          this.scrollChatToBottom();
        });
      },
      scrollChatToBottom() {
        this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
      },
    },
  };
  </script>
    
  <style>
  .chat-container {
    max-width: 900px;
    margin: 20px auto;
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .chat-messages {
    padding: 10px;
    max-height: 300px;
    overflow-y: auto;
  }
  
  .message {
    padding: 8px;
    margin-bottom: 8px;
    border-radius: 8px;
  }
  
  .client-message {
    background-color: #add8e6; /* Azul celeste para mensajes del cliente */
  }
  
  .bot-message {
    background-color: #f2f2f2; /* Gris claro para mensajes del chatbot */
  }
  
  .chat-input {
    padding: 10px;
    background-color: #fff;
    border-top: 1px solid #ccc;
  }
  
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
  }

  .chatbot-title {
  text-align: center;
  color: #7EC8E3; 
  /* tono de gris: */
  /* color: #A9A9A9; */
  /* Otra opción: */
  /* color: #CCCCCC; */
}
  </style>
  