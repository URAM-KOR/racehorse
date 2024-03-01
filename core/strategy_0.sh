#!/bin/bash
SHELL=/bin/bash
PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages

# Check if python3 is running
if ! pgrep -x "python3" > /dev/null
then
    # Run python3 in the background using nohup
    source /home/ubuntu/.bashrc
    source /home/ubuntu/.profile
    cd /home/ubuntu/racehorse/core
    nohup python3 ./strategy_0.py >> ./strategy_0.txt 2>&1 &
fi
