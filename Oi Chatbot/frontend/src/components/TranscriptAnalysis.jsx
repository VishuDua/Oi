import React, { useState, useEffect, useCallback } from 'react';
import { useTextAnalysis } from '../hooks/useApi';

const EmotionDisplay = ({ emotion }) => {
  if (!emotion) return null;
  
  const getEmotionColor = (label) => {
    switch(label.toLowerCase()) {
      case 'joy': return 'bg-yellow-100 text-yellow-800';
      case 'sadness': return 'bg-blue-100 text-blue-800';
      case 'anger': return 'bg-red-100 text-red-800';
      case 'fear': return 'bg-purple-100 text-purple-800';
      case 'surprise': return 'bg-green-100 text-green-800';
      case 'love': return 'bg-pink-100 text-pink-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Dominant Emotion</h3>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getEmotionColor(emotion.dominant_emotion?.label)}`}>
          {emotion.dominant_emotion?.label || 'Neutral'}
        </span>
      </div>
      
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-700">Emotion Breakdown</h4>
        <div className="space-y-1.5">
          {emotion.emotions?.map((e, i) => (
            <div key={i} className="flex items-center">
              <span className="w-24 text-sm text-gray-600 capitalize">{e.label}</span>
              <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-blue-500 rounded-full" 
                  style={{ width: `${e.score * 100}%` }}
                />
              </div>
              <span className="ml-2 text-xs w-10 text-right">
                {Math.round(e.score * 100)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const SentimentDisplay = ({ sentiment }) => {
  if (!sentiment) return null;
  
  const getSentimentColor = (label) => {
    switch(label) {
      case 'POSITIVE': return 'bg-green-100 text-green-800';
      case 'NEGATIVE': return 'bg-red-100 text-red-800';
      case 'NEUTRAL': 
      default: 
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Sentiment</h3>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(sentiment.label)}`}>
          {sentiment.label || 'Neutral'}
        </span>
      </div>
      
      <div>
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Confidence</span>
          <span className="font-medium">
            {sentiment.score ? `${Math.round(sentiment.score * 100)}%` : 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
};

const TranscriptAnalysis = ({ initialText = '', speakerId = null, autoAnalyze = true }) => {
  const [selectedText, setSelectedText] = useState(initialText);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  const {
    text,
    emotion,
    sentiment,
    summary,
    keywords,
    loading,
    error,
    analyze,
    reset
  } = useTextAnalysis(selectedText, autoAnalyze);

  // Handle text selection changes
  useEffect(() => {
    if (initialText && initialText !== selectedText) {
      setSelectedText(initialText);
    }
  }, [initialText, selectedText]);

  // Handle analysis when text or speaker changes
  useEffect(() => {
    if (autoAnalyze && selectedText) {
      const analyzeText = async () => {
        setIsAnalyzing(true);
        try {
          await analyze(selectedText, speakerId);
        } catch (err) {
          console.error('Analysis error:', err);
        } finally {
          setIsAnalyzing(false);
        }
      };
      
      analyzeText();
    }
  }, [selectedText, speakerId, autoAnalyze, analyze]);

  const handleTextSelection = (text) => {
    if (text && text.trim()) {
      setSelectedText(text.trim());
    }
  };

  const handleAnalyzeClick = async () => {
    if (!selectedText.trim()) return;
    
    setIsAnalyzing(true);
    try {
      await analyze(selectedText, speakerId);
    } catch (err) {
      console.error('Analysis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-800">Text Analysis</h2>
          <div className="flex space-x-2">
            <button
              onClick={handleAnalyzeClick}
              disabled={!selectedText || loading || isAnalyzing}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isAnalyzing ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : 'Analyze'}
            </button>
            <button
              onClick={reset}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              Reset
            </button>
          </div>
        </div>
        
        {error && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700">
            <p>Error: {error.message || 'Failed to analyze text'}</p>
          </div>
        )}
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left column - Analysis results */}
          <div className="space-y-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <EmotionDisplay emotion={emotion} />
            </div>
            
            <div className="p-4 bg-gray-50 rounded-lg">
              <SentimentDisplay sentiment={sentiment} />
            </div>
            
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-medium mb-3">Summary</h3>
              {summary?.summary ? (
                <p className="text-gray-700">{summary.summary}</p>
              ) : (
                <p className="text-gray-500 italic">No summary available</p>
              )}
            </div>
          </div>
          
          {/* Right column - Text and Keywords */}
          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-medium">Selected Text</h3>
                <span className="text-sm text-gray-500">
                  {selectedText ? `${selectedText.split(/\s+/).length} words` : 'No text selected'}
                </span>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg h-40 overflow-y-auto">
                {selectedText ? (
                  <p className="text-gray-800">{selectedText}</p>
                ) : (
                  <p className="text-gray-500 italic">Select text to analyze</p>
                )}
              </div>
            </div>
            
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-medium mb-3">Key Phrases</h3>
              <div className="flex flex-wrap gap-2">
                {keywords?.keywords?.length > 0 ? (
                  keywords.keywords.map((keyword, i) => (
                    <span 
                      key={i}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {keyword}
                    </span>
                  ))
                ) : (
                  <p className="text-gray-500 italic">No key phrases extracted</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Debug panel - only shown in development */}
      {process.env.NODE_ENV === 'development' && (
        <div className="p-4 bg-gray-100 border-t border-gray-200 text-xs text-gray-600">
          <h4 className="font-bold mb-2">Debug Info</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <h5 className="font-semibold">Emotion</h5>
              <pre className="overflow-x-auto">
                {JSON.stringify(emotion, null, 2)}
              </pre>
            </div>
            <div>
              <h5 className="font-semibold">Sentiment</h5>
              <pre className="overflow-x-auto">
                {JSON.stringify(sentiment, null, 2)}
              </pre>
            </div>
            <div>
              <h5 className="font-semibold">Keywords</h5>
              <pre className="overflow-x-auto">
                {JSON.stringify(keywords, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TranscriptAnalysis;
