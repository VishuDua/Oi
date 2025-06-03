import queue
import sounddevice as sd
import numpy as np
from app.config import SAMPLERATE, BLOCKSIZE

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("[⚠️ Audio Status]", status)
    q.put(bytes(indata))

def start_stream(device, processor):
    buffer = []
    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE, device=device,
                           dtype='int16', channels=1, callback=callback):
        while True:
            data = q.get()
            audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            buffer.append(audio_np)
            if len(buffer) >= 3:
                processor(buffer[-3:])
                buffer = buffer[-1:]
