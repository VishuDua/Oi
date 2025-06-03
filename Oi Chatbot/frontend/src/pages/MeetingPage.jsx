// src/pages/MeetingPage.jsx
import React, { useState, useEffect, useRef } from "react";
import "./MeetingPage.css";

export default function MeetingPage() {
  // ← Replace with your actual ngrok URL (no trailing slash)
  const BASE_URL = "https://7ca2-207-107-70-174.ngrok-free.app/";

  const [transcripts, setTranscripts] = useState([]);   // array of "[HH:MM:SS] SpeakerX: text"
  const intervalRef = useRef(null);

  const fetchTranscripts = () => {
    fetch(`${BASE_URL}/transcript?mode=speaker`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        // data is an array of strings like "[12:34:56] Speaker_1: Hello"
        setTranscripts(data || []);
      })
      .catch((err) => console.error("Error fetching speaker transcripts:", err));
  };

  useEffect(() => {
    // On mount, fetch once immediately, then every 2 seconds
    fetchTranscripts();
    intervalRef.current = setInterval(fetchTranscripts, 2000);
    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <div className="meeting-container">
      <div className="recording-indicator">Recording…</div>

      <div className="transcript-panels">
        {transcripts.length === 0 ? (
          <div className="no-lines">No speech detected yet…</div>
        ) : (
          transcripts.map((line, idx) => (
            <div key={idx} className="transcript-line">
              {line}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
