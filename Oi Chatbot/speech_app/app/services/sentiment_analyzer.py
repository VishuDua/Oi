from typing import Dict, Any, List
from transformers import pipeline
import torch
import logging

# Configure logging
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Service for analyzing sentiment from text"""
    
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        self.device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
        try:
            self.classifier = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=self.device,
                return_all_scores=True
            )
            logger.info(f"Sentiment analyzer initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analyzer: {str(e)}")
            raise
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of the given text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        if not text.strip():
            return {"label": "NEUTRAL", "score": 0.0}
            
        try:
            # Get sentiment predictions
            predictions = self.classifier(text)[0]
            
            # Convert to a more usable format
            sentiments = [
                {"label": pred["label"].upper(), "score": float(pred["score"])}
                for pred in predictions
            ]
            
            # Get the dominant sentiment
            dominant = max(sentiments, key=lambda x: x["score"])
            
            return {
                "label": dominant["label"],
                "score": dominant["score"],
                "all_sentiments": {s["label"]: s["score"] for s in sentiments}
            }
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {"label": "NEUTRAL", "score": 0.0, "error": str(e)}

# Singleton instance
sentiment_analyzer = SentimentAnalyzer()

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze the sentiment of the given text
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with sentiment analysis results
    """
    return sentiment_analyzer.analyze_sentiment(text)
