from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import os
import logging
from pathlib import Path

# Import services
from app.writer import transcript_lines_plain, transcript_lines_speaker, lock
from app.services.emotion_service import EmotionResult, get_emotion_detector
from app.services.sentiment_analyzer import analyze_sentiment
from app.services.summarizer import generate_summary
from app.services.keyword_extractor import extract_keywords

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Oi Voice Chatbot API",
    description="API for Oi Voice Chatbot with Transcription and Analysis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Templates
TEMPLATES_DIR = frontend_path / "src" if frontend_path.exists() else None
if TEMPLATES_DIR and TEMPLATES_DIR.exists():
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Pydantic models
class AnalysisRequest(BaseModel):
    text: str
    speaker_id: Optional[str] = None
    timestamp: Optional[float] = None

class AnalysisResponse(BaseModel):
    text: str
    analysis: Dict[str, Any]

# Routes
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    if TEMPLATES_DIR and (TEMPLATES_DIR / "index.html").exists():
        return templates.TemplateResponse("index.html", {"request": request})
    return {"message": "Frontend not found. Please check if the frontend is built."}

# Transcript Endpoints
@app.get("/api/transcript", response_model=List[Dict[str, Any]])
async def get_transcript(mode: str = "speaker"):
    """Get transcript in either plain text or with speaker information"""
    with lock:
        if mode == "plain":
            return [{"text": line} for line in transcript_lines_plain]
        else:
            return [{"speaker": line[0], "text": line[1]} for line in transcript_lines_speaker]

# Analysis Endpoints
@app.post("/api/analyze/emotion", response_model=Dict[str, Any])
async def analyze_emotion(request: AnalysisRequest):
    """Analyze emotion from text"""
    try:
        detector = get_emotion_detector()
        emotions = detector.detect_emotions(request.text)
        dominant = max(emotions, key=lambda x: x["score"]) if emotions else None
        
        return {
            "text": request.text,
            "emotions": emotions,
            "dominant_emotion": dominant
        }
    except Exception as e:
        logger.error(f"Error in emotion analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing emotion analysis")

@app.post("/api/analyze/sentiment", response_model=Dict[str, Any])
async def analyze_sentiment_endpoint(request: AnalysisRequest):
    """Analyze sentiment from text"""
    try:
        sentiment = analyze_sentiment(request.text)
        return {
            "text": request.text,
            "sentiment": sentiment
        }
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing sentiment analysis")

@app.post("/api/analyze/summary", response_model=Dict[str, Any])
async def generate_summary_endpoint(request: AnalysisRequest):
    """Generate a summary of the text"""
    try:
        summary = generate_summary(request.text)
        return {
            "text": request.text,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating summary")

@app.post("/api/analyze/keywords", response_model=Dict[str, Any])
async def extract_keywords_endpoint(request: AnalysisRequest):
    """Extract keywords from text"""
    try:
        keywords = extract_keywords(request.text)
        return {
            "text": request.text,
            "keywords": keywords
        }
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}")
        raise HTTPException(status_code=500, detail="Error extracting keywords")

# System Endpoints
@app.get("/api/status")
async def status():
    """Get the current status of the service"""
    with lock:
        return {
            "status": "running",
            "timestamp": datetime.utcnow().isoformat(),
            "total_lines": len(transcript_lines_speaker),
            "last_update": transcript_lines_speaker[-1][1] if transcript_lines_speaker else None
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "oi-voice-chatbot",
        "timestamp": datetime.utcnow().isoformat()
    }

# Error Handlers
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": f"The requested URL {request.url} was not found"},
    )

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error occurred"},
    )
