import io
import time
import numpy as np
from scipy.io.wavfile import write
from app.models import whisper_model
from app.speaker import identify_speaker
from app.writer import log_transcript

def process_chunk(audio_frames, known_speakers):
    start = time.time()
    full_chunk = np.concatenate(audio_frames)

    if np.mean(np.abs(full_chunk)) < 0.01:
        return

    wav_io = io.BytesIO()
    write(wav_io, 16000, (full_chunk * 32767).astype(np.int16))
    wav_io.seek(0)

    try:
        segments, _ = whisper_model.transcribe(wav_io, vad_filter=True)
        for segment in segments:
            text = segment.text.strip()
            if text:
                speaker = identify_speaker(audio_frames, known_speakers)
                log_transcript(speaker, text)
    except Exception as e:
        print(f"[❌ Whisper Error] {e}")
