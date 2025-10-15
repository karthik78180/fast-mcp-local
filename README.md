# Fast MCP Local

A minimal FastMCP server implementation with basic tools.

## Requirements

- Python 3.10 or higher (required by FastMCP)

## Setup

### Quick Setup (Automated)

If you have Python 3.10+ already installed:
```bash
./setup.sh
```

### Manual Setup

1. Install Python 3.13 (if not already installed):
```bash
brew install python@3.13
```

2. Create a virtual environment:
```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip3 install -e ".[dev]"
```

## Running the Server

```bash
source .venv/bin/activate
python3 -m fast_mcp_local.server
```

## Running Tests

```bash
source .venv/bin/activate
pytest           # Run all tests
pytest -v        # Verbose output
```

## Tools

The server provides two basic tools:

- `greet(name: str)`: Greets a person by name
- `add(a: int, b: int)`: Adds two numbers together

## Development

To add new tools:

1. Define a function in `src/fast_mcp_local/server.py` with type hints and docstring
2. Register it with `mcp.tool()(your_function)`
3. Write tests in `tests/test_server.py`
4. Run tests: `pytest`

Example:
```python
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

mcp.tool()(multiply)
```
