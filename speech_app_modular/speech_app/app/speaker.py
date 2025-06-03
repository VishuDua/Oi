from resemblyzer import preprocess_wav
import numpy as np
from sklearn.cluster import DBSCAN
from app.models import encoder
from app.config import MAX_SPEAKERS, SAMPLERATE

embedding_history = []

def identify_speaker(audio_frames, known_speakers):
    wav = preprocess_wav(np.concatenate(audio_frames), source_sr=SAMPLERATE)
    if np.mean(np.abs(wav)) < 0.01:
        return "Unknown"

    embedding = encoder.embed_utterance(wav)
    embedding_history.append(embedding)

    if len(embedding_history) < 5:
        return "Unknown"

    clustering = DBSCAN(eps=0.4, min_samples=5).fit(embedding_history)
    label = clustering.labels_[-1]

    identity = f"Speaker_{label + 1}" if label >= 0 else "Unknown"
    if identity not in known_speakers and len(known_speakers) < MAX_SPEAKERS:
        known_speakers[identity] = embedding
    return identity
