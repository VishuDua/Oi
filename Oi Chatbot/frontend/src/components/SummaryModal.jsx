import React, { useState, useEffect } from "react";
import { sendChatMessage } from "../api/openai";

export default function SummaryModal({ messages, onClose }) {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const runSummary = async () => {
      setLoading(true);
      const transcriptLines = messages.map(
        (m) => `${m.sender === "user" ? "User" : "Bot"}: ${m.text}`
      );
      const prompt = [
        {
          role: "system",
          content: "Please provide a brief summary of the conversation below:",
        },
        { role: "user", content: transcriptLines.join("\n") },
      ];
      try {
        const result = await sendChatMessage(prompt);
        setSummary(result);
      } catch (err) {
        setSummary("⚠️ Could not generate summary.");
      }
      setLoading(false);
    };

    runSummary();
  }, [messages]);

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-gray-800 rounded-2xl shadow-xl w-11/12 max-w-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold text-white">Conversation Summary</h3>
          <button
            onClick={onClose}
            className="text-gray-300 hover:text-white"
            aria-label="Close summary"
          >✕</button>
        </div>
        <div className="h-48 overflow-y-auto bg-gray-700 p-4 rounded-lg text-gray-200">
          {loading ? <p className="text-gray-400">Generating summary...</p> : <p>{summary}</p>}
        </div>
        <div className="mt-4 flex justify-end">
          <button onClick={onClose} className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
