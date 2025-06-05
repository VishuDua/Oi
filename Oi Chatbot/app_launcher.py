import os
import sys
import subprocess
import platform
import time
import signal
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional

class AppLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.processes = {}
        self.setup_environment()

    def setup_environment(self):
        """Set up the environment configuration for all apps."""
        self.app_configs = {
            "speech_app": {
                "env_name": "speech_env",
                "script_path": self.base_dir / "speech_app" / "app.py",
                "requirements": self.base_dir / "speech_app" / "requirements.txt",
                "port": 5001,
                "url": "http://localhost:5001"
            },
            "text_gen": {
                "env_name": "text_gen_env",
                "script_path": self.base_dir / "text_gen" / "app.py",
                "requirements": self.base_dir / "text_gen" / "requirements.txt",
                "port": 5002,
                "url": "http://localhost:5002"
            },
            "tts_app": {
                "env_name": "tts_env",
                "script_path": self.base_dir / "tts_app" / "app.py",
                "requirements": self.base_dir / "tts_app" / "requirements.txt",
                "port": 5003,
                "url": "http://localhost:5003"
            }
        }

    def create_virtualenv(self, env_name: str, requirements: Path) -> str:
        """Create a virtual environment and install requirements."""
        env_path = self.base_dir / "envs" / env_name
        python_exec = "python" if platform.system() == "Windows" else "python3"
        
        # Create envs directory if it doesn't exist
        (self.base_dir / "envs").mkdir(exist_ok=True)
        
        # Create virtual environment if it doesn't exist
        if not (env_path / "Scripts" / "python.exe").exists() and not (env_path / "bin" / "python").exists():
            print(f"Creating virtual environment for {env_name}...")
            subprocess.run([python_exec, "-m", "venv", str(env_path)], check=True)
            print(f"Virtual environment created at {env_path}")
        
        # Install requirements if they exist
        if requirements.exists():
            print(f"Installing requirements for {env_name}...")
            pip_cmd = [
                str(env_path / ("Scripts" if platform.system() == "Windows" else "bin") / "pip"),
                "install", "-r", str(requirements)
            ]
            subprocess.run(pip_cmd, check=True)
        
        # Return the path to the Python executable
        if platform.system() == "Windows":
            return str(env_path / "Scripts" / "python.exe")
        else:
            return str(env_path / "bin" / "python")

    def start_app(self, app_name: str) -> bool:
        """Start a single application in its own virtual environment."""
        if app_name not in self.app_configs:
            print(f"Unknown application: {app_name}")
            return False
            
        config = self.app_configs[app_name]
        
        # Check if app is already running
        if app_name in self.processes:
            print(f"{app_name} is already running!")
            return True
        
        try:
            # Create virtual environment if needed
            python_path = self.create_virtualenv(
                config["env_name"], 
                config["requirements"]
            )
            
            # Start the application
            print(f"Starting {app_name}...")
            process = subprocess.Popen(
                [python_path, str(config["script_path"])],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == "Windows" else 0
            )
            
            self.processes[app_name] = {
                "process": process,
                "url": config["url"]
            }
            print(f"{app_name} started (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"Failed to start {app_name}: {e}")
            return False

    def stop_app(self, app_name: str):
        """Stop a running application."""
        if app_name not in self.processes:
            print(f"{app_name} is not running.")
            return
            
        try:
            process = self.processes[app_name]["process"]
            if platform.system() == "Windows":
                import ctypes
                ctypes.windll.kernel32.GenerateConsoleCtrlEvent(1, process.pid)
            else:
                process.terminate()
            
            process.wait(timeout=5)
            print(f"{app_name} stopped.")
            
        except Exception as e:
            print(f"Error stopping {app_name}: {e}")
        finally:
            self.processes.pop(app_name, None)

    def start_all(self):
        """Start all applications."""
        print("Starting all applications...")
        for app_name in self.app_configs:
            self.start_app(app_name)
            time.sleep(2)  # Give each app time to start
        
        print("\nAll applications started!")
        self.list_status()
        print("\nAccess the applications at:")
        for app_name, info in self.processes.items():
            print(f"{app_name}: {info['url']}")

    def stop_all(self):
        """Stop all running applications."""
        print("Stopping all applications...")
        for app_name in list(self.processes.keys()):
            self.stop_app(app_name)
        print("All applications stopped.")

    def list_status(self):
        """List status of all applications."""
        print("\nApplication Status:")
        print("-" * 50)
        for app_name, config in self.app_configs.items():
            status = "RUNNING" if app_name in self.processes else "STOPPED"
            pid = self.processes[app_name]["process"].pid if app_name in self.processes else "N/A"
            print(f"{app_name.upper():<12} | {status:<10} | PID: {pid:<8} | {config['url']}")

    def open_in_browser(self, app_name: str):
        """Open the application in the default web browser."""
        if app_name not in self.processes:
            print(f"{app_name} is not running.")
            return
            
        url = self.processes[app_name]["url"]
        print(f"Opening {app_name} at {url}")
        webbrowser.open(url)

def print_menu(launcher):
    """Display the interactive menu."""
    print("\n" + "="*50)
    print("Oi Chatbot Server Manager".center(50))
    print("="*50)
    
    # Display server status
    print("\n[Current Status]")
    launcher.list_status()
    
    # Display menu options
    print("\n[Menu Options]")
    print("1. Start/Stop Speech App")
    print("2. Start/Stop Text Generation")
    print("3. Start/Stop TTS App")
    print("4. Start All Servers")
    print("5. Stop All Servers")
    print("6. Open in Browser")
    print("7. Refresh Status")
    print("8. Exit")
    
    # Get user choice
    try:
        choice = input("\nEnter your choice (1-8): ").strip()
        return choice
    except (KeyboardInterrupt, EOFError):
        return '8'

def handle_choice(choice, launcher):
    """Handle user's menu choice."""
    app_map = {
        '1': 'speech_app',
        '2': 'text_gen',
        '3': 'tts_app'
    }
    
    try:
        if choice in app_map:
            app_name = app_map[choice]
            if app_name in launcher.processes:
                print(f"\n{'*'*20}\nStopping {app_name}...\n{'*'*20}")
                launcher.stop_app(app_name)
            else:
                print(f"\n{'*'*20}\nStarting {app_name}...\n{'*'*20}")
                launcher.start_app(app_name)
        elif choice == '4':
            print("\n" + "*"*20 + "\nStarting all servers...\n" + "*"*20)
            launcher.start_all()
        elif choice == '5':
            print("\n" + "*"*20 + "\nStopping all servers...\n" + "*"*20)
            launcher.stop_all()
        elif choice == '6':
            print("\nOpen which app in browser?")
            print("1. Speech App")
            print("2. Text Generation")
            print("3. TTS App")
            browser_choice = input("Enter choice (1-3): ").strip()
            if browser_choice in app_map:
                launcher.open_in_browser(app_map[browser_choice])
            else:
                print("Invalid choice!")
        elif choice == '7':
            pass  # Just refresh the status
        elif choice == '8':
            print("\nExiting...")
            launcher.stop_all()
            return False
        else:
            print("\nInvalid choice! Please try again.")
            input("Press Enter to continue...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to continue...")
    
    return True

def print_help():
    """Print help information."""
    print("\nOi Chatbot Application Launcher")
    print("=" * 50)
    print("Interactive Menu Controls:")
    print("1-3: Toggle Start/Stop for Speech/Text/TTS")
    print("4: Start All Servers")
    print("5: Stop All Servers")
    print("6: Open in Browser")
    print("7: Refresh Status")
    print("8: Exit")

def main():
    launcher = AppLauncher()
    
    # Handle command line arguments for non-interactive mode
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        app_name = sys.argv[2].lower() if len(sys.argv) > 2 else ""
        
        if command == "start" and app_name:
            launcher.start_app(app_name)
        elif command == "stop" and app_name:
            launcher.stop_app(app_name)
        elif command == "startall":
            launcher.start_all()
        elif command == "stopall":
            launcher.stop_all()
        elif command == "status":
            launcher.list_status()
        elif command == "open" and app_name:
            launcher.open_in_browser(app_name)
        elif command == "help":
            print_help()
        else:
            print("Invalid command. Use 'python app_launcher.py help' for available commands.")
        return
    
    # Interactive menu mode
    print("\n" + "="*50)
    print("Oi Chatbot Server Manager".center(50))
    print("="*50)
    print("Interactive menu mode. Select an option below:")
    
    try:
        while True:
            choice = print_menu(launcher)
            if not handle_choice(choice, launcher):
                break
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Stopping all servers...")
        launcher.stop_all()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        launcher.stop_all()

if __name__ == "__main__":
    main()
