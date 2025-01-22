import React, { useState } from "react";
import ChatWindow from "./components/chatWindow";
import InputBar from "./components/inputBar";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (userInput) => {
    const newUserMessage = {
      sender: "user",
      query: userInput,
      result: null, 
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/recommend_coffee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userInput }),
      });

      const data = await response.json();
      const newBotMessage = {
        sender: "bot",
        query: data.answer.query, // user query
        result: data.answer.result, // server response
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, newBotMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = {
        sender: "bot",
        query: userInput,
        result: "서버 연결에 문제가 발생했습니다. 다시 시도해주세요.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1 className="app-title">BrewWing</h1>
    
      </header>
      <ChatWindow messages={messages} />
      {loading && <div className="loading-message">Loading...</div>}
      <InputBar onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
