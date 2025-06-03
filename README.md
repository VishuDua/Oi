# Oi Voice Assistant

## Overview

The **Oi Voice Assistant** is a fully integrated, modular AI system built for real-time, speech-based interaction. It combines Speech-to-Text (STT), Language Modeling (LLM), and Text-to-Speech (TTS) technologies to deliver emotionally intelligent, context-aware conversations. Designed for use in smart assistants, customer service bots, and NLP research, this suite leverages multi-threading and GPU-accelerated models for high performance.

The assistant is composed of four primary modules:

1. **Speech-to-Text (STT)** – Transcribes speech in real-time and detects unique speakers.
2. **Text Generation (LLM)** – Generates intelligent, emotional context-aware responses using Mistral-7B-Instruct.
3. **Text-to-Speech (TTS)** – Synthesizes high-quality speech from AI responses using Jenny TTS.
4. **Controller** – Manages subprocesses, synchronizes components, and handles runtime stability.

---

## Features

### 🔊 Speech-to-Text (STT)

* Real-time transcription using **FasterWhisper**.
* **Speaker Identification** using **Resemblyzer** voice embeddings.
* Multithreaded audio stream processing with `sounddevice`.
* Persistent transcript logging with optional API exposure.

### 🧠 Text Generation (LLM)

* Context-aware responses using **Mistral-7B-Instruct** via **llama-cpp**.
* Emotion detection via **GoEmotions** BERT-based classifier.
* Response tone adapts to detected emotions (e.g., supportive if sadness is detected).
* Built on **FastAPI** with async support and concurrency.
* Conversation memory using `deque` to maintain history.

### 🎧 Text-to-Speech (TTS)

* Voice synthesis using **Jenny TTS** (`coqui.ai`).
* Cleaned, emotion-filtered responses passed to the TTS engine.
* Non-blocking audio playback using `sounddevice`.
* Adjustable sample rate for audio fidelity.

### 🔗 Controller Module

* Centralized startup and monitoring of STT, LLM, and TTS modules.
* Uses Python subprocess and environment isolation.
* Logs output and manages crash recovery.
* Toggling between voice and text mode supported via API.

 ### 💻 Web Frontend
Built with Vite + Tailwind CSS for fast performance

Responsive design for real-time user input and output

Connects to backend /respond API for conversational flow

Displays AI replies and logs them in the interface

---

## Installation

### 1. Prerequisites

* Python 3.8 or higher
* (Optional) GPU support for better performance

### 2. Dependency Installation

```bash
pip install -r requirements.txt
```

### 3. Model Setup

* Place **Mistral-7B-Instruct GGUF model** in the correct directory.
* Ensure **Whisper**, **Jenny TTS**, and **Resemblyzer** are installed and working.
* Internet connection required to fetch emotion labels for GoEmotions.

### 4. Configuration

Update paths in `assistant_controller.py`:

```python
STT_ENV = "path_to_stt_venv/bin/python"
TEXT_GEN_ENV = "path_to_text_gen_venv/bin/python"
TTS_ENV = "path_to_tts_venv/bin/python"
```

---

## Usage

### 🚀 Running the Full Suite

```bash
python assistant_controller.py
```

This initializes:

* STT (real-time voice transcription)
* LLM (response generation)
* TTS (voice synthesis)
* Controller (synchronization)

### 📡 API Endpoints (via FastAPI)

| Endpoint                   | Description                                         |
| -------------------------- | --------------------------------------------------- |
| `/respond`                 | Generate AI response from text or last spoken input |
| `/toggle_mode`             | Toggle between voice and text input modes           |
| `/transcript?mode=plain`   | Get raw transcripts                                 |
| `/transcript?mode=speaker` | Get transcripts with speaker attribution            |
| `/`                        | Confirm server status                               |

---

## Technologies Used

* **Python 3.8+**
* **FastAPI** (API backend)
* **Torch, Transformers** (emotion classification)
* **llama-cpp-python** (Mistral LLM)
* **Jenny TTS** (TTS synthesis)
* **FasterWhisper** (real-time STT)
* **Resemblyzer** (speaker identification)
* **NumPy**, **SoundDevice** (audio handling)
* **Concurrent.futures**, **Threading**, **Subprocess** (parallel execution)

---

## Contributing

We welcome contributions:

* Fork the repository and submit PRs for features or bug fixes.
* Report bugs or suggest enhancements via GitHub Issues.
* Help optimize model integration or extend functionality.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
