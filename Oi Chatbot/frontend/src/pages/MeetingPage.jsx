import React, { useState, useEffect, useRef, useCallback } from "react";
import { useTranscript } from "../hooks/useApi";
import TranscriptAnalysis from "../components/TranscriptAnalysis";
import { MicrophoneIcon, StopIcon, PlayIcon, PauseIcon } from "@heroicons/react/24/solid";

// Helper function to parse speaker from transcript line
const parseSpeaker = (line) => {
  const match = line?.match(/\[\d+:\d+:\d+\]\s*(Speaker_\d+):/);
  return match ? match[1] : null;
};

export default function MeetingPage() {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [selectedSpeaker, setSelectedSpeaker] = useState(null);
  const [transcriptHistory, setTranscriptHistory] = useState([]);
  const transcriptEndRef = useRef(null);
  
  // Use the useTranscript hook to fetch transcripts
  const { data: transcripts = [], loading, error } = useTranscript('speaker', true);
  
  // Update transcript history when new transcripts arrive
  useEffect(() => {
    if (transcripts.length > 0) {
      setTranscriptHistory(prev => {
        // Only add new transcripts that aren't already in history
        const newTranscripts = transcripts.filter(
          (t, i) => i >= prev.length
        );
        return [...prev, ...newTranscripts];
      });
    }
  }, [transcripts]);
  
  // Auto-scroll to bottom when new transcripts arrive
  useEffect(() => {
    if (transcriptEndRef.current) {
      transcriptEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [transcriptHistory]);
  
  // Handle text selection for analysis
  const handleTextSelect = useCallback((e) => {
    const selection = window.getSelection();
    const selectedText = selection.toString().trim();
    
    if (selectedText) {
      // Find which speaker the selected text belongs to
      const range = selection.getRangeAt(0);
      const container = range.startContainer.parentElement;
      const lineElement = container.closest('.transcript-line');
      
      if (lineElement) {
        const lineIndex = Array.from(lineElement.parentElement.children).indexOf(lineElement);
        const speaker = parseSpeaker(transcriptHistory[lineIndex]);
        setSelectedSpeaker(speaker);
      }
      
      setSelectedText(selectedText);
    }
  }, [transcriptHistory]);
  
  // Toggle recording state
  const toggleRecording = () => {
    // In a real app, you would start/stop the recording here
    setIsRecording(!isRecording);
    setIsPaused(false);
  };
  
  // Toggle pause state
  const togglePause = () => {
    setIsPaused(!isPaused);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header with controls */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800 dark:text-white">
              Meeting Transcription
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Real-time transcription and analysis
            </p>
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={togglePause}
              disabled={!isRecording}
              className={`flex items-center px-4 py-2 rounded-md ${
                isRecording 
                  ? 'bg-yellow-500 hover:bg-yellow-600 text-white' 
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
              } transition-colors`}
            >
              {isPaused ? (
                <>
                  <PlayIcon className="h-5 w-5 mr-2" />
                  Resume
                </>
              ) : (
                <>
                  <PauseIcon className="h-5 w-5 mr-2" />
                  Pause
                </>
              )}
            </button>
            
            <button
              onClick={toggleRecording}
              className={`flex items-center px-4 py-2 rounded-md ${
                isRecording 
                  ? 'bg-red-500 hover:bg-red-600 text-white' 
                  : 'bg-green-600 hover:bg-green-700 text-white'
              } transition-colors`}
            >
              {isRecording ? (
                <>
                  <StopIcon className="h-5 w-5 mr-2" />
                  Stop Recording
                </>
              ) : (
                <>
                  <MicrophoneIcon className="h-5 w-5 mr-2" />
                  Start Recording
                </>
              )}
            </button>
          </div>
        </div>
        
        {/* Status indicators */}
        <div className="flex flex-wrap items-center gap-4 text-sm">
          <div className="flex items-center">
            <div className={`w-3 h-3 rounded-full mr-2 ${
              isRecording 
                ? isPaused 
                  ? 'bg-yellow-500' 
                  : 'bg-green-500 animate-pulse' 
                : 'bg-red-500'
            }`}></div>
            <span className="text-gray-700 dark:text-gray-300">
              {isRecording ? (isPaused ? 'Paused' : 'Recording') : 'Not Recording'}
            </span>
          </div>
          
          {loading && (
            <div className="flex items-center text-blue-600 dark:text-blue-400">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Updating transcript...
            </div>
          )}
          
          {error && (
            <div className="text-red-600 dark:text-red-400">
              Error loading transcript: {error.message}
            </div>
          )}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Transcript Panel */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden">
              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
                  Live Transcript
                </h2>
              </div>
              
              <div 
                className="p-4 h-[600px] overflow-y-auto bg-gray-50 dark:bg-gray-900/50"
                onMouseUp={handleTextSelect}
              >
                {transcriptHistory.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-gray-500 dark:text-gray-400">
                    {loading ? 'Loading transcript...' : 'No transcription available. Start speaking to see the transcript here.'}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {transcriptHistory.map((line, idx) => {
                      const speaker = parseSpeaker(line);
                      const text = line?.replace(/^\[\d+:\d+:\d+\]\s*\w+:\s*/, '') || line;
                      const time = line?.match(/^\[(\d+:\d+:\d+)\]/)?.[1] || '';
                      
                      return (
                        <div 
                          key={idx} 
                          className="transcript-line p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-text"
                        >
                          <div className="flex items-start gap-2">
                            {speaker && (
                              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                                {speaker}
                              </span>
                            )}
                            {time && (
                              <span className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                                {time}
                              </span>
                            )}
                          </div>
                          <p className="mt-1 text-gray-800 dark:text-gray-200">
                            {text}
                          </p>
                        </div>
                      );
                    })}
                    <div ref={transcriptEndRef} />
                  </div>
                )}
              </div>
            </div>
          </div>
          
          {/* Analysis Panel */}
          <div className="lg:col-span-1">
            <TranscriptAnalysis 
              initialText={selectedText} 
              speakerId={selectedSpeaker}
              autoAnalyze={!!selectedText}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
