import os, torch, time, requests, sys
from datetime import datetime
from llama_cpp import Llama
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import Flask, request, jsonify
from queue import Queue
import threading

# === CONFIG ===
MODEL_PATH = "/mnt/d/WSL/Ubuntu/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf"
TRANSCRIPT_API = "http://localhost:9575/transcript?mode=plain"
TRANSCRIPT_DIR = "/mnt/d/Data_Files/Transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ai_conversation_path = os.path.join(TRANSCRIPT_DIR, f"ai_responses_{timestamp_str}.txt")

# === LOAD MODELS ===
print("🔄 Loading LLM...")
llm = Llama(model_path=MODEL_PATH, n_gpu_layers=32, n_ctx=12288, n_batch=128, use_mmap=True, use_mlock=True)
print("✅ LLM loaded.")

emotion_model_name = "monologg/bert-base-cased-goemotions-original"
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)
labels_url = "https://raw.githubusercontent.com/google-research/google-research/master/goemotions/data/emotions.txt"
emotion_labels = requests.get(labels_url).text.strip().split("\n")

# === STATE ===
chat_history = []
last_seen_line = ""
mode = "text"
q = Queue()
app = Flask(__name__)

# === EMOTION ===
def detect_emotions(text, threshold=0.3):
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = emotion_model(**inputs).logits
        probs = torch.sigmoid(logits)[0]
    detected = [(emotion_labels[i], probs[i].item()) for i in range(len(probs)) if probs[i] > threshold]
    detected.sort(key=lambda x: x[1], reverse=True)
    return [e[0] for e in detected] if detected else ["neutral"]

# === AI RESPONSE ===
def generate_response(user_input):
    emotions = detect_emotions(user_input)
    emotion_str = ", ".join(emotions)
    chat_history.append(f"User: {user_input}")
    history_text = "\n".join(chat_history)
    prompt = f"""### Instruction:
You are a helpful, emotionally intelligent AI assistant. Adjust your tone to fit the user's emotion(s): {emotion_str}.

{history_text}
AI Assistant:"""
    result = llm(prompt, max_tokens=512, temperature=0.8, top_p=0.9, repeat_penalty=1.1)
    ai_response = result["choices"][0]["text"].strip()
    chat_history.append(f"AI: {ai_response}")
    return f"(Detected Emotion: {emotion_str})\n{ai_response}"

# === LOGGING ===
def log_to_file(user_input, ai_response):
    with open(ai_conversation_path, "a", encoding="utf-8") as f:
        f.write(f"[User] {user_input}\n[AI] {ai_response}\n\n")

# === SAFE INPUT (for subprocess-aware fallback) ===
def safe_input(prompt):
    if sys.stdin and sys.stdin.isatty():
        return input(prompt)
    return ""

# === FLASK ===
@app.route("/toggle_mode", methods=["POST"])
def toggle_mode():
    global mode
    mode = "voice" if mode == "text" else "text"
    return jsonify({"mode": mode})

@app.route("/respond", methods=["POST"])
def respond_to_input():
    global last_seen_line
    data = request.get_json()
    user_input = data.get("input", "")

    if mode == "voice":
        try:
            res = requests.get(TRANSCRIPT_API, timeout=3)
            lines = res.json()
            if lines and lines[-1] != last_seen_line:
                last_seen_line = lines[-1]
                user_input = last_seen_line.split("] ", 1)[-1]
            else:
                return jsonify({"response": None})
        except Exception as e:
            return jsonify({"response": f"[Transcript fetch error] {str(e)}"})

    ai_response = generate_response(user_input)
    log_to_file(user_input, ai_response)
    return jsonify({"response": ai_response})

# === TRANSCRIPT POLLING ===
def poll_transcript():
    global last_seen_line
    while True:
        if mode == "voice":
            try:
                res = requests.get(TRANSCRIPT_API, timeout=3)
                lines = res.json()
                if lines and lines[-1] != last_seen_line:
                    last_seen_line = lines[-1]
                    user_input = last_seen_line.split("] ", 1)[-1]
                else:
                    user_input = safe_input("🧑 You (manual input): ").strip()
                    if not user_input:
                        time.sleep(1)
                        continue
                ai_response = generate_response(user_input)
                log_to_file(user_input, ai_response)
                print(f"\n👤 {user_input}\n🤖 {ai_response}\n")
            except Exception as e:
                print(f"[❌ Transcript Error] {e}")
                user_input = safe_input("🎤 STT unavailable. Type your input: ").strip()
                if not user_input:
                    time.sleep(1)
                    continue
                ai_response = generate_response(user_input)
                log_to_file(user_input, ai_response)
                print(f"\n👤 {user_input}\n🤖 {ai_response}\n")
        time.sleep(3)

# === START FUNCTIONS ===
def start_polling():
    threading.Thread(target=poll_transcript, daemon=True).start()

def launch_standalone():
    print("🧠 AI Assistant running in STANDALONE mode...")
    start_polling()
    app.run(debug=False, host="0.0.0.0", port=8989, use_reloader=False)

# === MAIN ===
if __name__ == "__main__":
    launch_standalone()
