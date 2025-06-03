import logging
from tts_assistant.tts_engine import speak
from tts_assistant.input_handler import get_voice_input
from tts_assistant.ai_client import get_response_from_server

if __name__ == "__main__":
    import sounddevice as sd

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        logging.info("🎧 Choose input method: [1] Voice [2] Text")
        choice = input("🔧 Enter choice (1/2): ").strip()

        while True:
            user_input = get_voice_input() if choice == "1" else input("🧠 You: ").strip()

            if user_input.lower() in ("exit", "quit"):
                logging.info("👋 Exiting.")
                break

            if user_input:
                reply = get_response_from_server(user_input)
                if reply:
                    logging.info(f"🤖 Response: {reply}")
                    speak(reply)

    except KeyboardInterrupt:
        logging.info("\n👋 Exiting on Ctrl+C.")
    finally:
        logging.info("🛑 Cleaning up resources...")
        sd.stop()
