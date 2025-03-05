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

    with open("error.log", "w") as log_file:
        process = subprocess.Popen([PYTHON_EXECUTABLE, "-m", "app.main"], cwd=BASE_DIR)

    return process  # No time.sleep() to avoid blocking execution

def show_welcome_screen():
    """Launch the welcome screen (runs in parallel without blocking)"""
    welcome_script = os.path.join(BASE_DIR, "frontend", "welcome.py")

    if not os.path.exists(welcome_script):
        print(f"Error: Welcome screen script not found at {welcome_script}")
        sys.exit(1)

    subprocess.Popen([PYTHON_EXECUTABLE, welcome_script], cwd=BASE_DIR)  # No time.sleep()
    # Launch welcome screen and WAIT for it to close
    #process = subprocess.Popen([PYTHON_EXECUTABLE, welcome_script], cwd=BASE_DIR)
    #process.wait()  # Wait for the welcome screen to close before proceeding
    time.sleep(2)
    

def start_frontend():
    """Starts the Tkinter frontend using the virtual environment"""
    frontend_script = os.path.join(BASE_DIR, "frontend", "main.py")

    if not os.path.exists(frontend_script):
        print(f"Error: Frontend script not found at {frontend_script}")
        sys.exit(1)

    subprocess.Popen([PYTHON_EXECUTABLE, frontend_script], cwd=BASE_DIR)

if __name__ == "__main__":
    # Step 1: Start Backend First (No Delay)
    backend_process = start_backend()

    # Step 2: Show Welcome Screen (Runs Parallel)
    show_welcome_screen()

    # Step 3: Start Frontend Immediately (No Time Gap)
    
    start_frontend()

    # Step 4: Keep Backend Running in the Background
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        backend_process.terminate()
