import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import requests
import json
import threading
import time  # Import time for potential testing delays

# Replace with your actual Gemini API key (consider loading from a secure source)
GEMINI_API_KEY = "AIzaSyDEwn99vtbn8WB-KBzecRawG1lBi3dW09w"  # Your API key in quotes

class TerminalGUI:
    def __init__(self, master):
        self.master = master
        master.title("aipred_cli.py - Terminal with Gemini")

        # Create scrolled text widget to display output
        self.output_text = scrolledtext.ScrolledText(master, height=20, width=80, state="disabled")
        self.output_text.pack(pady=10)

        # Gemini Prompt Label
        self.gemini_label = ttk.Label(master, text="Gemini Prompt:", font=("Arial", 10))
        self.gemini_label.pack(pady=5)

        # Gemini Entry Widget
        self.gemini_entry = tk.Entry(master, width=60)
        self.gemini_entry.pack(pady=5)

        # Bind <Return> key to execute_gemini_command function
        self.gemini_entry.bind("<Return>", self.execute_gemini_command)

        # Command Entry Label
        self.command_label = ttk.Label(master, text="System Command:", font=("Arial", 10))
        self.command_label.pack(pady=5)

        # Create entry widget to input system commands
        self.command_entry = tk.Entry(master, width=60)
        self.command_entry.pack(pady=5)

        # Bind <Return> key to execute_command function
        self.command_entry.bind("<Return>", self.execute_command)

        # Status Label
        self.status_label = ttk.Label(master, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def query_gemini(self, prompt):
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
            self.display_output(f"Error querying Gemini API: {e}")
            return None

    def execute_gemini_command(self, event):
        """Executes a Gemini prompt and displays the response."""
        prompt = self.gemini_entry.get()
        if prompt:
            self.display_output(f">> Gemini Prompt: {prompt}\nThinking...")
            self.gemini_entry.delete(0, "end")  # Clear the entry
            threading.Thread(target=self.fetch_and_display_gemini_response, args=(prompt,)).start()

    def fetch_and_display_gemini_response(self, prompt):
        """Fetches the Gemini response in a thread and displays it."""
        response = self.query_gemini(prompt)
        if response:
            self.master.after(0, self.display_output, f"Gemini Response:\n{response}\n") # Use after
        else:
            self.master.after(0, self.display_output, "No response from Gemini.\n")  # Use after

    def execute_command(self, event):
        """Executes a system command and displays the output."""
        command = self.command_entry.get()
        self.display_output(f">> System Command: {command}\n")
        self.command_entry.delete(0, "end")  # Clear the entry
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
            self.display_output(f"{output}\n")
            self.status_label.config(text="Command executed successfully", fg="green")
        except subprocess.CalledProcessError as e:
            output = e.output
            self.display_output(f"{output}\n")
            self.status_label.config(text=f"Error: {e}", fg="red")
        except FileNotFoundError:
            self.display_output("Command not found.\n")
            self.status_label.config(text="Command not found", fg="red")

    def display_output(self, text):
        """Displays text in the scrolled text widget."""
        self.output_text.config(state="normal")
        self.output_text.insert("end", text)
        self.output_text.see("end")  # Autoscroll
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalGUI(root)
    root.mainloop()  # This line is crucial!