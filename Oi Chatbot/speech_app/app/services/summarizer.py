from typing import Dict, Any, List
from transformers import pipeline
import torch
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# Configure logging
logger = logging.getLogger(__name__)

class TextSummarizer:
    """Service for generating text summaries"""
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        
        try:
            # Initialize the summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                device=self.device
            )
            logger.info(f"Text summarizer initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize text summarizer: {str(e)}")
            raise
    
    def generate_summary(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """
        Generate a summary of the given text
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            
        Returns:
            Generated summary text
        """
        if not text.strip():
            return ""
            
        try:
            # Use BART for short to medium texts
            if len(text.split()) < 500:  # Roughly 2-3 paragraphs
                result = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )
                return result[0]['summary_text'].strip()
            else:
                # For longer texts, use extractive summarization first
                return self._extractive_summary(text, max_sentences=5)
                
        except Exception as e:
            logger.error(f"Error in text summarization: {str(e)}")
            # Fallback to extractive summarization
            return self._extractive_summary(text, max_sentences=3)
    
    def _extractive_summary(self, text: str, max_sentences: int = 5) -> str:
        """
        Generate an extractive summary using LSA (Latent Semantic Analysis)
        
        Args:
            text: Input text
            max_sentences: Maximum number of sentences in the summary
            
        Returns:
            Extracted summary text
        """
        try:
            # Initialize the parser
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            
            # Initialize the summarizer
            stemmer = Stemmer("english")
            summarizer = LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")
            
            # Generate the summary
            summary = summarizer(parser.document, max_sentences)
            
            # Join the sentences
            return " ".join([str(sentence) for sentence in summary])
            
        except Exception as e:
            logger.error(f"Error in extractive summarization: {str(e)}")
            # Return the first few sentences as a fallback
            sentences = text.split('. ')
            return '. '.join(sentences[:3]) + ('.' if len(sentences) > 3 else '')

# Singleton instance
text_summarizer = TextSummarizer()

def generate_summary(text: str, max_length: int = 130, min_length: int = 30) -> str:
    """
    Generate a summary of the given text
    
    Args:
        text: Input text to summarize
        max_length: Maximum length of the summary
        min_length: Minimum length of the summary
        
    Returns:
        Generated summary text
    """
    return text_summarizer.generate_summary(text, max_length, min_length)
