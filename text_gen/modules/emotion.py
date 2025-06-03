import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests

emotion_model_name = "monologg/bert-base-cased-goemotions-original"
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)
labels_url = "https://raw.githubusercontent.com/google-research/google-research/master/goemotions/data/emotions.txt"
emotion_labels = requests.get(labels_url).text.strip().split("\n")

def detect_emotions(text, threshold=0.4):
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = emotion_model(**inputs).logits
        probs = torch.sigmoid(logits)[0]

    detected = [(emotion_labels[i], probs[i].item()) for i in range(len(probs)) if probs[i] > threshold]
    detected.sort(key=lambda x: x[1], reverse=True)
    return [e[0] for e in detected] if detected else ["neutral"]