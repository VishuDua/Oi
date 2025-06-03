import requests
import logging
import time
from .config import STT_URL, TIMEOUT_DURATION, MAX_RETRIES

def get_voice_input():
    logging.info("🎤 Listening for voice input...")
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(STT_URL, timeout=TIMEOUT_DURATION)
            if response.status_code == 200:
                transcribed_text = response.json()
                if transcribed_text:
                    return transcribed_text[0].strip()
            logging.warning(f"[❌ STT Error] Code {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.warning(f"[🚨 STT Request Error] Attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            time.sleep(1)
    return "[Failed to recognize speech]"
