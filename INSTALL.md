# Installation Instructions

## Problem

This project requires Python 3.10 or higher, but your system only has Python 3.9.6.

## Solution: Install Python 3.11+

### Option 1: Homebrew (Recommended - Fastest)

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Remove old venv
rm -rf .venv

# Create new venv with Python 3.11
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip3 install -e ".[dev]"

# Run tests
pytest

# Run server
python3 -m fast_mcp_local.server
```

### Option 2: Download from python.org

1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or newer for macOS
3. Install it
4. Then run:

```bash
# Remove old venv
rm -rf .venv

# Create new venv
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip3 install -e ".[dev]"
```

### Option 3: pyenv

```bash
# Install pyenv
brew install pyenv

# Add to shell config
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Restart shell or source config
source ~/.zshrc

# Install Python 3.11
pyenv install 3.11

# Set as local version for this project
pyenv local 3.11

# Remove old venv
rm -rf .venv

# Create new venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip3 install -e ".[dev]"
```

## Verification

After installation, verify your Python version:

```bash
source .venv/bin/activate
python3 --version  # Should show 3.10 or higher
```
