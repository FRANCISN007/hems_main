import os
import sys
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXECUTABLE = os.path.join(BASE_DIR, "env", "Scripts", "python.exe")  # Ensure correct path

# Check if Python executable exists
if not os.path.exists(PYTHON_EXECUTABLE):
    print(f"Error: Python executable not found at {PYTHON_EXECUTABLE}")
    sys.exit(1)

def start_backend():
    """Starts the FastAPI backend using the virtual environment"""
    backend_script = os.path.join(BASE_DIR, "app", "main.py")

    if not os.path.exists(backend_script):
        print(f"Error: Backend script not found at {backend_script}")
        sys.exit(1)

    #process = subprocess.Popen([PYTHON_EXECUTABLE, "-m", "app.main"], cwd=BASE_DIR)
    with open("error.log", "w") as log_file:
        process = subprocess.Popen([PYTHON_EXECUTABLE, "-m", "app.main"], cwd=BASE_DIR)


    time.sleep(3)  # Wait for backend to start
    return process

def start_frontend():
    """Starts the Tkinter frontend using the virtual environment"""
    frontend_script = os.path.join(BASE_DIR, "frontend", "main.py")

    if not os.path.exists(frontend_script):
        print(f"Error: Frontend script not found at {frontend_script}")
        sys.exit(1)

    subprocess.Popen([PYTHON_EXECUTABLE, frontend_script], cwd=BASE_DIR)

if __name__ == "__main__":
    backend_process = start_backend()
    start_frontend()
    
    # Keep the program running (so backend doesn't close)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        backend_process.terminate()