Oi Voice Assistant

Overview
The AI Conversational Assistant Suite is a fully integrated, modular system designed for real-time speech interaction and intelligent responses. It combines Speech-to-Text (STT), Text Generation (LLM), and Text-to-Speech (TTS) to deliver seamless AI-driven conversations with emotion-aware contextual replies.
The suite is structured around four key components:
- Speech-to-Text (STT) – Captures and transcribes voice input, identifying speakers dynamically.
- Text Generation (LLM) – Processes user queries and generates intelligent responses using Mistral-7B-Instruct.
- Text-to-Speech (TTS) – Converts AI-generated text responses into high-quality synthesized speech using Jenny TTS.
- Controller Module – Oversees and synchronizes all processes for efficient execution.
This project is ideal for virtual assistants, AI-powered customer service, and research in natural language processing and emotional AI.

Features
🔊 Speech-to-Text (STT)
- Speaker Identification using voice embeddings with Resemblyzer.
- Real-time transcription leveraging Whisper AI for high accuracy.
- Multi-threaded audio processing for optimized performance.
- Automatic data logging for structured transcript management.
🧠 Text Generation (LLM)
- Context-aware responses powered by Mistral-7B-Instruct.
- Emotion detection using GoEmotions BERT model to adjust AI tone dynamically.
- Flask-based API to handle user requests efficiently.
- Interactive conversation memory for better engagement.
🎧 Text-to-Speech (TTS)
- Natural voice synthesis using Jenny TTS for fluid AI speech generation.
- Optimized text cleanup to remove unnecessary characters for TTS readability.
- Customizable sample rate for high-quality audio playback.
- Threaded audio streaming for minimal latency in speech response.
🔗 Controller Module
- Process management for launching STT, LLM, and TTS seamlessly.
- Subprocess monitoring to track real-time output.
- Error handling mechanisms ensuring stability and recovery from failures.
- Virtual environment support for modular execution.

Installation
1️⃣ Prerequisites
Ensure you have Python installed (>=3.8) and that your system supports GPU-based execution (optional but recommended for faster processing).
2️⃣ Dependency Installation
Install all required dependencies using:
pip install -r requirements.txt


3️⃣ Model Setup
- Download and place the Mistral-7B-Instruct model in the designated directory.
- Ensure Whisper AI and Resemblyzer are installed.
- Verify Jenny TTS model availability.
4️⃣ Configuration
Modify the environment paths in the controller script:
STT_ENV = "path_to_stt_venv/bin/python"
TEXT_GEN_ENV = "path_to_text_gen_venv/bin/python"
TTS_ENV = "path_to_tts_venv/bin/python"



Usage
🚀 Launching the AI Assistant
Start all modules with:
python assistant_controller.py


This will:
- Initialize STT to process voice input.
- Trigger LLM for response generation.
- Convert AI replies to speech via TTS.
- Monitor and synchronize processes.
📡 API Endpoints
- /transcript?mode=plain – Fetch a clean transcription.
- /transcript?mode=speaker – Retrieve transcripts with speaker attribution.
- /respond – Generate AI response from user input.
- /toggle_mode – Switch between voice and text interaction modes.
- /status – View system diagnostics (active threads, memory usage, etc.).

Technologies Used
The system is built using state-of-the-art machine learning and audio processing libraries:
- Python 3.8+
- Flask (API framework)
- Torch & Transformers (LLM processing)
- LlamaCpp (Efficient model execution)
- Jenny TTS (Speech synthesis)
- Resemblyzer (Speaker identification)
- Whisper AI (Speech-to-text)
- NumPy (Audio processing)
- SoundDevice (Real-time audio handling)
- Subprocess & Threading (Parallel execution)

Contributing
We welcome contributions! You can:
- Submit pull requests for enhancements or bug fixes.
- Open issues to report bugs or suggest improvements.
- Help optimize model integration for better AI performance.

License
This project is licensed under the MIT License. See LICENSE for more details.
