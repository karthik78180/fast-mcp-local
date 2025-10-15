# Fast MCP Local

A FastMCP server that provides intelligent document management, Vert.x verticle code generation, and OpenRewrite-based code migration capabilities.

## What This Does

Fast MCP Local is a Model Context Protocol (MCP) server that provides:

1. **Document Management**: Automatically indexes markdown documentation with SQLite storage and token counting
2. **Intelligent Search**: Full-text search across indexed documents with contextual snippets
3. **Vert.x Code Generation**: Template-based generation of Vert.x verticle code with Gradle dependencies
4. **Migration Guidance**: Step-by-step OpenRewrite migration guides with automated refactoring support

## Features

- 📚 Recursive markdown document indexing
- 🔍 Fast full-text search with SQLite
- 🎯 Token counting using tiktoken (GPT-4 encoding)
- ⚡ Vert.x verticle code generation (PostgreSQL, HTTP, and more)
- 🔄 OpenRewrite migration guides with step-by-step instructions
- 🏗️ Template-based approach (no LLM/AI required)
- 📦 Gradle dependency management
- ✅ 87 comprehensive tests

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

### MCP Server Mode
```bash
python3 -m fast_mcp_local.server
```

### CLI Mode (for GitHub Copilot integration)
```bash
# After installing, use the mcp command
mcp --help
mcp search "postgres verticle"
mcp generate postgres
mcp list-verticles
```

## Running Tests

```bash
pytest           # Run all tests
pytest -v        # Verbose output
pytest --cov     # With coverage report
```

Currently: **87 tests passing** covering document management, template extraction, metadata loading, verticle generation, migration guides, and CLI interface.

## Tools

### MCP Tools (Server Mode)

**Document Query Tools:**
- `search_documents(query: str, limit: int = 10)`: Search documents by content
- `get_all_documents()`: Get a list of all documents with metadata
- `get_document(filename: str)`: Get the full content of a specific document

**Vert.x Verticle Generation Tools:**
- `generate_verticle(verticle_type: str)`: Generate Vert.x verticle code from templates
  - Returns verticle Java code, Gradle dependencies, configuration example, and deployment code
  - Supported types: `postgres`, `http`
- `list_verticle_types()`: List all available verticle templates

**Migration Tools:**
- `list_migrations()`: List all available migration guides
- `get_migration_metadata(migration_id: str)`: Get migration metadata (versions, dependencies, steps)
- `get_migration_guide(migration_id: str)`: Get complete migration guide with all documentation
- `get_migration_step(migration_id: str, step_number: int)`: Get specific step instructions

### CLI Commands (Copilot Integration)

```bash
# Search documentation
mcp search "deployment patterns" --limit 5
mcp ask "how to configure postgres"

# List documents
mcp list-docs

# Get specific document
mcp get "vertx/deployment-config.md"

# Generate verticle code
mcp generate postgres
mcp generate http

# List available types
mcp list-verticles

# Migration tools
mcp list-migrations
mcp migration-info v1-to-v2
mcp migration-guide v1-to-v2
mcp migration-step v1-to-v2 1
```

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
│   ├── vertx/                     # Vert.x templates
│   │   ├── templates/             # Verticle code templates
│   │   ├── schemas/               # Verticle metadata (JSON)
│   │   └── deployment-config.md   # Deployment guide
│   └── migrations/                # Migration guides
│       ├── v1-to-v2/              # V1 to V2 migration
│       │   ├── migration-guide.md # Overview
│       │   ├── steps.md           # Step-by-step instructions
│       │   └── gradle-setup.md    # Gradle configuration
│       └── schemas/               # Migration metadata (JSON)
├── src/fast_mcp_local/
│   ├── server.py                  # Main MCP server
│   ├── database.py                # SQLite operations
│   ├── loader.py                  # Document loader
│   ├── template_extractor.py      # Template parsing
│   ├── metadata.py                # Verticle metadata
│   ├── migration.py               # Migration guide management
│   └── cli.py                     # CLI wrapper
├── tests/                         # Test suite (87 tests)
└── documents.db                   # SQLite database (auto-generated)
```

## GitHub Copilot Integration

This project includes GitHub Copilot workspace instructions that allow Copilot to query the documentation and generate code using the CLI tools.

**Setup:**
1. Copilot automatically reads `.github/copilot-instructions.md`
2. Copilot can now execute CLI commands to help you:
   - Search documentation: "Search for postgres examples"
   - Generate code: "Generate an HTTP verticle"
   - Find information: "How do I deploy verticles?"

**Example Copilot conversation:**

```
You: "Generate a PostgreSQL verticle for my project"

Copilot: I'll generate that for you.
[Executes: mcp generate postgres]

Here's your PostgreSQL verticle:

[Shows generated Java code, Gradle dependencies, and configuration]
```

**Note:** This works even when MCP server integration is disabled in your organization, as it uses the CLI wrapper instead.

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

### Adding New Migrations

1. Create migration directory: `docs/migrations/[migration-id]/`
2. Add migration documentation:
   - `migration-guide.md` - Overview and introduction
   - `steps.md` - Step-by-step instructions
   - `gradle-setup.md` - Gradle configuration reference
3. Create metadata: `docs/migrations/schemas/[migration-id].json`
4. Restart server - migration automatically available via CLI and MCP tools

Example migration metadata:
```json
{
  "migration_id": "v1-to-v2",
  "name": "V1 to V2 Migration",
  "description": "Migrate from version 1.x to 2.x",
  "source_version": "1.x",
  "target_version": "2.x",
  "openrewrite_dependency": {
    "group": "com.example",
    "artifact": "migration-recipes",
    "version": "1.0.0",
    "recipe_class": "com.example.V1ToV2Migration"
  },
  "prerequisites": {
    "java_version": "11+",
    "gradle_version": "7.0+"
  },
  "total_steps": 5,
  "estimated_time": "15-20 minutes"
}
```

## License

MIT License
