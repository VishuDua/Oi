import React from "react";

export default function AudioRecorder({ onTranscription, className = "" }) {
  // Placeholder for voice input; real microphone integration can be added later
  return (
    <div className={`flex items-center justify-center w-full ${className}`}>
      <button
        onClick={() => { if (onTranscription) onTranscription(); }}
        className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-full transition"
      >
        🎤 Speak
      </button>
    </div>
  );
}
