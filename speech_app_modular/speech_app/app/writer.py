import threading
from collections import deque
from app.config import SPEAKER_TRANSCRIPT_PATH, PLAIN_TRANSCRIPT_PATH

transcript_lines_speaker = deque(maxlen=10000)
transcript_lines_plain = deque(maxlen=10000)
write_buffer = []
lock = threading.Lock()

def log_transcript(speaker, text):
    from datetime import datetime
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {speaker}: {text}"
    print(line)
    with lock:
        transcript_lines_speaker.append(line)
        transcript_lines_plain.append(text)
        write_buffer.append((line, text))

def writer_thread():
    import time
    while True:
        time.sleep(5)
        with lock:
            if write_buffer:
                with open(SPEAKER_TRANSCRIPT_PATH, "a") as f1, open(PLAIN_TRANSCRIPT_PATH, "a") as f2:
                    for s, p in write_buffer:
                        f1.write(s + "\n")
                        f2.write(p + "\n")
                write_buffer.clear()
