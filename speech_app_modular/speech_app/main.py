import threading
import uvicorn
from app.api import app
from app.audio_input import start_stream
from app.transcription import process_chunk
from app.writer import writer_thread
from app.performance import monitor

known_speakers = {}

def background_tasks():
    threading.Thread(target=writer_thread, daemon=True).start()
    threading.Thread(target=monitor, daemon=True).start()
    threading.Thread(target=start_stream, args=(None, lambda audio: process_chunk(audio, known_speakers)), daemon=True).start()

if __name__ == "__main__":
    background_tasks()
    uvicorn.run(app, host="0.0.0.0", port=9575)
