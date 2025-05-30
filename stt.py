import queue
import sys
import os
import threading
import numpy as np
import sounddevice as sd
import torch
from datetime import datetime
from flask import Flask, jsonify, request
from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.spatial.distance import cosine
from faster_whisper import WhisperModel
from scipy.io.wavfile import write
import io
import pickle
import time
from concurrent.futures import ThreadPoolExecutor
from flask_cors import CORS
from collections import deque

# === CONFIG ===
transcript_dir = "D:/Data_Files/Transcripts"
os.makedirs(transcript_dir, exist_ok=True)
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
speaker_transcript_path = os.path.join(transcript_dir, f"with_speakers_{timestamp_str}.txt")
plain_transcript_path = os.path.join(transcript_dir, f"plain_{timestamp_str}.txt")

device = None
samplerate = 16000
blocksize = 16000
speaker_threshold = 0.55
MAX_TRANSCRIPT_LINES = 1000

# === MODELS ===
device_type = "cuda" if torch.cuda.is_available() else "cpu"
encoder = VoiceEncoder().to(device_type)
whisper_model = WhisperModel("medium", device=device_type, compute_type="float16" if device_type == "cuda" else "int8")

# === STORAGE ===
known_speakers = {}
try:
    if os.path.exists("known_speakers.pkl"):
        with open("known_speakers.pkl", "rb") as f:
            known_speakers = pickle.load(f)
except Exception as e:
    print(f"[⚠️ Failed to load known_speakers.pkl] {e}. Regenerating...")
    known_speakers = {}

recent_predictions = []
q = queue.Queue()
transcript_lines_speaker = deque(maxlen=MAX_TRANSCRIPT_LINES)
transcript_lines_plain = deque(maxlen=MAX_TRANSCRIPT_LINES)
transcript_lock = threading.Lock()
write_buffer = []
executor = ThreadPoolExecutor(max_workers=2)

# === AUDIO PROCESSING ===
def callback(indata, frames, time, status):
    if status:
        print("[⚠️ Audio Status]", status, file=sys.stderr)
    q.put(bytes(indata))

def identify_speaker(audio_frames):
    wav = preprocess_wav(np.concatenate(audio_frames), source_sr=samplerate)
    if np.mean(np.abs(wav)) < 0.01:
        return "Unknown"
    embedding = encoder.embed_utterance(wav)
    min_dist = float('inf')
    identity = "Unknown"

    for name, ref_embedding in known_speakers.items():
        dist = cosine(embedding, ref_embedding)
        if dist < speaker_threshold and dist < min_dist:
            min_dist = dist
            identity = name

    recent_predictions.append(identity)
    if recent_predictions[-2:] == ["Unknown", "Unknown"]:
        new_id = f"Speaker_{len(known_speakers) + 1}"
        known_speakers[new_id] = embedding
        identity = new_id
        recent_predictions.clear()
        with open("known_speakers.pkl", "wb") as f:
            pickle.dump(known_speakers, f)

    if identity != "Unknown":
        recent_predictions.clear()

    return identity

def log_transcript(speaker, text):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line_with_speaker = f"[{timestamp}] {speaker}: {text}"
    line_plain = f"[{timestamp}] {text}"
    with transcript_lock:
        transcript_lines_speaker.append(line_with_speaker)
        transcript_lines_plain.append(line_plain)
        write_buffer.append((line_with_speaker, line_plain))
    print(line_with_speaker)

def process_chunk(audio_frames):
    full_chunk = np.concatenate(audio_frames)
    if np.mean(np.abs(full_chunk)) < 0.01:
        return

    wav_io = io.BytesIO()
    write(wav_io, samplerate, (full_chunk * 32767).astype(np.int16))
    wav_io.seek(0)

    segments, _ = whisper_model.transcribe(
        wav_io,
        vad_filter=True,
        vad_parameters={"threshold": 0.6, "min_silence_duration_ms": 300}
    )
    for segment in segments:
        text = segment.text.strip()
        if text and len(text.split()) >= 5 and segment.avg_logprob > -0.5:
            speaker = identify_speaker(audio_frames)
            log_transcript(speaker, text)

def audio_thread():
    buffer = []
    while True:
        try:
            with sd.RawInputStream(samplerate=samplerate, blocksize=blocksize,
                                   device=device, dtype='int16', channels=1,
                                   callback=callback):
                while True:
                    data = q.get()
                    audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                    buffer.append(audio_np)

                    if len(buffer) >= 6:
                        executor.submit(process_chunk, buffer[-6:])
                        buffer = buffer[-2:]
        except Exception as e:
            print(f"[❌ Audio Thread Error] {e}")
            time.sleep(3)

def periodic_writer():
    while True:
        try:
            time.sleep(5)
            with transcript_lock:
                if write_buffer:
                    with open(speaker_transcript_path, "a", encoding="utf-8") as f1, \
                         open(plain_transcript_path, "a", encoding="utf-8") as f2:
                        for speaker_line, plain_line in write_buffer:
                            f1.write(speaker_line + "\n")
                            f2.write(plain_line + "\n")
                    write_buffer.clear()
        except Exception as e:
            print(f"[❌ Writer Thread Error] {e}")

def start_background_tasks():
    threading.Thread(target=audio_thread, daemon=True).start()
    threading.Thread(target=periodic_writer, daemon=True).start()

# === FLASK SERVER ===
app = Flask(__name__)
CORS(app)

@app.route("/transcript")
def get_transcript():
    mode = request.args.get("mode", "plain")
    with transcript_lock:
        if mode == "plain":
            return jsonify(list(transcript_lines_plain))
        elif mode == "speaker":
            return jsonify(list(transcript_lines_speaker))
        else:
            return jsonify([])

@app.route("/status")
def status():
    with transcript_lock:
        return jsonify({
            "known_speakers": list(known_speakers.keys()),
            "total_lines_speaker": len(transcript_lines_speaker),
            "total_lines_plain": len(transcript_lines_plain),
            "write_buffer_size": len(write_buffer),
            "queue_size": q.qsize(),
            "active_threads": threading.active_count()
        })

@app.route("/")
def index():
    return jsonify({"message": "API is running. Use /transcript and /status endpoints."})

def run_flask_server():
    app.run(debug=False, host="0.0.0.0", port=9575, use_reloader=False)

# === ENTRY POINT ===
if __name__ == "__main__":
    mode = os.environ.get("RUN_MODE", "standalone").lower()

    print(f"🔧 Running in {mode.upper()} mode...")

    start_background_tasks()

    if mode == "server":
        run_flask_server()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Exiting on Ctrl+C.")
