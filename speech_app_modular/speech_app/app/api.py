from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.writer import transcript_lines_plain, transcript_lines_speaker, lock

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/transcript")
async def get_transcript(mode: str = "plain"):
    with lock:
        return list(transcript_lines_plain) if mode == "plain" else list(transcript_lines_speaker)

@app.get("/status")
async def status():
    with lock:
        return {"lines": len(transcript_lines_speaker)}
