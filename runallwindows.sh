import subprocess
import time
import os
import sys
from datetime import datetime

def timestamp():
    """Returns the current timestamp in the format YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_process_running(process_name):
    """Checks if a process with the given name (or part of it) is running."""
    try:
        if sys.platform.startswith('win'):
            # Windows
            tasklist_output = subprocess.check_output(['tasklist'], text=True)
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
            subprocess.run(['taskkill', '/F', '/IM', process_name], check=False)
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
    print("\nStarting progress:")
    for i in range(duration + 1):
        percent = (i / duration) * 100
        filled_length = int(round(columns * i / duration))
        bar = fill_char * filled_length + empty_char * (columns - filled_length)
        print(f"\r[{bar}] {percent:.0f}%", end="", flush=True)
        time.sleep(1)
    print("\nProgress complete.\n")

# Define script stages and their duration in seconds
STAGE1_DURATION = 20
STAGE2_DURATION = 30
STAGE3_DURATION = 20
STAGE4_DURATION = 20
STAGE5_DURATION = 10
TOTAL_DURATION = STAGE1_DURATION + STAGE2_DURATION + STAGE3_DURATION + STAGE4_DURATION + STAGE5_DURATION

# Kill related programs
processes_to_kill = ["Xvfb :99", "website_monitor.py", "BitPredictor.py", "webserver.py", "PriceUpdater.py", "Xvfb"]
print(f"{timestamp()} - Checking and killing related programs...")
for proc in processes_to_kill:
    if is_process_running(proc):
        kill_process(proc)
        time.sleep(2)
print(f"{timestamp()} - All related programs checked and killed (if running)")
print()

# Start progress bar for the whole process in a separate thread (optional, for non-blocking)
import threading
progress_thread = threading.Thread(target=progress_bar, args=(TOTAL_DURATION,))
progress_thread.start()

CURRENT_PROGRESS = 0

# Stage 1: Start Xvfb virtual display server
print(f"{timestamp()} - Starting Xvfb virtual display server...")
xvfb_process = None
if not sys.platform.startswith('win'):
    try:
        xvfb_process = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1024x768x24'])
        time.sleep(2)
        if not is_process_running("Xvfb :99"):
            error_msg = f"{timestamp()} - Failed to start Xvfb virtual display server"
            print(error_msg)
            with open("runallscripts.log", "a") as f:
                f.write(error_msg + "\n")
            sys.exit(1)
        print(f"{timestamp()} - Xvfb virtual display server started (PID: {xvfb_process.pid if xvfb_process else 'N/A'})")
    except FileNotFoundError:
        error_msg = f"{timestamp()} - Error: Xvfb not found. Please ensure it's installed (Linux/macOS only)."
        print(error_msg)
        with open("runallscripts.log", "a") as f:
            f.write(error_msg + "\n")
        sys.exit(1)
else:
    print(f"{timestamp()} - Skipping Xvfb as it's not typically used on Windows.")

time.sleep(STAGE1_DURATION)
CURRENT_PROGRESS += STAGE1_DURATION

# Stage 2: Run BitPredictor script
print(f"{timestamp()} - Running BitPredictor script...")
bitpredictor_process = subprocess.Popen(['python', 'BitPredictor.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(10)
output = bitpredictor_process.stdout.read()
if "BitPredictor started successfully" not in output:
    error_msg = f"{timestamp()} - BitPredictor script failed to start. Check BitPredictor.log for details."
    print(error_msg)
    with open("runallscripts.log", "a") as f:
        f.write(error_msg + "\n")
    with open("BitPredictor.log", "w") as f:
        f.write(output + bitpredictor_process.stderr.read())
    sys.exit(2)
print(f"{timestamp()} - BitPredictor script started successfully (PID: {bitpredictor_process.pid})")

time.sleep(STAGE2_DURATION)
CURRENT_PROGRESS += STAGE2_DURATION

# Stage 3: Run PriceUpdater script
print(f"{timestamp()} - Running PriceUpdater script...")
priceupdater_process = subprocess.Popen(['python', 'PriceUpdater.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(10)
output = priceupdater_process.stdout.read()
if "PriceUpdater started successfully" not in output:
    error_msg = f"{timestamp()} - PriceUpdater script failed to start. Check PriceUpdater.log for details."
    print(error_msg)
    with open("runallscripts.log", "a") as f:
        f.write(error_msg + "\n")
    with open("PriceUpdater.log", "w") as f:
        f.write(output + priceupdater_process.stderr.read())
    sys.exit(3)
print(f"{timestamp()} - PriceUpdater script started successfully (PID: {priceupdater_process.pid})")

time.sleep(STAGE3_DURATION)
CURRENT_PROGRESS += STAGE3_DURATION

# Stage 4: Run website monitoring script
print(f"{timestamp()} - Running website monitoring script...")
website_monitor_process = subprocess.Popen(['python', 'website_monitor.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(10)
output = website_monitor_process.stdout.read()
if "Website monitoring started successfully" in output:
    print(f"{timestamp()} - Website monitoring script started successfully (PID: {website_monitor_process.pid})")
else:
    error_msg = f"{timestamp()} - Website monitoring script failed to start. Check website_monitor.log for details."
    print(error_msg)
    with open("runallscripts.log", "a") as f:
        f.write(error_msg + "\n")
    with open("website_monitor.log", "w") as f:
        f.write(output + website_monitor_process.stderr.read())
    sys.exit(4)

time.sleep(STAGE4_DURATION)
CURRENT_PROGRESS += STAGE4_DURATION

# Stage 5 (Implicit): The remaining time in the progress bar

# Wait for the progress bar thread to finish
progress_thread.join()

print(f"{timestamp()} - All scripts started successfully.")