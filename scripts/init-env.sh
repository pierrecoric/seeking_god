#!/bin/bash

python3 -m venv godenv
source godenv/bin/activate
pip install beautifulsoup4
pip list
deactivate