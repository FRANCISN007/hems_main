import os
import sys
import time
import subprocess
import requests
import shutil
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_base_path():
    """Return the base path, adjusting for PyInstaller's bundling."""
    return sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd()

BASE_PATH = get_base_path()
app_executable = sys.executable

print(f"[INFO] Using Executable: {app_executable}")
print(f"[INFO] Base Path: {BASE_PATH}")

# Create a safer temporary directory for the backend
BACKEND_TEMP_PATH = os.path.join(tempfile.gettempdir(), "backend_temp")

def setup_backend_temp():
    """Copy backend files to a separate temporary directory to avoid locks."""
    if os.path.exists(BACKEND_TEMP_PATH):
        for root, dirs, files in os.walk(BACKEND_TEMP_PATH, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)  # Try deleting files first
                except Exception as e:
                    print(f"[WARNING] Could not delete {file_path}: {e}")

        try:
            shutil.rmtree(BACKEND_TEMP_PATH)  # Remove old temp backend if exists
        except Exception as e:
            print(f"[ERROR] Failed to remove backend temp directory: {e}")
            time.sleep(2)
            try:
                shutil.rmtree(BACKEND_TEMP_PATH)
            except Exception as e:
                print(f"[CRITICAL] Could not remove backend temp even after retrying: {e}")
                sys.exit(1)

    shutil.copytree(os.path.join(BASE_PATH, "app"), os.path.join(BACKEND_TEMP_PATH, "app"))
    print(f"[INFO] Copied backend to: {BACKEND_TEMP_PATH}")

    # Add the temp directory to `sys.path` so FastAPI can find `app`
    sys.path.insert(0, BACKEND_TEMP_PATH)

def kill_existing_uvicorn():
    """Kill any process using port 8000 to free it up for the backend."""
    try:
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if ":8000" in line:
                pid = line.strip().split()[-1]
                if pid.isdigit():
                    print(f"[INFO] Terminating existing process on port 8000 (PID: {pid})")
                    subprocess.run(["taskkill", "/PID", pid, "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[WARNING] Failed to check running processes: {e}")

def start_backend():
    """Start the FastAPI backend server."""
    backend_path = os.path.join(BACKEND_TEMP_PATH, "app", "main.py")

    if not os.path.exists(backend_path):
        print(f"[ERROR] Backend script not found: {backend_path}")
        sys.exit(1)

    print(f"[INFO] Starting Backend from Temp: {backend_path}")

    backend_process = subprocess.Popen(
        [app_executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=BACKEND_TEMP_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return backend_process

def is_backend_running():
    """Check if the backend is running."""
    for attempt in range(20):
        try:
            response = requests.get("http://127.0.0.1:8000/docs", timeout=3)
            if response.status_code == 200:
                print("[SUCCESS] Backend is running!")
                return True
        except requests.ConnectionError:
            time.sleep(1)

    print("[ERROR] Backend failed to start. Exiting...")
    return False

def start_frontend():
    """Start the Tkinter frontend."""
    frontend_path = os.path.join(BASE_PATH, "frontend", "main.py")

    if not os.path.exists(frontend_path):
        print(f"[ERROR] Frontend script not found: {frontend_path}")
        sys.exit(1)

    print(f"[INFO] Launching Frontend: {frontend_path}")
    subprocess.run([app_executable, frontend_path])  # Removed `shell=True` for better PowerShell compatibility

# Set up backend in a separate temp directory
setup_backend_temp()

# Kill existing uvicorn processes on port 8000
kill_existing_uvicorn()

# Start Backend
backend_process = start_backend()

# Check Backend Logs for Errors
for _ in range(5):
    if backend_process.poll() is not None:
        stdout, stderr = backend_process.communicate()
        print("[ERROR] Backend failed to start.")
        print("[STDOUT]:", stdout)
        print("[STDERR]:", stderr)
        sys.exit(1)
    time.sleep(1)

# Proceed if Backend is Running
if is_backend_running():
    start_frontend()
else:
    print("[ERROR] Backend failed to start. Check logs for details.")
    backend_process.terminate()
    sys.exit(1)

# Ensure Backend is Killed Before Exiting
backend_process.terminate()
backend_process.wait()

# Force Cleanup of PyInstaller Temporary Directory
if getattr(sys, 'frozen', False):
    try:
        shutil.rmtree(BASE_PATH, ignore_errors=True)
        print(f"[INFO] Cleaned up temporary directory: {BASE_PATH}")
    except Exception as e:
        print(f"[WARNING] Failed to remove temporary directory: {e}")

sys.exit(0)
