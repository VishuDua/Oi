def classify_intent(user_input):
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