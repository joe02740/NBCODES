import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css'; // We'll create this file for styling

function ChatInterface({ initialContext, explanation }) {
  const [messages, setMessages] = useState([
    { text: explanation, sender: 'ai' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (inputMessage.trim() === '') return;

    setMessages(prev => [...prev, { text: inputMessage, sender: 'user' }]);

    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputMessage, 
          context: initialContext 
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      setMessages(prev => [...prev, { text: data.response, sender: 'ai' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { text: "Sorry, I couldn't process your request.", sender: 'ai' }]);
    }

    setInputMessage('');
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your follow-up question..."
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatInterface;