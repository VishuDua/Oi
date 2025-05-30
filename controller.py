import subprocess
import sys
import os
import time

# Paths to your existing scripts
STT_SCRIPT = "stt_script.py"  # Replace with your STT script path
TEXT_GEN_SCRIPT = "text_gen_script.py"  # Replace with your Text Gen script path
TTS_SCRIPT = "tts_script.py"  # Replace with your TTS script path

# Define the paths for your virtual environments (if needed)
STT_ENV = "path_to_stt_venv/bin/python"  # Replace with your STT virtual environment's Python executable
TEXT_GEN_ENV = "path_to_text_gen_venv/bin/python"  # Replace with your Text Gen virtual environment's Python executable
TTS_ENV = "path_to_tts_venv/bin/python"  # Replace with your TTS virtual environment's Python executable

# Function to run each script in a subprocess with the required environment
def run_subprocess(script_path, env_python_path, name):
    try:
        process = subprocess.Popen(
            [env_python_path, script_path],  # Command to run the script
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,  # Capture output and errors
            universal_newlines=True  # Text mode
        )
        print(f"Started {name} subprocess.")
        return process
    except Exception as e:
        print(f"[ERROR] Failed to start {name} subprocess: {e}")
        return None

# Function to monitor the subprocess and capture its output
def monitor_subprocess(process, name):
    try:
        for line in iter(process.stdout.readline, ""):
            print(f"[{name}] {line.strip()}")  # Print the output of each process
        process.stdout.close()
        process.wait()
    except Exception as e:
        print(f"[ERROR] {name} subprocess error: {e}")

# Main function to start the processes
def start_all_processes():
    # Start the STT subprocess
    stt_process = run_subprocess(STT_SCRIPT, STT_ENV, "STT")
    if not stt_process:
        return

    # Start the Text Generation subprocess
    text_gen_process = run_subprocess(TEXT_GEN_SCRIPT, TEXT_GEN_ENV, "Text Generation")
    if not text_gen_process:
        return

    # Start the TTS subprocess
    tts_process = run_subprocess(TTS_SCRIPT, TTS_ENV, "TTS")
    if not tts_process:
        return

    # Monitor the subprocesses
    monitor_subprocess(stt_process, "STT")
    monitor_subprocess(text_gen_process, "Text Generation")
    monitor_subprocess(tts_process, "TTS")

# Entry point
if __name__ == "__main__":
    start_all_processes()
