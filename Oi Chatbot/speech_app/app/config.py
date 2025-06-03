from datetime import datetime
import os

TRANSCRIPT_DIR = "D:/Data_Files/Transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SPEAKER_TRANSCRIPT_PATH = os.path.join(TRANSCRIPT_DIR, f"with_speakers_{TIMESTAMP}.txt")
PLAIN_TRANSCRIPT_PATH = os.path.join(TRANSCRIPT_DIR, f"plain_{TIMESTAMP}.txt")

SAMPLERATE = 16000
BLOCKSIZE = 16000
SPEAKER_THRESHOLD = 0.55
MAX_TRANSCRIPT_LINES = 10000
MAX_SPEAKERS = 4
