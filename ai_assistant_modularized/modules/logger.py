def log_to_file(user_input, ai_response, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[User] {user_input}\n[AI] {ai_response}\n\n")