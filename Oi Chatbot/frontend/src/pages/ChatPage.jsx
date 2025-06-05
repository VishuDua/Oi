import React, { useState, useEffect, useRef } from "react";
import api from "../services/api";
import "./ChatPage.css";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [mode, setMode] = useState("text"); // "text" or "voice"
  const wsRef = useRef(null);
  const chatWindowRef = useRef(null);

  // Handle WebSocket connection for real-time speech transcription
  useEffect(() => {
    if (isListening && mode === "voice") {
      wsRef.current = api.connectSpeechWebSocket((data) => {
        if (data.text) {
          handleNewMessage(data.text);
        }
      });
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [isListening, mode]);

  // Scroll chat window to bottom when new messages arrive
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const handleNewMessage = async (text) => {
    try {
      const response = await api.getResponse(text);
      if (response.response) {
        setMessages(prev => [...prev, 
          { type: 'user', text },
          { type: 'bot', text: response.response }
        ]);
      }
    } catch (error) {
      console.error('Error getting response:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    await handleNewMessage(inputText);
    setInputText("");
  };

  const toggleMode = async () => {
    try {
      const response = await api.toggleMode();
      setMode(response.mode);
      setIsListening(false);
    } catch (error) {
      console.error('Error toggling mode:', error);
    }
  };

  return (
    <div className="chat-container">
      {/* Chat Window */}
      <div className="chat-window" ref={chatWindowRef}>
        {messages.length === 0 ? (
          <div className="no-messages">
            {mode === "voice" 
              ? "Click ▶️ to start voice chat"
              : "Type a message to start chatting"}
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              <div className="message-content">{msg.text}</div>
            </div>
          ))
        )}
      </div>

      {/* Controls */}
      <div className="chat-controls">
        <button
          onClick={toggleMode}
          className="mode-toggle"
        >
          {mode === "voice" ? "🎤 Voice Mode" : "⌨️ Text Mode"}
        </button>

        {mode === "voice" ? (
          <button
            onClick={() => setIsListening(!isListening)}
            className={`mic-button ${isListening ? "recording" : ""}`}
          >
            {isListening ? "⏹ Stop" : "▶️ Start"}
          </button>
        ) : (
          <form onSubmit={handleSubmit} className="text-input-form">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your message..."
              className="text-input"
            />
            <button type="submit" className="send-button">
              Send
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
