// src/App.js
import React, { useState } from "react";
import ChatWindow from "./components/chatWindow";
import InputBar from "./components/inputBar";
import "./App.css";

function App() {
  // 채팅 메시지 상태
  const [messages, setMessages] = useState([]);

  // 메시지 전송 함수
  const handleSendMessage = async (userInput) => {
    // 사용자가 입력한 메시지를 먼저 대화창에 표시
    const newUserMessage = {
      sender: "user",
      text: userInput,
    };
    setMessages((prev) => [...prev, newUserMessage]);

    try {
      // FastAPI 서버로 POST 요청
      const response = await fetch("http://localhost:8000/recommend_coffee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userInput }),
      });
      const data = await response.json();

      // 서버의 추천 결과를 봇 메시지로 추가
      const newBotMessage = {
        sender: "bot",
        text: data.coffeeRecommendation,
      };
      setMessages((prev) => [...prev, newBotMessage]);
    } catch (error) {
      console.error("Error:", error);
      // 에러 발생 시 안내 메시지
      const errorMessage = {
        sender: "bot",
        text: "서버 연결에 문제가 생겼습니다. 잠시 후 다시 시도해주세요.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  return (
    <div className="App">
      {/* 상단(혹은 중앙)에 채팅 창 배치 */}
      <ChatWindow messages={messages} />
      
      {/* 말풍선 중간에 이미지를 넣을 공간(예시) */}
      <div className="image-container">
        <img 
          src="/coffee_image.jpg" 
          alt="Coffee" 
          className="coffee-image"
        />
      </div>

      {/* 하단에 텍스트 입력 + 버튼 */}
      <InputBar onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
