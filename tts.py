import requests
from TTS.api import TTS
import re
import sounddevice as sd
import numpy as np

# === Config ===
SERVER_URL = "http://172.27.148.150:8989/"  # 🔁 Server endpoint
SAMPLE_RATE = 56050  # 🎧 Jenny TTS sample rate

# === Load TTS Model ===
try:
    print("🔄 Loading TTS model (Jenny)...")
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=False)
    print("✅ TTS model loaded successfully.")
except Exception as e:
    print(f"[❌ TTS Model Load Failed] {e}")
    tts = None

# === Send Input to Server ===
def get_response_from_server(user_input):
    payload = {"input": user_input}
    try:
        response = requests.post(SERVER_URL + "respond", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            full_reply = data.get("response", "[No response]")
            print("🤖 Bot:", full_reply)
            return clean_reply(full_reply)
        else:
            print(f"[❌ Server Error] Code {response.status_code}")
            print(response.text)
            return "[Failed to get response]"
    except requests.exceptions.Timeout:
        print("[⏱️ Timeout] Server took too long to respond.")
        return "[Timeout]"
    except requests.exceptions.RequestException as e:
        print(f"[🚨 Request Error] {e}")
        return "[Request Failed]"

# === Clean Output for TTS ===
def clean_reply(text):
    text = re.sub(r"\(Detected Emotion:.*?\)", "", text)
    lines = text.strip().splitlines()
    clean_lines = [
        line for line in lines
        if not re.match(r"^\s*(User\s*\d*:|User:|AI Assistant:|AI:|C:/|& C:/|>)", line.strip())
    ]
    return " ".join(clean_lines).strip()

# === Speak Using TTS ===
def speak(text):
    if not tts:
        print("[⚠️ TTS not available]")
        return
    if not text:
        print("[⚠️ Empty text received for TTS]")
        return
    try:
        print("🔊 Speaking...")
        wav = tts.tts(text)
        wav = np.array(wav, dtype=np.float32)
        sd.play(wav, samplerate=SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(f"[❌ TTS Error] {e}")

# === CLI Entry Point ===
if __name__ == "__main__":
    print("🎤 Type your message below. Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("🧠 You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("👋 Exiting.")
                break
            if not user_input:
                continue
            reply = get_response_from_server(user_input)
            speak(reply)
        except KeyboardInterrupt:
            print("\n👋 Exiting on Ctrl+C.")
            break
