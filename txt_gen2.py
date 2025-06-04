import os, torch, time, requests
from datetime import datetime
from llama_cpp import Llama
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections import deque
import asyncio
import concurrent.futures  # Added for parallel execution

# === CONFIG ===
MODEL_PATH = "/mnt/d/WSL/Ubuntu/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf"
TRANSCRIPT_API = "http://localhost:9575/transcript?mode=plain"
TRANSCRIPT_DIR = "/mnt/d/Data_Files/Transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ai_conversation_path = os.path.join(TRANSCRIPT_DIR, f"ai_responses_{timestamp_str}.txt")

# === LOAD MODELS WITH OPTIMIZED PARAMETERS ===
print("🔄 Loading LLM...")
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=32,
    n_ctx=8192,
    n_batch=64,
    use_mmap=True,
    use_mlock=True
)
print("✅ LLM loaded.")

emotion_model_name = "monologg/bert-base-cased-goemotions-original"
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)
labels_url = "https://raw.githubusercontent.com/google-research/google-research/master/goemotions/data/emotions.txt"
emotion_labels = requests.get(labels_url).text.strip().split("\n")

# === STATE ===
chat_history = deque(maxlen=50)
last_seen_line = ""
mode = "text"
app = FastAPI()

# === ROOT ENDPOINT FIX ===
@app.get("/")
async def root():
    """Root endpoint for server confirmation."""
    return {"message": "AI Assistant is running! Use /respond for interaction."}

@app.get("/favicon.ico")
async def favicon():
    """Prevents unnecessary 404 errors for favicon requests."""
    return {"message": "No favicon available."}

# === EMOTION DETECTION ===
def detect_emotions(text, threshold=0.4):
    """Detects emotions with refined confidence filtering."""
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = emotion_model(**inputs).logits
        probs = torch.sigmoid(logits)[0]

    detected = [(emotion_labels[i], probs[i].item()) for i in range(len(probs)) if probs[i] > threshold]
    detected.sort(key=lambda x: x[1], reverse=True)

    return [e[0] for e in detected] if detected else ["neutral"]

# === INTENT CLASSIFICATION ===
def classify_intent(user_input):
    """Basic intent classification to guide AI response."""
    intent_map = {
        "summary": ["summarize", "give me a short version"],
        "recommendation": ["suggest", "recommend"],
        "emotion_boost": ["cheer me up", "support"],
        "clarification": ["explain", "what does this mean"],
    }

    for intent, keywords in intent_map.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            return intent
    return "conversation"

# === AI RESPONSE GENERATION WITH PARALLEL PROCESSING ===
def generate_response(user_input):
    """Generates AI response with emotional context-awareness, intent recognition, and parallel execution."""
    emotions = detect_emotions(user_input)
    emotion_str = ", ".join(emotions)
    intent = classify_intent(user_input)

    chat_history.append(f"User: {user_input}")
    history_text = "\n".join(chat_history)

    prompt = f"""### Instruction:
You are a helpful, emotionally intelligent AI assistant. Adjust your tone to fit the user's emotion(s): {emotion_str}.
Recognized user intent: {intent}.

{history_text}
AI Assistant:"""

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(
            llm,
            prompt,
            max_tokens=512,
            temperature=0.55,  # Lowered for controlled responses
            top_p=0.7,
            repeat_penalty=1.1
        )
        result = future.result()

    ai_response = result["choices"][0]["text"].strip()
    chat_history.append(f"AI: {ai_response}")
    return f"(Detected Emotion: {emotion_str})\n{ai_response}"

# === REQUEST MODEL ===
class UserInput(BaseModel):
    input: str

# === API ENDPOINTS ===
@app.post("/toggle_mode")
async def toggle_mode():
    """Switch between text and voice input modes."""
    global mode
    mode = "voice" if mode == "text" else "text"
    return {"mode": mode}

@app.post("/respond")
async def respond_to_input(data: UserInput):
    """Processes user input and returns AI-generated response asynchronously."""
    global last_seen_line
    user_input = data.input

    if mode == "voice":
        try:
            res = requests.get(TRANSCRIPT_API, timeout=2)
            lines = res.json()
            if lines and lines[-1] != last_seen_line:
                last_seen_line = lines[-1]
                user_input = last_seen_line.split("] ", 1)[-1]
            else:
                return {"response": None}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transcript fetch error: {str(e)}")

    ai_response = generate_response(user_input)
    log_to_file(user_input, ai_response)
    return {"response": ai_response}

# === LOGGING ===
def log_to_file(user_input, ai_response):
    """Logs AI interactions for future analysis."""
    with open(ai_conversation_path, "a", encoding="utf-8") as f:
        f.write(f"[User] {user_input}\n[AI] {ai_response}\n\n")

# === EVENT-BASED TRANSCRIPT HANDLING ===
async def poll_transcript():
    """Optimized event-based transcript retrieval instead of fixed intervals."""
    global last_seen_line
    while True:
        try:
            if mode == "voice":
                res = requests.get(TRANSCRIPT_API, timeout=2)
                lines = res.json()

                if lines and lines[-1] != last_seen_line:
                    last_seen_line = lines[-1]
                    user_input = last_seen_line.split("] ", 1)[-1]
                    ai_response = generate_response(user_input)
                    log_to_file(user_input, ai_response)
                    print(f"\n👤 {user_input}\n🤖 {ai_response}\n")
        except Exception as e:
            print(f"[❌ Transcript Error] {e}")

        await asyncio.sleep(1)  # Faster response time with async handling

# === START FUNCTIONS ===
@app.on_event("startup")
async def startup_event():
    """Starts transcript polling when FastAPI server runs."""
    asyncio.create_task(poll_transcript())

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    import uvicorn
    print("🚀 AI Assistant running with FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8989, log_level="info")
