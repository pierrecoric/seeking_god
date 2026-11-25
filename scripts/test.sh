#!/bin/bash

source godenv/bin/activate
echo "" > output/history.md
python3 test.py
deactivate