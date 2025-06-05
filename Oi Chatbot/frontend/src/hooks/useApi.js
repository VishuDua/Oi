import { useState, useEffect, useCallback } from 'react';
import api from '../api/fastapi';

// Base hook for API calls
function useApi(apiFunction, initialData = null, immediate = false) {
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFunction(...args);
      setData(result);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiFunction]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { 
    data, 
    loading, 
    error, 
    execute,
    // Helper to reset the hook state
    reset: () => {
      setData(initialData);
      setError(null);
      setLoading(false);
    }
  };
}

// ====== Transcript Hooks ======
export function useTranscript(mode = 'speaker', immediate = true) {
  return useApi(
    useCallback(() => api.getTranscript(mode), [mode]),
    [],
    immediate
  );
}

// ====== Analysis Hooks ======
export function useEmotionAnalysis(immediate = false) {
  return useApi(
    useCallback((text, speakerId = null) => 
      api.analyzeEmotion(text, speakerId), []),
    null,
    immediate
  );
}

export function useSentimentAnalysis(immediate = false) {
  return useApi(
    useCallback((text, speakerId = null) => 
      api.analyzeSentiment(text, speakerId), []),
    null,
    immediate
  );
}

export function useSummary(immediate = false) {
  return useApi(
    useCallback((text, speakerId = null) => 
      api.generateSummary(text, speakerId), []),
    null,
    immediate
  );
}

export function useKeywords(immediate = false) {
  return useApi(
    useCallback((text, speakerId = null) => 
      api.extractKeywords(text, speakerId), []),
    null,
    immediate
  );
}

// ====== System Hooks ======
export function useStatus(immediate = true) {
  return useApi(api.getStatus, null, immediate);
}

export function useHealthCheck(immediate = false) {
  return useApi(api.checkHealth, { status: 'checking' }, immediate);
}

// ====== Combined Analysis Hook ======
export function useTextAnalysis(initialText = '', immediate = false) {
  const [text, setText] = useState(initialText);
  const [speakerId, setSpeakerId] = useState(null);
  
  const emotion = useEmotionAnalysis(false);
  const sentiment = useSentimentAnalysis(false);
  const summary = useSummary(false);
  const keywords = useKeywords(false);
  
  // Combined loading state
  const loading = emotion.loading || sentiment.loading || 
                 summary.loading || keywords.loading;
  
  // Combined error state
  const error = emotion.error || sentiment.error || 
               summary.error || keywords.error;
  
  // Execute all analysis functions
  const analyze = useCallback(async (textToAnalyze = text, speaker = speakerId) => {
    if (!textToAnalyze.trim()) {
      return Promise.reject(new Error('No text provided for analysis'));
    }
    
    setText(textToAnalyze);
    if (speaker) setSpeakerId(speaker);
    
    try {
      const results = await Promise.all([
        emotion.execute(textToAnalyze, speaker),
        sentiment.execute(textToAnalyze, speaker),
        summary.execute(textToAnalyze, speaker),
        keywords.execute(textToAnalyze, speaker)
      ]);
      
      return {
        emotion: results[0],
        sentiment: results[1],
        summary: results[2],
        keywords: results[3]
      };
    } catch (err) {
      throw err;
    }
  }, [text, speakerId, emotion.execute, sentiment.execute, summary.execute, keywords.execute]);
  
  // Reset all analysis states
  const reset = useCallback(() => {
    emotion.reset();
    sentiment.reset();
    summary.reset();
    keywords.reset();
    setText('');
    setSpeakerId(null);
  }, [emotion, sentiment, summary, keywords]);
  
  // Auto-run analysis if immediate is true and text is provided
  useEffect(() => {
    if (immediate && initialText) {
      analyze(initialText, speakerId);
    }
  }, [immediate, initialText, speakerId, analyze]);
  
  return {
    text,
    setText,
    speakerId,
    setSpeakerId,
    emotion: emotion.data,
    sentiment: sentiment.data,
    summary: summary.data,
    keywords: keywords.data,
    loading,
    error,
    analyze,
    reset,
    // Individual states in case they're needed
    states: {
      emotion: emotion,
      sentiment: sentiment,
      summary: summary,
      keywords: keywords
    }
  };
}
