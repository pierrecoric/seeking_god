#!/bin/bash

source godenv/bin/activate
echo "" > output/history.md
echo "" > output/poem.txt
python3 seeking.py
deactivate