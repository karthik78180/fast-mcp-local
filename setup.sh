#!/bin/bash
set -e

echo "Fast MCP Local - Setup Script"
echo "=============================="
echo

# Check for Python 3.10+
PYTHON_CMD=""
for cmd in python3.13 python3.12 python3.11 python3.10; do
    if command -v $cmd &> /dev/null; then
        PYTHON_CMD=$cmd
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.10 or higher is required but not found."
    echo
    echo "Please install Python 3.10+ first. See INSTALL.md for instructions."
    echo
    echo "Quick install with Homebrew:"
    echo "  brew install python@3.11"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
echo "✓ Found $PYTHON_CMD ($PYTHON_VERSION)"
echo

# Remove old venv if it exists
if [ -d ".venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf .venv
fi

# Create venv
echo "Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv .venv

# Activate and install
echo "Installing dependencies..."
source .venv/bin/activate
pip3 install --upgrade pip > /dev/null
pip3 install -e ".[dev]"

echo
echo "✓ Setup complete!"
echo
echo "To activate the environment:"
echo "  source .venv/bin/activate"
echo
echo "To run tests:"
echo "  pytest"
echo
echo "To run the server:"
echo "  python3 -m fast_mcp_local.server"
