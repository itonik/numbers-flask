#!/bin/sh

# Fail on error
set -e

# If ./venv does not exist -> 
# -> create venv and add all dependencies
if [ ! -d "./venv" ]; then
    echo "No venv found. Creating..."
    python3 -m venv venv
    python3 -m pip install Flask opencv-python sklearn pandas
fi

# venv can be activated by:
# . venv/bin/activate
