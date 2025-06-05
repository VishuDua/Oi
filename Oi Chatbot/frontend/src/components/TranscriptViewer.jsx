import React, { useState, useEffect } from 'react';
import { useTranscript, useStatus } from '../hooks/useApi';

const TranscriptViewer = () => {
  const [mode, setMode] = useState('speaker');
  const { data: transcript, loading, error, execute: refreshTranscript } = useTranscript(mode);
  const { data: status } = useStatus();
  
  // Auto-refresh the transcript every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refreshTranscript();
    }, 5000);
    
    return () => clearInterval(interval);
  }, [refreshTranscript]);

  if (loading && !transcript) {
    return <div className="p-4">Loading transcript...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-red-600">
        Error loading transcript: {error.message}
      </div>
    );
  }

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold">Live Transcript</h2>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium">View Mode:</span>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="px-3 py-1 border rounded-md text-sm"
            >
              <option value="speaker">With Speaker</option>
              <option value="plain">Plain Text</option>
            </select>
          </div>
          {status && (
            <div className="text-sm text-gray-600">
              Status: <span className="font-medium">{status.status}</span> • 
              Lines: <span className="font-medium">{status.total_lines || 0}</span>
            </div>
          )}
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        {mode === 'speaker' ? (
          <div className="space-y-4">
            {transcript && transcript.length > 0 ? (
              transcript.map((entry, index) => (
                <div key={index} className="border-l-4 border-blue-500 pl-4 py-1">
                  <div className="font-semibold text-blue-700">{entry.speaker || 'Speaker'}</div>
                  <div className="text-gray-800">{entry.text}</div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 italic">No transcript available. Start speaking to see the transcription here.</p>
            )}
          </div>
        ) : (
          <div className="whitespace-pre-wrap">
            {transcript && transcript.length > 0 ? (
              transcript.map((entry, index) => (
                <span key={index}>
                  {entry.text}
                  {index < transcript.length - 1 ? ' ' : ''}
                </span>
              ))
            ) : (
              <p className="text-gray-500 italic">No transcript available. Start speaking to see the transcription here.</p>
            )}
          </div>
        )}
      </div>
      
      <div className="mt-4 flex justify-end">
        <button
          onClick={refreshTranscript}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Refreshing...
            </>
          ) : (
            'Refresh'
          )}
        </button>
      </div>
    </div>
  );
};

export default TranscriptViewer;
