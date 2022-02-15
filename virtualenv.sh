#!/bin/bash

# sudo apt install python3-venv
 
python3 -m venv ../../env/btceurhist
source ../../env/btceurhist/bin/activate

pip3 install -U pip wheel
pip install -r requirements.txt

# used by tools mentioned in this github python template:
pip install flake8 black mypy types-requests mkdocs
