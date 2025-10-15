# Fast MCP Local

A FastMCP server that provides intelligent document management and Vert.x verticle code generation capabilities.

## What This Does

Fast MCP Local is a Model Context Protocol (MCP) server that provides:

1. **Document Management**: Automatically indexes markdown documentation with SQLite storage and token counting
2. **Intelligent Search**: Full-text search across indexed documents with contextual snippets
3. **Vert.x Code Generation**: Template-based generation of Vert.x verticle code with Gradle dependencies

## Features

- 📚 Recursive markdown document indexing
- 🔍 Fast full-text search with SQLite
- 🎯 Token counting using tiktoken (GPT-4 encoding)
- ⚡ Vert.x verticle code generation (PostgreSQL, HTTP, and more)
- 🏗️ Template-based approach (no LLM/AI required)
- 📦 Gradle dependency management
- ✅ 54 comprehensive tests

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
pytest           # Run all tests
pytest -v        # Verbose output
pytest --cov     # With coverage report
```

Currently: **54 tests passing** covering document management, template extraction, metadata loading, and verticle generation.

## Tools

### Document Query Tools

- `search_documents(query: str, limit: int = 10)`: Search documents by content
- `get_all_documents()`: Get a list of all documents with metadata
- `get_document(filename: str)`: Get the full content of a specific document

### Vert.x Verticle Generation Tools

- `generate_verticle(verticle_type: str)`: Generate Vert.x verticle code from templates
  - Returns verticle Java code, Gradle dependencies, configuration example, and deployment code
  - Supported types: `postgres`, `http`
  - Example: `generate_verticle("postgres")` returns a complete PostgreSQL verticle implementation

- `list_verticle_types()`: List all available verticle templates
  - Returns metadata for all available verticle types with descriptions and dependencies

See [docs/vertx/README.md](docs/vertx/README.md) for more information on Vert.x templates.

## Architecture

For detailed architecture documentation, see:
- [ARCHITECTURE.md](ARCHITECTURE.md) - Overall system design with Mermaid diagrams
- [ARCHITECTURE-VERTX-SIMPLE.md](ARCHITECTURE-VERTX-SIMPLE.md) - Vert.x extension architecture

## Project Structure

```
fast-mcp-local/
├── docs/                          # Documentation source
│   ├── *.md                       # General documentation
│   └── vertx/                     # Vert.x templates
│       ├── templates/             # Verticle code templates
│       ├── schemas/               # Verticle metadata (JSON)
│       └── deployment-config.md   # Deployment guide
├── src/fast_mcp_local/
│   ├── server.py                  # Main MCP server
│   ├── database.py                # SQLite operations
│   ├── loader.py                  # Document loader
│   ├── template_extractor.py      # Template parsing
│   └── metadata.py                # Verticle metadata
├── tests/                         # Test suite (54 tests)
└── documents.db                   # SQLite database (auto-generated)
```

## Development

### Adding New MCP Tools

To add a new tool, edit `src/fast_mcp_local/server.py`:

```python
def my_new_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return result

# Register with MCP
mcp.tool()(my_new_tool)
```

### Adding New Verticle Templates

1. Create `docs/vertx/templates/[type]-verticle.md` with template content
2. Create `docs/vertx/schemas/[type].json` with metadata
3. Restart server - template automatically available

## License

MIT License
