#!/bin/sh

# Fail on error
set -e

# If ./venv does not exist -> 
# -> create venv and add all dependencies
if [ ! -d "./venv" ]; then
    echo "No venv found. Creating..."
    python3 -m venv venv
    python3 -m pip install Flask
fi

# Activate venv
. venv/bin/activate
