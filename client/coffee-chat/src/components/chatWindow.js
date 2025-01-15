// src/components/ChatWindow.js
import React from "react";
import "./chatwindow.css";

function ChatWindow({ messages }) {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`chat-bubble ${msg.sender === "user" ? "user-bubble" : "bot-bubble"}`}
        >
          {msg.text}
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;
