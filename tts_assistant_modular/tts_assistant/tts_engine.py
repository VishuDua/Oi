import logging
import numpy as np
import sounddevice as sd
from TTS.api import TTS
from .config import DEFAULT_SAMPLE_RATE

def load_tts_model():
    try:
        logging.info("🔄 Loading TTS model (Jenny)...")
        return TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=True)
    except Exception as e:
        logging.error(f"[❌ TTS Model Load Failed] {e}")
        return None

tts = load_tts_model()

def speak(text, sample_rate=DEFAULT_SAMPLE_RATE):
    if not tts:
        logging.warning("[⚠️ TTS not available]")
        return
    if not text:
        logging.warning("[⚠️ Empty text received for TTS]")
        return
    try:
        logging.info("🔊 Speaking response...")
        wav = np.array(tts.tts(text), dtype=np.float32)
        sd.play(wav, samplerate=int(sample_rate), blocking=False)
    except Exception as e:
        logging.error(f"[❌ TTS Error] {e}")
