#!/bin/bash

# List of commands to check
PACKAGES=("python3" "pip3")

INFO=$(echo "
For instructions to install the latest stable  
release of Python dependencies browse to:
https://www.python.org/doc/versions/")
        

for CMD in "${PACKAGES[@]}"; do
    # command -v returns 0 if found, 1 if not
    if command -v "$CMD" &> /dev/null; then
        echo "✓ $CMD is installed."
    else
        echo "✗ $CMD is NOT installed." 
        echo "$INFO"
        exit 1
    fi
done   

# Check if the venv module is available in the current Python installation
if python3 -m venv --help &> /dev/null; then
    echo "✓ python3 venv module is installed."
else
    echo "✗ python3 venv module is not installed."
    echo "$INFO"
    exit 1
fi   