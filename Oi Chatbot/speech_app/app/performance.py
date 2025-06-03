import psutil
import time

def monitor():
    while True:
        print(f"[📊 CPU]: {psutil.cpu_percent()}% | [💾 RAM]: {psutil.virtual_memory().percent}%")
        time.sleep(5)
