import React from 'react';

const MessageDisplay = ({ messages, isLoading }) => {
  return (
    <div className="chat-messages">
      {messages.length === 0 ? (
        <div className="welcome-message">
          <p>Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook.</p>
          <p>Please select text from the textbook content and ask me questions about it.</p>
        </div>
      ) : (
        messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <div className="message-text">{message.text}</div>
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))
      )}
      {isLoading && (
        <div className="message bot-message">
          <div className="message-text">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageDisplay;