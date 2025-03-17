import subprocess
import time
import os
import sys
from datetime import datetime
import requests
import json
import threading

# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyDEwn99vtbn8WB-KBzecRawG1lBi3dW09w"  # Your API key in quotes

def timestamp():
    """Returns the current timestamp in the format YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_process_running(process_name):
    """Checks if a process with the given name (or part of it) is running."""
    try:
        if sys.platform.startswith('win'):
            # Windows (More specific check)
            tasklist_output = subprocess.check_output(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FI', f'WINDOWTITLE eq {process_name}*'], text=True)
            return process_name in tasklist_output
        else:
            # Linux/macOS
            pgrep_output = subprocess.check_output(['pgrep', '-f', process_name], text=True)
            return True if pgrep_output.strip() else False
    except subprocess.CalledProcessError:
        return False

def kill_process(process_name):
    """Kills all processes matching the given name."""
    print(f"{timestamp()} - Killing processes matching '{process_name}'...")
    try:
        if sys.platform.startswith('win'):
            # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/FI', f'WINDOWTITLE eq {process_name}*'], check=False)
        else:
            # Linux/macOS
            subprocess.run(['pkill', '-f', process_name], check=False)
    except Exception as e:
        print(f"{timestamp()} - Error killing '{process_name}': {e}")

def progress_bar(duration):
    """Displays a simple text-based progress bar."""
    columns = 50  # Approximate console width
    fill_char = '#'
    empty_char = '-'
    print("\nStarting initial processes:")
    for i in range(duration + 1):
        percent = (i / duration) * 100
        filled_length = int(round(columns * i / duration))
        bar = fill_char * filled_length + empty_char * (columns - filled_length)
        print(f"\r[{bar}] {percent:.0f}%", end="", flush=True)
        time.sleep(1)
    print("\nInitial processes complete.\n")

def query_gemini(prompt):
    """Queries the Gemini API with the given prompt."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        error_msg = f"{timestamp()} - Error querying Gemini API: {e}"
        print(error_msg)
        print(f"{timestamp()} -   URL: {url}")
        print(f"{timestamp()} -   Headers: {headers}")
        print(f"{timestamp()} -   Data: {json.dumps(data)}")
        print(f"{timestamp()} -   Status Code: {response.status_code if 'response' in locals() else 'N/A'}")
        print(f"{timestamp()} -   Response Text: {response.text if 'response' in locals() else 'N/A'}")
        with open("run_all_windows.log", "a") as f:
            f.write(error_msg + "\n")
        return None

# Define script stages and their duration in seconds
STAGE_KILL_DURATION = 5
STAGE_START_GUI_DELAY = 2  # Delay before starting GUI
STAGE_GEMINI_TEST_DURATION = 5
TOTAL_DURATION = STAGE_KILL_DURATION + STAGE_START_GUI_DELAY + STAGE_GEMINI_TEST_DURATION

# Kill related programs
processes_to_kill = ["Xvfb :99", "website_monitor.py", "BitPredictor.py", "webserver.py", "PriceUpdater.py", "Xvfb", "aipred_cli.py", "python aipred_cli.py"]
print(f"{timestamp()} - Checking and killing related programs...")
for proc in processes_to_kill:
    if is_process_running(proc):
        kill_process(proc)
        time.sleep(2)
print(f"{timestamp()} - All related programs checked and killed (if running)")
print()

# Start progress bar for the initial processes in a separate thread
progress_thread = threading.Thread(target=progress_bar, args=(TOTAL_DURATION,))
progress_thread.start()

CURRENT_PROGRESS = 0
time.sleep(STAGE_KILL_DURATION)
CURRENT_PROGRESS += STAGE_KILL_DURATION

# Stage: Small delay before starting the GUI
print(f"{timestamp()} - Waiting {STAGE_START_GUI_DELAY} seconds before starting aipred_cli.py...")
time.sleep(STAGE_START_GUI_DELAY)
print(f"{timestamp()} - Starting aipred_cli.py...")
cli_process = None
try:
    # Get the absolute path to aipred_cli.py
    cli_path = os.path.abspath("aipred_cli.py")

    # Check if the file exists
    if not os.path.exists(cli_path):
        error_msg = f"{timestamp()} - Error: aipred_cli.py not found at path: {gui_path}"
        print(error_msg)
        with open("run_all_windows.log", "a") as f:
            f.write(error_msg + "\n")
        sys.exit(1)

    # Start aipred_cli.py using the full path
    if sys.platform.startswith('win'):
        cli_process = subprocess.Popen(['python', cli_path])
    else:
        # You might need to adapt this for Linux
        cli_process = subprocess.Popen(['python', cli_path])

    print(f"{timestamp()} - aipred_cli.py started successfully (PID: {cli_process.pid if cli_process else 'N/A'})")

except FileNotFoundError:
    error_msg = f"{timestamp()} - Error: Python executable not found."
    print(error_msg)
    with open("run_all_windows.log", "a") as f:
        f.write(error_msg + "\n")
    sys.exit(1)
except Exception as e:
    error_msg = f"{timestamp()} - Error starting aipred_cli.py: {e}"
    print(error_msg)
    with open("run_all_windows.log", "a") as f:
        f.write(error_msg + "\n")
    sys.exit(1)

# Stage: Attempting to connect to Gemini API (Example)
print(f"{timestamp()} - Performing initial Gemini API connection test...")
example_prompt = "Say hello."
gemini_response = query_gemini(example_prompt)

if gemini_response:
    print(f"{timestamp()} - Initial Gemini API connection test successful. Response: {gemini_response.strip()}")
else:
    print(f"{timestamp()} - Initial Gemini API connection test failed. Check logs for errors.")

time.sleep(STAGE_GEMINI_TEST_DURATION)
CURRENT_PROGRESS += STAGE_GEMINI_TEST_DURATION

# Wait for the progress bar thread to finish
progress_thread.join()

print(f"{timestamp()} - Initial processes completed. The aipred_cli.py GUI is now fully ready.")