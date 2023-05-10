#!/bin/bash

# This script installs the 'wikipedia' package using pip in a user-specific directory

# Get the directory containing the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Install 'python3-venv' if not already installed
if ! dpkg -s python3-venv >/dev/null 2>&1; then
  echo "Installing 'python3-venv'..."
  sudo apt-get update && sudo apt-get install -y python3-venv
fi

# Create a virtual environment
if [ ! -d "$DIR/venv" ]; then
  python3 -m venv "$DIR/venv"
fi

# Activate the virtual environment
source "$DIR/venv/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install the 'wikipedia' package
pip install wikipedia

# Deactivate the virtual environment
deactivate

# Add the directory containing the script to the PATH environment variable
export PATH="$PATH:$DIR"
