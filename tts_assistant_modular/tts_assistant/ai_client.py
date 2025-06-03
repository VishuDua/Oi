import requests
import re
import logging
import time
from .config import AI_URL, TIMEOUT_DURATION, MAX_RETRIES

def get_response_from_server(user_input):
    payload = {"input": user_input}
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(AI_URL, json=payload, timeout=TIMEOUT_DURATION)
            if response.status_code == 200:
                full_reply = response.json().get("response", "[No response]")
                logging.info(f"🤖 Bot Response: {full_reply}")
                return clean_reply(full_reply)
            logging.warning(f"[❌ AI Server Error] Code {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.warning(f"[🚨 AI Request Error] Attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            time.sleep(1)
    return "[Failed to retrieve AI response]"

def clean_reply(text):
    return re.sub(r"\(Detected Emotion:.*?\)", "", text).strip()
