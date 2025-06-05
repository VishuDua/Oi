from typing import Dict, List, Optional
import torch
from transformers import pipeline
from pydantic import BaseModel
import logging

# Configure logging
logger = logging.getLogger(__name__)

class EmotionResult(BaseModel):
    """Model for emotion detection result"""
    label: str
    score: float
    timestamp: Optional[float] = None
    speaker_id: Optional[str] = None

class EmotionDetector:
    """Service for detecting emotions from text and audio"""
    
    def __init__(self, model_name="bhadresh-savani/bert-base-uncased-emotion"):
        self.device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
        try:
            self.classifier = pipeline(
                "text-classification",
                model=model_name,
                device=self.device,
                return_all_scores=True
            )
            self.emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]
            logger.info(f"Emotion detector initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize emotion detector: {str(e)}")
            raise
    
    def detect_emotions(self, text: str) -> List[Dict[str, float]]:
        """
        Detect emotions from text
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of dictionaries with emotion labels and scores
        """
        if not text.strip():
            return []
            
        try:
            predictions = self.classifier(text)[0]
            # Convert to list of dicts with label and score
            emotions = [
                {"label": pred["label"].lower(), "score": float(pred["score"])}
                for pred in predictions
            ]
            return emotions
        except Exception as e:
            logger.error(f"Error in emotion detection: {str(e)}")
            return []
    
    def get_dominant_emotion(self, text: str) -> Optional[Dict[str, float]]:
        """Get the dominant emotion from text"""
        emotions = self.detect_emotions(text)
        if not emotions:
            return None
        return max(emotions, key=lambda x: x["score"])

# Singleton instance
emotion_detector = EmotionDetector()

def get_emotion_detector() -> EmotionDetector:
    """Get the singleton instance of EmotionDetector"""
    return emotion_detector
