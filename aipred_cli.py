import sys
import os
import requests
import importlib
from dotenv import load_dotenv
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
                             QPlainTextEdit, QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtGui import QClipboard
import json
import subprocess
from PIL import Image
import threading

# Optional imports for other model types (install these if needed: pip install torch tensorflow)
# import torch
# import tensorflow as tf
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # Ensure transformers is installed

load_dotenv()

# Set up your API keys (load from .env file for security)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Your API key in quotes
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

API_URL = "http://127.0.0.1:5000"  # Replace with your Flask API URL
LAST_AI_FILE = "last_ai.txt"


# --- Helper Functions (remain the same) --->
# --- Helper Functions --->

def display_error(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.exec()

def display_warning(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.exec()

def display_info(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.exec()

def run_subprocess(command, shell=False, text=True, check=True, stderr=subprocess.STDOUT):
    """Helper function to run subprocess commands."""
    try:
        result = subprocess.run(command, shell=shell, text=text, check=check, stderr=stderr, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stdout.strip()}"
    except FileNotFoundError:
        return "Error: Command not found."
# --- AI Functions (remain the same) ---
# --- AI Functions ---

def google_gemini(message):
    if not GEMINI_API_KEY:
        display_error("API Key Error", "GEMINI_API_KEY not set in .env file.")
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": message}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        display_error("API Error", f"Failed to get response from Gemini: {e}")
        return None

def autogpt(message):
    if not OPENAI_API_KEY:
        display_error("API Key Error", "OPENAI_API_KEY not set in .env file.")
        return None
    url = "https://api.openai.com/v1/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-3.5-turbo-instruct", # Or another suitable model
        "prompt": message,
        "temperature": 0.7,
        "max_tokens": 150 # Increased max tokens
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()['choices'][0]['text'].strip()
    except requests.exceptions.RequestException as e:
        display_error("API Error", f"Failed to get response from OpenAI: {e}")
        return None

def LLaMA(message):
    display_warning("LLaMA", "LLaMA API integration is a placeholder and might require significant setup or a different API depending on your LLaMA access.")
    if not LLAMA_API_KEY:
        display_error("API Key Error", "LLAMA_API_KEY not set in .env file.")
        return None
    # Replace with the actual LLaMA API endpoint and headers if you have access
    # This is a very generic example and likely needs modification
    url = "YOUR_LLAMA_API_ENDPOINT"
    headers = {"Authorization": f"Bearer {LLAMA_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": message}
    try:
        if "YOUR_LLAMA_API_ENDPOINT" in url:
            return "[LLaMA API Endpoint Not Configured]"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json().get("completion") # Adjust based on actual API response
    except requests.exceptions.RequestException as e:
        display_error("API Error", f"Failed to get response from LLaMA: {e}")
        return None

# List of AI participants
ai_list = [google_gemini]  # Initialize ai_list with the google_gemini function

# --- GUI Setup ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chatbox")
        self.setGeometry(100, 100, 1920, 1080)  # Set window size to 1080p

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        # --- Chat Display ---
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Allow expansion
        self.layout.addWidget(self.chat_display)

        # --- Chat Input ---
        self.input_layout = QHBoxLayout()
        self.command_entry = QPlainTextEdit()
        self.input_layout.addWidget(self.command_entry)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)

        # --- AI Selection and Controls ---
        self.controls_layout = QHBoxLayout()
        self.ai_label = QLabel("Select AI:")
        self.controls_layout.addWidget(self.ai_label)
        self.cmb_ai = QComboBox()
        self.controls_layout.addWidget(self.cmb_ai)

        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.clicked.connect(self.clear_chat_history)
        self.controls_layout.addWidget(self.clear_history_button)

        self.layout.addLayout(self.controls_layout)

        # --- Output Display (for thought process) ---
        self.output_display = QPlainTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Allow expansion
        self.layout.addWidget(self.output_display)

        self.output_controls_layout = QHBoxLayout()
        self.copy_output_button = QPushButton("Copy Output")
        self.copy_output_button.clicked.connect(self.copy_output_to_clipboard)
        self.output_controls_layout.addWidget(self.copy_output_button)
        self.layout.addLayout(self.output_controls_layout)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.load_ai_participants()
        self.populate_ai_combobox()

    def add_message(self, message, sender):
        if sender == "You":
            self.chat_display.append(f"<span style='font-weight: bold;'>You:</span> {message}")
        else:
            self.chat_display.append(f"<span style='font-weight: bold; color: blue;'>{sender}:</span> {message}")

    def response(self, message, sender):
        self.add_message(message, sender)

    @Slot()
    def send_message(self):
        message = self.command_entry.toPlainText().strip()
        if message:
            self.add_message(message, "You")
            self.command_entry.clear()
            selected_ai_name = self.cmb_ai.currentText()
            ai_response = None
            if selected_ai_name == "google_gemini":
                threading.Thread(target=self.fetch_and_display_gemini_response, args=(message,)).start()
            elif selected_ai_name == "autogpt":
                threading.Thread(target=self.fetch_and_display_autogpt_response, args=(message,)).start()
            elif selected_ai_name == "LLaMA":
                threading.Thread(target=self.fetch_and_display_llama_response, args=(message,)).start()
            else:
                # Check for locally loaded AI participants
                for ai_func in ai_list:
                    if hasattr(ai_func, '__name__') and ai_func.__name__ == selected_ai_name:
                        threading.Thread(target=self.fetch_and_display_local_response, args=(message, ai_func)).start()
                        break
                else:
                    display_error("Error", "No AI participant selected or found.")
            self.status_label.setText("Idle.") # Clear status after processing

    def display_output(self, text):
        self.output_display.appendPlainText(text)

    def fetch_and_display_gemini_response(self, prompt):
        self.display_output("Gemini is thinking...")
        response_text = google_gemini(prompt)
        if response_text:
            self.display_output("Gemini finished thinking.")
            self.response(response_text, "google_gemini")
        else:
            self.display_output("No response from Gemini.\n")
        self.status_label.setText("Idle.")

    def fetch_and_display_autogpt_response(self, prompt):
        self.display_output("AutoGPT is thinking...")
        response_text = autogpt(prompt)
        if response_text:
            self.display_output("AutoGPT finished thinking.")
            self.response(response_text, "autogpt")
        else:
            self.display_output("No response from AutoGPT.\n")
        self.status_label.setText("Idle.")

    def fetch_and_display_llama_response(self, prompt):
        self.display_output("LLaMA is thinking...")
        response_text = LLaMA(prompt)
        if response_text:
            self.display_output("LLaMA finished thinking.")
            self.response(response_text, "LLaMA")
        else:
            self.display_output("No response from LLaMA.\n")
        self.status_label.setText("Idle.")

    def fetch_and_display_local_response(self, prompt, ai_function):
        self.display_output(f"{ai_function.__name__} is thinking...")
        response_text = ai_function(prompt)
        if response_text:
            self.display_output(f"{ai_function.__name__} finished thinking.")
            self.response(response_text, ai_function.__name__)
        else:
            self.display_output(f"No response from {ai_function.__name__}.\n")
        self.status_label.setText("Idle.")

    def load_ai_participants(self):
        if GEMINI_API_KEY:
            ai_list.append(google_gemini)
        if OPENAI_API_KEY:
            ai_list.append(autogpt)
        if LLAMA_API_KEY:
            ai_list.append(LLaMA)

        modules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")
        sys.path.append(modules_dir)
        if os.path.exists(modules_dir):
            files = os.listdir(modules_dir)
            for file in files:
                if file.endswith(".py"):
                    module_name = file[:-3]
                    try:
                        module = importlib.import_module(module_name)

                        # Check for a general 'ai' function
                        if hasattr(module, "ai") and callable(module.ai) and module.ai not in ai_list:
                            ai_list.append(module.ai)
                            print(f"Loaded AI function from: {module_name} as {module_name}")

                        # Check for Hugging Face model path
                        elif hasattr(module, "model_path"):
                            model_path = getattr(module, "model_path")
                            try:
                                from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
                                tokenizer = AutoTokenizer.from_pretrained(model_path)
                                model = AutoModelForCausalLM.from_pretrained(model_path)
                                pipe = pipeline('text-generation', model=model, tokenizer=tokenizer)

                                def huggingface_ai(prompt, pipeline=pipe):
                                    try:
                                        result = pipeline(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
                                        return result
                                    except Exception as e:
                                        return f"Error during inference: {e}"

                                huggingface_ai.__name__ = module_name
                                if huggingface_ai not in ai_list:
                                    ai_list.append(huggingface_ai)
                                    print(f"Loaded Hugging Face model from: {model_name} as {module_name}")

                            except ImportError as e:
                                print(f"Error importing transformers or loading model from {module_name}: {e}")
                            except Exception as e:
                                print(f"Error loading Hugging Face model from {module_name}: {e}")

                        # Add checks for other model types here (e.g., PyTorch, TensorFlow)
                        # elif hasattr(module, "pytorch_model"):
                        #     # Example PyTorch loading (requires proper setup in the module)
                        #     if hasattr(module, "load_pytorch_model") and callable(module.load_pytorch_model):
                        #         model = module.load_pytorch_model()
                        #         if hasattr(module, "generate_pytorch_response") and callable(module.generate_pytorch_response) and hasattr(model, '__call__'):
                        #             def pytorch_ai(prompt, model=model, generate_fn=module.generate_pytorch_response):
                        #                 return generate_fn(prompt, model)
                        #             pytorch_ai.__name__ = module_name
                        #             if pytorch_ai not in ai_list:
                        #                 ai_list.append(pytorch_ai)
                        #                 print(f"Loaded PyTorch model from: {module_name} as {module_name}")

                        else:
                            print(f"Warning: No valid AI interface found in module: {module_name}")

                    except Exception as e:
                        print(f"Error loading module {module_name}: {e}")
        else:
            print("Modules directory does not exist.")

    def populate_ai_combobox(self):
        ai_options = [ai_func.__name__ for ai_func in ai_list if hasattr(ai_func, '__name__')]
        self.cmb_ai.clear()
        self.cmb_ai.addItems(ai_options)
        if "google_gemini" in ai_options:
            self.cmb_ai.setCurrentText("google_gemini")
        elif ai_options:
            self.cmb_ai.setCurrentIndex(0)

    @Slot()
    def clear_chat_history(self):
        # Clear the widgets in the chat layout
        for i in reversed(range(self.chat_layout.count())):
            widget = self.chat_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    @Slot()
    def copy_output_to_clipboard(self):
        # For this new GUI, we'll copy the entire chat history
        full_chat = ""
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item.widget():
                full_chat += item.widget().text() + "\n"
        clipboard = QClipboard()
        clipboard.setText(full_chat.strip())
        display_info("Copied", "Chat history copied to clipboard.")

    def closeEvent(self, event):
        self.save_last_ai()
        event.accept()

    def save_last_ai(self):
        current_ai = self.cmb_ai.currentText()
        try:
            with open(LAST_AI_FILE, "w") as f:
                f.write(current_ai)
        except Exception as e:
            print(f"Error saving last AI: {e}")

    def load_last_ai(self):
        try:
            if os.path.exists(LAST_AI_FILE):
                with open(LAST_AI_FILE, "r") as f:
                    last_ai = f.readline().strip()
                    index = self.cmb_ai.findText(last_ai)
                    if index != -1:
                        self.cmb_ai.setCurrentIndex(index)
        except Exception as e:
            print(f"Error loading last AI: {e}")

    @Slot()
    def start_speech_recognition(self):
        threading.Thread(target=speech_to_text, args=(self,)).start()

    def execute_command(command):
        """Executes a system command or a predefined action and displays the output."""
        command_lower = command.lower()
        if command_lower == "open notepad":
            notepad_command = "notepad.exe" if sys.platform.startswith('win') else (
                "xdg-open notepad" if sys.platform.startswith('linux') else (
                "open -a TextEdit" if sys.platform.startswith('darwin') else None))
            if notepad_command:
                output = run_subprocess(notepad_command, shell=True)
                return f"Command: {command}\n{output}\n"
            else:
                return "Error: Unsupported OS for '{command}'.\n"
        elif command_lower == "list files":
            list_command = "dir" if sys.platform.startswith('win') else "ls -l"
            output = run_subprocess(list_command, shell=True)
            return f"Command: {command}\n{output}\n"
        else:
            output = run_subprocess(command, shell=True)
            return f"Command: {command}\n{output}\n"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
