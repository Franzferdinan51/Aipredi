#!/bin/bash

# create virtual environment
python3 -m venv env

# activate virtual environment
source env/bin/activate

# update package list
sudo apt update

# install packages
sudo apt install python3-tk python3-pil python3-pil.imagetk python3-pip

# install pip packages
pip3 install requests
pip3 install blockchain-api-client
pip3 install blockchain

# ask user for confirmation before deactivating virtual environment
read -p "Do you want to deactivate the virtual environment? (yes/no) " choice
case "$choice" in 
  yes|y ) 
    # wait for any running processes to finish
    echo "Waiting for processes to finish..."
    wait
    # deactivate virtual environment
    deactivate
    ;;
  * ) 
    echo "Virtual environment will remain activated."
    ;;
esac

