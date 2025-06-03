from llama_cpp import Llama

llm = None

def init_llm():
    global llm
    print("🔄 Loading LLM...")
    MODEL_PATH = "/mnt/d/WSL/Ubuntu/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf"
    llm = Llama(
        model_path=MODEL_PATH,
        n_gpu_layers=32,
        n_ctx=8192,
        n_batch=64,
        use_mmap=True,
        use_mlock=True
    )
    print("✅ LLM loaded.")

def generate_response(user_input, chat_history):
    from modules.emotion import detect_emotions
    from modules.intent import classify_intent

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

    result = llm(prompt, max_tokens=512, temperature=0.55, top_p=0.7, repeat_penalty=1.1)
    ai_response = result["choices"][0]["text"].strip()
    chat_history.append(f"AI: {ai_response}")
    return f"(Detected Emotion: {emotion_str})\n{ai_response}"