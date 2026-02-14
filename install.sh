#!/usr/bin/env bash
# Installation script for Mac/Linux

set -e

echo "=== Installing Claude Multi ==="
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "Using Python: $PYTHON"
$PYTHON --version
echo ""

# Install the package
echo "Installing claude-multi..."
$PYTHON -m pip install -e .

if [ $? -eq 0 ]; then
    echo ""
    echo "[OK] Installation successful!"
    echo ""

    # Make run.sh executable
    chmod +x run.sh
    echo "[OK] Made run.sh executable"
    echo ""

    # Initialize claude-multi
    echo "Initializing claude-multi..."
    $PYTHON -m claude_multi.cli init
    echo ""

    # Offer to add to PATH
    echo "=== Setup Complete ==="
    echo ""
    echo "You can now use claude-multi in three ways:"
    echo ""
    echo "1. Use the wrapper script:"
    echo "   ./run.sh start ."
    echo ""
    echo "2. Use python -m directly:"
    echo "   $PYTHON -m claude_multi.cli start ."
    echo ""
    echo "3. Add an alias to your shell profile (~/.bashrc, ~/.zshrc):"
    echo "   alias claude-multi='$PYTHON -m claude_multi.cli'"
    echo ""
    echo "Or install the wrapper globally:"
    echo "   sudo cp run.sh /usr/local/bin/claude-multi"
    echo ""
else
    echo ""
    echo "[ERROR] Installation failed"
    exit 1
fi
