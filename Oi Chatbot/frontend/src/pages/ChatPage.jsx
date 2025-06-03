import React, { useState, useEffect, useRef } from "react";
import "./ChatPage.css";

export default function ChatPage() {
  // ← Update this to match your current Ngrok URL (no trailing slash)
  const BASE_URL = "https://a1b2-xxx-yyy-zzz.ngrok-free.app";

  // Holds all lines returned by GET /transcript?mode=plain
  const [transcripts, setTranscripts] = useState([]);

  // Are we currently polling? Controls button label and style
  const [isListening, setIsListening] = useState(false);
  const intervalRef = useRef(null);

  // Fetch the plain‐text transcript array from the backend
  const fetchPlainTranscripts = async () => {
    try {
      const res = await fetch(`${BASE_URL}/transcript?mode=plain`);
      if (!res.ok) {
        console.error("Fetch returned HTTP", res.status);
        return;
      }
      const data = await res.json();
      // 'data' is an array of strings, e.g. ["Hello world", "Next line"]
      setTranscripts(data);
    } catch (err) {
      console.error("Error fetching /transcript?mode=plain:", err);
    }
  };

  // Start polling every 2 seconds
  const startListening = () => {
    setIsListening(true);
    fetchPlainTranscripts(); // immediate first fetch
    intervalRef.current = setInterval(fetchPlainTranscripts, 2000);
  };

  // Stop polling
  const stopListening = () => {
    setIsListening(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  // Cleanup if the component unmounts
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return (
    <div className="chat-container">
      {/* ==== Chat Transcript Window ==== */}
      <div className="chat-window">
        {transcripts.length === 0 ? (
          <div className="no-lines">
            {isListening
              ? "Listening… no speech detected yet."
              : "Click ▶️ to start listening."}
          </div>
        ) : (
          transcripts.map((line, idx) => (
            <div key={idx} className="chat-line">
              {line}
            </div>
          ))
        )}
      </div>

      {/* ==== Mic Button ==== */}
      <div className="mic-wrapper">
        <button
          onClick={isListening ? stopListening : startListening}
          className={`mic-button ${isListening ? "recording" : ""}`}
        >
          {isListening ? "⏹ Stop" : "▶️ Start"}
        </button>
      </div>
    </div>
  );
}
