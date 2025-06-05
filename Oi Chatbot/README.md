# Oi Voice Chatbot Transcriber

A comprehensive voice-enabled chatbot system with real-time transcription, text generation, and text-to-speech capabilities. Built with Python, FastAPI, and React.

## Features

- **Multi-service Architecture**: Modular design with separate services for different functionalities
- **Speech-to-Text**: Real-time transcription with speaker diarization
- **Text Generation**: AI-powered text generation for chatbot responses
- **Text-to-Speech**: Natural-sounding voice synthesis
- **Unified Launcher**: Easy management of all services through a single interface
- **Web-based Interface**: Modern React frontend for interaction
- **RESTful APIs**: Well-documented endpoints for each service

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- FFmpeg (for audio processing)
- Git (for cloning the repository)
- pip (Python package manager)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/VishuDua/Oi-Voice-Chatbot-Transcriber.git
   cd "Oi-Voice-Chatbot-Transcriber\Oi Chatbot"
   ```

2. Run the application launcher:
   ```bash
   python app_launcher.py
   ```

3. Follow the on-screen menu to start/stop services and access their web interfaces.

## Services

The system consists of multiple microservices, each running on its own port:

1. **Speech App (Port 5001)**
   - Handles speech-to-text conversion
   - Real-time transcription with speaker diarization
   - Accessible at: `http://localhost:5001`

2. **Text Generation (Port 5002)**
   - AI-powered text generation for chatbot responses
   - Accessible at: `http://localhost:5002`

3. **Text-to-Speech (Port 5003)**
   - Converts text to natural-sounding speech
   - Accessible at: `http://localhost:5003`

## Manual Setup (Alternative)

If you prefer to run services individually:

1. For each service (speech_app, text_gen, tts_app):
   ```bash
   cd <service_directory>
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # or
   # source venv/bin/activate  # On Unix/macOS
   pip install -r requirements.txt
   uvicorn app:app --reload --host 0.0.0.0 --port <port_number>
   ```

## Frontend Development

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

4. For production build:
   ```bash
   npm run build
   ```

## Configuration

Each service has its own configuration. Create `.env` files in the respective service directories with the following variables:

### Speech App (speech_app/.env)
```env
SECRET_KEY=your-secret-key
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Text Generation (text_gen/.env)
```env
OPENAI_API_KEY=your-openai-api-key
MODEL_NAME=gpt-3.5-turbo
```

### Text-to-Speech (tts_app/.env)
```env
SPEECH_KEY=your-azure-speech-key
SPEECH_REGION=your-azure-region
```

## API Documentation

Each service provides its own API documentation:

1. **Speech App**: `http://localhost:5001/docs`
   - `/api/transcript` - Get current transcript
   - `/api/status` - Service status
   - `/api/health` - Health check

2. **Text Generation**: `http://localhost:5002/docs`
   - `/api/generate` - Generate text
   - `/api/models` - List available models

3. **Text-to-Speech**: `http://localhost:5003/docs`
   - `/api/synthesize` - Convert text to speech
   - `/api/voices` - List available voices

## Project Structure

```
.
├── app_launcher.py          # Main application launcher
├── controller.py            # Service controller script
├── frontend/                # React frontend
│   ├── public/              # Static files
│   └── src/                 # Source files
│       ├── api/             # API client code
│       ├── components/      # Reusable components
│       ├── hooks/           # Custom React hooks
│       ├── pages/           # Page components
│       ├── App.jsx          # Main App component
│       └── main.jsx         # Entry point
│
├── speech_app/             # Speech-to-Text service
│   ├── app/                 # Application code
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
│
├── text_gen/               # Text Generation service
│   ├── app/                 # Application code
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
│
└── tts_app/                # Text-to-Speech service
    ├── app/                 # Application code
    ├── main.py              # FastAPI application
    └── requirements.txt     # Python dependencies
```

## Troubleshooting

- **Port Conflicts**: Ensure no other services are running on ports 5001, 5002, or 5003
- **Dependency Issues**: If you encounter dependency conflicts, try recreating the virtual environments
- **API Keys**: Make sure all required API keys are set in the respective .env files
- **Logs**: Check the console output of each service for detailed error messages

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT
```

## Deployment

### Backend

1. Set up a production server (e.g., Gunicorn with Uvicorn workers):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

2. For production, use a proper ASGI server like Uvicorn with a process manager (e.g., systemd, Supervisor).

### Frontend

1. Build the production version:
   ```bash
   npm run build
   ```

2. Serve the built files using a static file server or a web server like Nginx.

## Troubleshooting

- If you encounter CORS issues, ensure the frontend URL is included in the `CORS_ORIGINS` environment variable.
- For audio device issues, check your system's audio input settings.
- Check the browser's developer console for frontend errors.
- Check the backend logs for server-side errors.

## License

MIT
