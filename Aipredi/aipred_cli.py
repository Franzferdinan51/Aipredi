import tkinter as tk
from tkinter import scrolledtext
import subprocess

class TerminalGUI:
    def __init__(self, master):
        self.master = master
        master.title("Terminal")

        # Create scrolled text widget to display output
        self.output_text = scrolledtext.ScrolledText(master, height=20, width=50, state="disabled")
        self.output_text.pack()

        # Create entry widget to input commands
        self.command_entry = tk.Entry(master)
        self.command_entry.pack()

        # Bind <Return> key to execute_command function
        self.command_entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        # Get command from entry widget
        command = self.command_entry.get()

        # Execute command using subprocess module
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output

        # Display output in scrolled text widget
        self.output_text.config(state="normal")
        self.output_text.insert("end", f">> {command}\n{output}\n")
        self.output_text.config(state="disabled")

        # Clear command entry widget
        self.command_entry.delete(0, "end")

# Create root window and initialize GUI
root = tk.Tk()
gui = TerminalGUI(root)

# Start GUI event loop
root.mainloop()
