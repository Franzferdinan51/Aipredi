#!/bin/bash

# create virtual environment
python3 -m venv env

# activate virtual environment
source env/bin/activate

# update package list
sudo apt update

# install packages
sudo apt install python3-tk python3-pil python3-pil.imagetk python3-wikipedia python3-stackapi python3-pip

# install pip packages
pip3 install requests
pip3 install git+https://github.com/blockchain/api-v1-client-python.git

# install stackexchange package
pip3 install git+https://github.com/lucjon/Py-StackExchange.git

# deactivate virtual environment
deactivate
