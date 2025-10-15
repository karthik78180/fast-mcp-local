# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastMCP server implementation with document management capabilities. The server automatically loads markdown documents from the `docs/` folder, stores them in a SQLite database with token counts (using tiktoken), and provides tools to query and retrieve document information.

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
docs/                       # Markdown documents (recursively scanned on startup)
  mcp-overview.md
  fastmcp-guide.md
  building-tools.md
  tutorials/                # Nested folders supported
    getting-started.md
    best-practices.md
  api/
    reference/
      tools.md
      resources.md
src/fast_mcp_local/
  __init__.py          # Package initialization
  server.py            # Main MCP server with tools
  database.py          # SQLite database operations
  loader.py            # Document loading and token counting
tests/
  test_server.py       # Server tool tests
  test_database.py     # Database operation tests
  test_loader.py       # Document loader tests
documents.db           # SQLite database (auto-generated, gitignored)
```

### Key Components

- **server.py**: Contains the FastMCP server instance and tool definitions
  - Initializes database and loads documents on startup
  - Provides document query tools and utility tools
  - Tools are defined as Python functions decorated with `@mcp.tool()`

- **database.py**: SQLite database operations
  - `DocumentDatabase` class for managing document storage
  - Methods for inserting, updating, searching, and retrieving documents
  - Supports context manager pattern for safe connection handling

- **loader.py**: Document loading and token counting
  - `DocumentLoader` class for recursively scraping markdown files
  - Uses `glob("**/*.md")` to find files in all subdirectories
  - Stores documents with relative paths (e.g., "tutorials/guide.md")
  - Uses tiktoken for accurate token counting (GPT-4 encoding)
  - Automatically loads documents from `docs/` folder on server startup

- Each tool has type hints and docstrings that define the MCP interface

### Adding New Tools

To add a new tool:
1. Define a function in `src/fast_mcp_local/server.py`
2. Add the `@mcp.tool()` decorator
3. Include type hints and a descriptive docstring
4. Write corresponding unit tests in `tests/test_server.py`

## Dependencies

### Core Dependencies
- **fastmcp**: The FastMCP framework for building MCP servers
- **tiktoken**: Token counting library (GPT-4 encoding)

### Development Dependencies
- **pytest**: Testing framework
- **pytest-asyncio**: Async support for pytest

### Built-in Libraries
- **sqlite3**: Database storage (included with Python)
- **pathlib**: File path operations (included with Python)
