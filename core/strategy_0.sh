#!/bin/bash
SHELL=/bin/bash
PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages

source /home/ubuntu/.bashrc
source /home/ubuntu/.profile
cd /home/ubuntu/racehorse/core
nohup python3 ./strategy_0.py >> ./strategy_0.txt 2>&1 &