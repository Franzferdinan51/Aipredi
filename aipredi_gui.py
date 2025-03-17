import tkinter as tk
from tkinter import ttk
import requests
import threading
import website  # Assuming you have a website.py file
import json

# Replace with your actual Gemini API key (consider loading from a secure source)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Define event to signal pausing of training
pause_event = threading.Event()

class AiprediGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Training Progress with Gemini")

        self.progress_var = tk.StringVar()
        self.accuracy_var = tk.StringVar()
        self.progress_label = ttk.Label(self, textvariable=self.progress_var, font=("Arial", 16))
        self.accuracy_label = ttk.Label(self, textvariable=self.accuracy_var, font=("Arial", 16))
        self.progress_label.pack(pady=10)
        self.accuracy_label.pack(pady=10)

        self.start_button = ttk.Button(self, text="Start", command=self.start_training)
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_training, state="disabled")
        self.pause_button = ttk.Button(self, text="Pause", command=self.pause_training, state="disabled")
        self.start_button.pack(side="left", padx=10)
        self.stop_button.pack(side="left", padx=10)
        self.pause_button.pack(side="left", padx=10)

        self.website_status_label = ttk.Label(self, text="", font=("Arial", 16))
        self.website_status_label.pack(pady=10)
        self.check_website_status()

        # Gemini Integration
        self.gemini_label = ttk.Label(self, text="Ask Gemini:", font=("Arial", 12))
        self.gemini_label.pack(pady=5)
        self.gemini_prompt_entry = ttk.Entry(self, width=50)
        self.gemini_prompt_entry.pack(pady=5)
        self.gemini_send_button = ttk.Button(self, text="Send to Gemini", command=self.send_to_gemini)
        self.gemini_send_button.pack(pady=10)
        self.gemini_response_label = ttk.Label(self, text="Gemini Response:", font=("Arial", 12))
        self.gemini_response_label.pack(pady=5)
        self.gemini_response_text = tk.Text(self, height=5, width=50)
        self.gemini_response_text.pack(pady=5)
        self.gemini_response_text.config(state=tk.DISABLED)

        self.training_thread = None

    def start_training(self):
        website.start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.pause_button.config(state="normal")
        self.pause_event.clear() # Ensure pause is not set at start
        self.training_thread = threading.Thread(target=self._train)
        self.training_thread.start()

    def _train(self):
        for i in range(1, 101):
            while self.pause_event.is_set():
                self.update()
                time.sleep(0.1)
                continue
            self.progress_var.set(f"Training progress: {i}%")
            self.accuracy_var.set(f"Accuracy: {i/2}%")
            time.sleep(0.1) # Simulate training time

    def stop_training(self):
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.pause_button.config(text="Pause", state="disabled")
        website.stop()
        self.progress_var.set("")
        self.accuracy_var.set("")
        if self.training_thread and self.training_thread.is_alive():
            # No clean way to force stop a thread in Python, consider using a flag
            pass # For this example, we'll just disable controls

    def pause_training(self):
        if self.pause_button.config('text')[-1] == 'Pause':
            self.pause_button.config(text='Resume')
            self.pause_event.set()
        else:
            self.pause_button.config(text='Pause')
            self.pause_event.clear()

    def check_website_status(self):
        try:
            response = requests.get('http://localhost:8000')
            self.website_status_label.config(text="Website is up", fg="green")
        except requests.exceptions.RequestException as e:
            self.website_status_label.config(text="Website is down", fg="red")
        self.after(5000, self.check_website_status)

    def query_gemini(self, prompt):
        """Queries the Gemini API with the given prompt."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMAIzaSyDEwn99vtbn8WB-KBzecRawG1lBi3dW09w}"
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
            error_message = f"Error querying Gemini API: {e}"
            self.display_gemini_response(error_message)
            return None

    def send_to_gemini(self):
        prompt = self.gemini_prompt_entry.get()
        if prompt:
            self.display_gemini_response("Thinking...")
            threading.Thread(target=self.fetch_and_display_gemini_response, args=(prompt,)).start()

    def fetch_and_display_gemini_response(self, prompt):
        response = self.query_gemini(prompt)
        self.display_gemini_response(response if response else "No response from Gemini.")

    def display_gemini_response(self, text):
        self.gemini_response_text.config(state=tk.NORMAL)
        self.gemini_response_text.delete("1.0", tk.END)
        self.gemini_response_text.insert(tk.END, text)
        self.gemini_response_text.config(state=tk.DISABLED)

    pause_event = threading.Event()

if __name__ == "__main__":
    app = AiprediGUI()
    app.mainloop()