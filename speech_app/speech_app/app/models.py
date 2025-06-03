import torch
from resemblyzer import VoiceEncoder
from faster_whisper import WhisperModel

device_type = "cuda" if torch.cuda.is_available() else "cpu"
encoder = VoiceEncoder().to(device_type)
whisper_model = WhisperModel("medium", device=device_type, compute_type="float16" if device_type == "cuda" else "int8")
