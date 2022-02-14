#!/bin/bash
 
source ../../env/btceurhist/bin/activate
python -u -m btceurhist startserver 2>&1 | tee -a LOGGING.txt


