import tkinter as tk
from tkinter import ttk
import requests
import threading
import website

# Define event to signal pausing of training
pause_event = threading.Event()

# Define function to start training
def start_training():
    # Start the website
    website.start()

    # Disable start button and enable stop and pause buttons
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    pause_button.config(state="normal")

    # Start training
    for i in range(1, 101):
        # Check for pause event and wait if it is set
        while pause_event.is_set():
            root.update()
            continue

        # Update progress and accuracy labels
        progress_var.set(f"Training progress: {i}%")
        accuracy_var.set(f"Accuracy: {i/2}%")

        # Sleep for 0.1 seconds to simulate training time
        root.after(100)

# Define function to stop training and stop website
def stop_training():
    # Enable start button and disable stop and pause buttons
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    pause_button.config(text="Pause", state="disabled")

    # Stop the website
    website.stop()

    # Reset progress and accuracy labels
    progress_var.set("")
    accuracy_var.set("")

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
        website_status_label.config(text="Website is up", fg="green")
    except requests.exceptions.RequestException as e:
        # If the request fails, set the label text to "Website is down" and color to red
        website_status_label.config(text="Website is down", fg="red")

    # Call this function again after 5 seconds
    root.after(5000, check_website_status)

# Create GUI
root = tk.Tk()
root.title("AI Training Progress")

# Create labels for progress and accuracy
progress_var = tk.StringVar()
accuracy_var = tk.StringVar()
progress_label = ttk.Label(root, textvariable=progress_var, font=("Arial", 16))
accuracy_label = ttk.Label(root, textvariable=accuracy_var, font=("Arial", 16))
progress_label.pack(pady=10)
accuracy_label.pack(pady=10)

# Create start, stop, and pause buttons
start_button = ttk.Button(root, text="Start", command=start_training)
stop_button = ttk.Button(root, text="Stop", command=stop_training, state="disabled")
pause_button = ttk.Button(root, text="Pause", command=pause_training, state="disabled")
start_button.pack(side="left", padx=10)
stop_button.pack(side="left", padx=10)
pause_button.pack(side="left", padx=10)

# Create label to display website status
website_status_label = ttk.Label(root, text="", font=("Arial", 16))
website_status_label.pack(pady=10)

# Start checking website status
check_website_status()

# Start GUI event loop
root.mainloop()
