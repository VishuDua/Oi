
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime
import os
from collections import deque

from modules.llm_engine import generate_response, init_llm
from modules.emotion import detect_emotions
from modules.intent import classify_intent
from modules.logger import log_to_file

# === CONFIG ===
TRANSCRIPT_API = "http://localhost:9575/transcript?mode=plain"
TRANSCRIPT_DIR = "/mnt/d/Data_Files/Transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ai_conversation_path = os.path.join(TRANSCRIPT_DIR, f"ai_responses_{timestamp_str}.txt")

# === STATE ===
chat_history = deque(maxlen=50)
last_seen_line = ""
mode = "text"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Assistant is running! Use /respond for interaction."}

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available."}

class UserInput(BaseModel):
    input: str

@app.post("/toggle_mode")
async def toggle_mode():
    global mode
    mode = "voice" if mode == "text" else "text"
    return {"mode": mode}

@app.post("/respond")
async def respond_to_input(data: UserInput):
    global last_seen_line
    user_input = data.input

    if mode == "voice":
        try:
            res = requests.get(TRANSCRIPT_API, timeout=2)
            lines = res.json()
            if lines and lines[-1] != last_seen_line:
                last_seen_line = lines[-1]
                user_input = last_seen_line.split("] ", 1)[-1]
            else:
                return {"response": None}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transcript fetch error: {str(e)}")

    ai_response = generate_response(user_input, chat_history)
    log_to_file(user_input, ai_response, ai_conversation_path)
    return {"response": ai_response}

async def poll_transcript():
    global last_seen_line
    while True:
        try:
            if mode == "voice":
                res = requests.get(TRANSCRIPT_API, timeout=2)
                lines = res.json()

                if lines and lines[-1] != last_seen_line:
                    last_seen_line = lines[-1]
                    user_input = last_seen_line.split("] ", 1)[-1]
                    ai_response = generate_response(user_input, chat_history)
                    log_to_file(user_input, ai_response, ai_conversation_path)
                    print(f"\n👤 {user_input}\n🤖 {ai_response}\n")
        except Exception as e:
            print(f"[❌ Transcript Error] {e}")

        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    init_llm()
    asyncio.create_task(poll_transcript())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8989, log_level="info")
