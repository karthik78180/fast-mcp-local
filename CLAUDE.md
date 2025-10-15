# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A minimal FastMCP server implementation using Python. This project provides a simple MCP server with basic tools for demonstration and testing purposes.

## Requirements

- Python 3.10 or higher (required by FastMCP)

## Commands

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e ".[dev]"
```

### Running the Server
```bash
python3 -m fast_mcp_local.server
```

### Testing
```bash
pytest                    # Run all tests
pytest tests/test_server.py  # Run specific test file
pytest -v                 # Verbose output
```

### Interactive Testing with MCP Inspector
```bash
# Test the server interactively with the MCP Inspector web UI
npx @modelcontextprotocol/inspector python3 -m fast_mcp_local.server
```

This opens a web interface where you can:
- View all available tools
- Invoke tools with parameters
- See responses in real-time

## Architecture

### Project Structure
```
src/fast_mcp_local/
  __init__.py          # Package initialization
  server.py            # Main MCP server with tools
tests/
  test_server.py       # Unit tests for server tools
```

### Key Components

- **server.py**: Contains the FastMCP server instance and tool definitions
- Tools are defined as Python functions decorated with `@mcp.tool()`
- Each tool has type hints and docstrings that define the MCP interface

### Adding New Tools

To add a new tool:
1. Define a function in `src/fast_mcp_local/server.py`
2. Add the `@mcp.tool()` decorator
3. Include type hints and a descriptive docstring
4. Write corresponding unit tests in `tests/test_server.py`

## Dependencies

- **fastmcp**: The FastMCP framework for building MCP servers
- **pytest**: Testing framework
- **pytest-asyncio**: Async support for pytest (for future async tools)
