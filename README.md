# Fast MCP Local

A minimal FastMCP server implementation with basic tools.

## Requirements

- Python 3.10 or higher (required by FastMCP)

## Setup

1. Create a virtual environment (use python3.10, python3.11, python3.12, or python3.13):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip3 install -e ".[dev]"
```

## Running the Server

```bash
python3 -m fast_mcp_local.server
```

## Running Tests

```bash
pytest
```

## Tools

The server provides document query tools:

- `search_documents(query: str, limit: int = 10)`: Search documents by content
- `get_all_documents()`: Get a list of all documents with metadata
- `get_document(filename: str)`: Get the full content of a specific document

## Development

To add new tools, edit `src/fast_mcp_local/server.py` and decorate functions with `@mcp.tool()`.
