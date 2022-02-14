#!/bin/bash

sudo apt install python3-venv
 
python3 -m venv ../../env/btceurhist
source ../../env/btceurhist/bin/activate

pip3 install -U pip wheel
pip install -r requirements.txt