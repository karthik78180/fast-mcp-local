# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastMCP server implementation with document management, Vert.x code generation, migration guidance, and code scoring capabilities. The server automatically loads markdown documents from the `docs/` folder, stores them in a SQLite database with token counts (using tiktoken), and provides tools to query documents, generate Vert.x verticles, execute OpenRewrite migrations, and score codebases against best practices.

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
  vertx/                    # Vert.x templates and guides
    templates/              # Verticle code templates
    schemas/                # Verticle metadata
  migrations/               # Migration guides
    v1-to-v2/               # V1 to V2 migration
    schemas/                # Migration metadata
  patterns/                 # Code scoring patterns
    vertx/                  # Vert.x patterns
      scoring-rules.json    # Scoring rules definition
      best-practices.md     # Best practices guide
      anti-patterns.md      # Anti-patterns guide
src/fast_mcp_local/
  __init__.py               # Package initialization
  server.py                 # Main MCP server with tools
  database.py               # SQLite database operations
  loader.py                 # Document loading and token counting
  template_extractor.py     # Template parsing
  metadata.py               # Verticle metadata
  migration.py              # Migration guide management
  pattern_matcher.py        # Pattern matching engine
  scorer.py                 # Code scoring module
  cli.py                    # CLI wrapper
tests/
  test_server.py            # Server tool tests
  test_database.py          # Database operation tests
  test_loader.py            # Document loader tests
  test_pattern_matcher.py   # Pattern matcher tests
  test_scorer.py            # Scorer tests
  ... (120 tests total)
documents.db                # SQLite database (auto-generated, gitignored)
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

- **template_extractor.py**: Template parsing for Vert.x code generation
  - Extracts code blocks from markdown templates
  - Supports Java, JSON, and deployment examples

- **metadata.py**: Verticle metadata management
  - Loads verticle metadata from JSON schemas
  - Provides verticle type listings

- **migration.py**: Migration guide management
  - Lists available migrations
  - Provides metadata and step-by-step guides
  - Supports OpenRewrite integration

- **pattern_matcher.py**: Pattern matching engine
  - Regex-based code pattern matching
  - Text presence/absence checking
  - File and directory scanning
  - Supports multiple file extensions

- **scorer.py**: Code scoring module
  - Rule-based codebase analysis
  - Category-weighted scoring system
  - Violation tracking and reporting
  - Markdown compliance report generation
  - Currently supports: `vertx-best-practices` pattern

- **cli.py**: Command-line interface wrapper
  - Provides CLI access to all MCP tools
  - GitHub Copilot integration support

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
