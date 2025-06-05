from typing import List, Dict, Any, Tuple
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

# Configure logging
logger = logging.getLogger(__name__)

class KeywordExtractor:
    """Service for extracting keywords and key phrases from text"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.punctuation = set(string.punctuation)
        logger.info("Keyword extractor initialized")
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess the text by tokenizing, removing stopwords, and lemmatizing
        
        Args:
            text: Input text to preprocess
            
        Returns:
            List of preprocessed tokens
        """
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and punctuation, and lemmatize
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and token not in self.punctuation:
                # Lemmatize the token
                lemma = self.lemmatizer.lemmatize(token)
                processed_tokens.append(lemma)
        
        return processed_tokens
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Extract keywords from the given text
        
        Args:
            text: Input text to extract keywords from
            top_n: Number of top keywords to return
            
        Returns:
            List of dictionaries containing keywords and their scores
        """
        if not text.strip():
            return []
            
        try:
            # Preprocess the text
            tokens = self.preprocess_text(text)
            
            # Calculate word frequencies
            freq_dist = FreqDist(tokens)
            
            # Get the most common words
            keywords = []
            for word, freq in freq_dist.most_common(top_n * 2):  # Get more to filter later
                # Skip very short words
                if len(word) < 3:
                    continue
                    
                # Calculate score (normalized frequency)
                score = freq / len(tokens)
                
                keywords.append({
                    'word': word,
                    'score': score,
                    'frequency': freq
                })
                
                # Stop if we have enough keywords
                if len(keywords) >= top_n:
                    break
            
            return keywords
            
        except Exception as e:
            logger.error(f"Error in keyword extraction: {str(e)}")
            return []
    
    def extract_key_phrases(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract key phrases (multi-word expressions) from the text
        
        Args:
            text: Input text to extract key phrases from
            top_n: Number of top key phrases to return
            
        Returns:
            List of key phrases
        """
        if not text.strip():
            return []
            
        try:
            # Tokenize into sentences
            sentences = sent_tokenize(text)
            
            # Extract noun phrases (simple approach)
            phrases = defaultdict(int)
            
            for sentence in sentences:
                # Tokenize and tag parts of speech
                words = word_tokenize(sentence)
                tagged = nltk.pos_tag(words)
                
                # Simple noun phrase chunking (adjective + noun, or noun + noun)
                grammar = r"""
                    NP: {<JJ>*<NN.*>+}  # Adjectives followed by nouns
                        {<NN.*><NN.*>+}   # Multiple nouns together
                """
                
                cp = nltk.RegexpParser(grammar)
                tree = cp.parse(tagged)
                
                # Extract phrases
                for subtree in tree.subtrees():
                    if subtree.label() == 'NP':
                        phrase = ' '.join(word for word, tag in subtree.leaves())
                        phrases[phrase.lower()] += 1
            
            # Sort phrases by frequency and return top N
            sorted_phrases = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
            return [phrase for phrase, count in sorted_phrases[:top_n]]
            
        except Exception as e:
            logger.error(f"Error in key phrase extraction: {str(e)}")
            return []

# Singleton instance
keyword_extractor = KeywordExtractor()

def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    Extract keywords from the given text
    
    Args:
        text: Input text to extract keywords from
        top_n: Number of top keywords to return
        
    Returns:
        List of top keywords
    """
    keywords = keyword_extractor.extract_keywords(text, top_n)
    return [kw['word'] for kw in keywords]

def extract_key_phrases(text: str, top_n: int = 5) -> List[str]:
    """
    Extract key phrases from the given text
    
    Args:
        text: Input text to extract key phrases from
        top_n: Number of top key phrases to return
        
    Returns:
        List of key phrases
    """
    return keyword_extractor.extract_key_phrases(text, top_n)
