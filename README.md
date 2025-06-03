# Oi Voice Assistant 🎧🧠🗣️
---

## 🌟 Features

### Backend (Voice Assistant Engine)

* 🔊 **Speech-to-Text** with Whisper + Resemblyzer (Speaker Recognition)
* 🧠 **Text Generation** using Mistral-7B with Emotion Detection
* 🗣️ **Text-to-Speech** using Jenny TTS with audio playback
* 📋 Transcript Logging and Conversation Memory
* 🔄 RESTful APIs for all modules
* 🌿 Emotion-adaptive tone (e.g., supportive if sadness is detected)
* ⏱️ Multithreaded audio and model execution
* 🚀 Real-time voice activity detection

### Frontend (Chat UI)

* 🖥️ **React-based Chat Interface**
* 💬 Typing & Voice input toggling
* 🎙️ Speech-to-text integration (planned)
* ⚡ Fast and responsive design
* 🧪 Mock and real backend support

---

## 🏗️ Folder Structure

```
Oi-Chatbot/
├── src/
│   ├── Speech_to_text/        # Whisper + Resemblyzer
│   │   ├── api.py
│   │   ├── audio.py
│   │   ├── models.py
│   │   ├── speaker.py
│   │   ├── stt.py
│   │   ├── transcript.py
│   │   └── utils.py
│   ├── Text_GEN/              # Mistral + GoEmotions
│   │   ├── data/
│   │   ├── modules/
│   │   ├── transcripts/
│   │   └── text_gen.py
│   └── Text_To_Speech/        # Jenny TTS
│       └── tts.py
├── Mistral/                   # Model files
├── Transcripts/               # Transcripts
├── Requirements.txt           # Main dependencies
├── stt.py                     # STT entry point
├── assistant_controller.py    # Process orchestrator
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/
│       ├── components/
│       ├── assets/
│       ├── App.jsx
│       └── index.js
└── README.md
```

---

## 🔧 Installation & Setup

### 1️⃣ Backend Setup

#### Prerequisites

* Python 3.8+
* (Recommended) CUDA-capable GPU
* Three Virtual Environments (main, text\_gen, tts)

#### Install Main Backend Dependencies

```bash
pip install -r Requirements.txt
```

#### Text Generation venv Setup

```bash
cd src/Text_GEN
python -m venv venv2
source venv2/bin/activate
pip install -r Requirements2.txt
```

#### Text-to-Speech venv Setup

```bash
cd src/Text_To_Speech
python -m venv venv
source venv/bin/activate
pip install TTS
```

#### Model Setup

* Place Mistral-7B GGUF model in `Mistral/`
* Ensure Whisper and Resemblyzer models are available
* Internet required to fetch GoEmotions labels

---

## 🔠 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at [http://localhost:5173](http://localhost:5173)

Update `src/api/openai.js` with:

```js
export async function sendChatMessage(messages) {
  const res = await fetch("http://localhost:8989/respond", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input: messages[messages.length - 1].content })
  });
  const data = await res.json();
  return data.response;
}
```

---

## 🚀 Running the System

### Option A: Individual Modules

```bash
# TTS
python src/Text_To_Speech/tts.py
# STT
python stt.py
# Text Gen
python src/Text_GEN/text_gen.py
# Frontend
npm run dev
```

### Option B: Controller

```bash
python assistant_controller.py
```

Update the paths in `assistant_controller.py`:

```python
STT_ENV = "path_to_stt_venv/bin/python"
TEXT_GEN_ENV = "path_to_text_gen_venv/bin/python"
TTS_ENV = "path_to_tts_venv/bin/python"
```

---

## 📡 API Endpoints

| Endpoint                       | Description                                    |
| ------------------------------ | ---------------------------------------------- |
| `POST /respond`                | Generate AI response from text or spoken input |
| `POST /tts?text=Hello`         | Convert text to speech (Jenny TTS)             |
| `POST /chat?text=Hello`        | Respond and speak                              |
| `GET /transcript?mode=plain`   | Raw transcript log                             |
| `GET /transcript?mode=speaker` | Speaker-attributed transcript                  |
| `/toggle_mode`                 | Toggle between voice/text mode                 |

---

## 🧰 Technologies Used

* **Backend**: Python, FastAPI, Flask, Torch, Transformers
* **Speech**: Faster Whisper, Resemblyzer, SoundDevice
* **LLM**: llama-cpp, Mistral 7B Instruct
* **Emotion**: GoEmotions (BERT-based classifier)
* **Frontend**: React.js, Vite, TailwindCSS

---

## 🚪 Usage Examples

```bash
# Basic TTS
curl -X POST 'http://localhost:6969/tts?text=Hello%20world!'

# Chat with TTS
curl -X POST 'http://localhost:6969/chat?text=How%20are%20you?'
```

---

## 🔧 Troubleshooting

* **Audio Issues**: Check microphone, sounddevice, audio config
* **Model Loading**: Ensure correct model paths, enough RAM/GPU
* **API Errors**: Verify ports and endpoints match

---

## 💪 Contributing

* Fork, clone, and PR your improvements
* Open GitHub issues for bugs and features
* Improve frontend integration or backend performance

---

## 📄 License

MIT License

---

## Credits

* Mistral AI
* Coqui TTS (Jenny Model)
* Hugging Face
* Faster Whisper
* Resemblyzer
* Google GoEmotions
