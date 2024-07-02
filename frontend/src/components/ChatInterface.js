import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css'; // Make sure this file exists

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
      const response = await fetch(`${process.env.REACT_APP_API_URL}/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          message: inputMessage, 
          context: initialContext 
        }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
  
      if (data.error) {
        throw new Error(data.error);
      }
  
      setMessages(prev => [...prev, { text: data.response, sender: 'ai' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { text: `Error: ${error.message}`, sender: 'ai' }]);
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