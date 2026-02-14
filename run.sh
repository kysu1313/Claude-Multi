#!/usr/bin/env bash
# Convenient wrapper for running claude-multi on Unix systems

# Find python3 or python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Run claude-multi
$PYTHON -m claude_multi.cli "$@"
