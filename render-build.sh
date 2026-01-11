#!/usr/bin/env bash
# Exit on error
set -e
echo "Starting Render Build Process..."

echo "=== DIAGNOSTIC START ==="
echo "Current Directory: $(pwd)"
echo "Listing files:"
ls -F
echo "========================"

if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt, installing..."
    pip install -r requirements.txt
else
    echo "ERROR: requirements.txt not found!"
    exit 1
fi
