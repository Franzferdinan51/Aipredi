 
import time
import requests
import subprocess
import sys
import os
import traceback
import threading
from typing import List

sys.path.append('/home/duckets/Documents/Aipredi')
from aipredi_gui import *

# Define a function to simulate the AI training process
def train_model(progress_var, accuracy_var, stop_event, pause_event):
    # Set initial values
    progress = 0
    accuracy = 0
    epoch = 0

    # Run training loop until stop button is pressed
    while not stop_event.is_set():
        # Check if pause button is pressed
        while pause_event.is_set():
            time.sleep(0.1)

        # Perform one epoch of training
        time.sleep(0.5) # Simulate training time
        epoch += 1
        progress = epoch / 10
        accuracy = epoch * 10 % 100

        # Update progress and accuracy variables
        set_progress(progress_var, progress)
        set_accuracy(accuracy_var, accuracy)

        # Check if training is complete
        if epoch == 10:
            break

        # Update GUI
        root.update()

    # If an error occurs, save error information to file
    try:
        # Call a function that doesn't exist to raise an exception
        undefined_function()
    except Exception as e:
        # Get the traceback information
        tb = traceback.format_exc()

        # Save the traceback information to a file
        with open('error.log', 'w') as f:
            f.write(tb)

        # Display a message box with the error information
        response = messagebox.askyesno("Error", f"An error occurred:\n\n{tb}\n\nDo you want to view the error log?")
        if response:
            # Open the error log file
            subprocess.Popen(['xdg-open', 'error.log'])

# Define function to start training
def start_training():
    global stop_event, pause_event
    # Disable start button and enable stop and pause buttons
    disable_start_button()
    enable_stop_button()
    enable_pause_button()

    # Create stop and pause events
    stop_event = threading.Event()
    pause_event = threading.Event()

    # Start training thread
    training_thread = threading.Thread(target=train_model, args=(progress_var, accuracy_var, stop_event, pause_event))
    training_thread.start()

    # Open a new terminal and show processes and logging information for this program only
    subprocess.Popen(['terminator', '-e', 'watch -n 1 "ps -ef | grep train_model"'])

# Define function to stop training
def stop_training():
    # Enable start button and disable stop and pause buttons
    enable_start_button()
    disable_stop_button()
    disable_pause_button()

    # Set stop event to stop training
    stop_event.set()

# Define function to pause/resume training
def pause_training():
    # Toggle pause event
    if pause_button.config('text')[-1] == 'Pause':
        pause_button.config(text='Resume')
        pause_event.set()
    else:
        pause_button.config(text='Pause')
        pause_event.clear()

# Define function to check website status and update label
def check_website_status():
    # Send a GET request to the website
    try:
        response = requests.get('http://localhost:8000')
        # If the request is successful, set the label text to "Website is up" and color to green
        set_website_status("Website is up", "green")
    except requests.exceptions.RequestException as e:
        # If the request fails, set the label text to "Website is down" and color to red
