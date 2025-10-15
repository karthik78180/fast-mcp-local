# Chat Mode - Tool Definitions

This file defines available tools for AI assistants (GitHub Copilot, Claude, etc.) to help with Fast MCP Local development.

## Tool Schema

```json
{
  "tools": [
    {
      "name": "search_documents",
      "description": "Search through indexed markdown documentation with contextual snippets",
      "command": "mcp search \"{query}\" --limit {limit}",
      "properties": {
        "query": {
          "type": "string",
          "description": "Search query to find in documents",
          "required": true,
          "examples": ["postgres verticle", "deployment patterns", "connection pooling"]
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of results to return",
          "required": false,
          "default": 10,
          "minimum": 1,
          "maximum": 50
        }
      },
      "returns": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "integer"},
            "filename": {"type": "string"},
            "snippet": {"type": "string"},
            "tokens": {"type": "integer"},
            "created_at": {"type": "string"}
          }
        }
      },
      "use_cases": [
        "User asks about concepts or patterns",
        "User wants to find documentation on a topic",
        "User asks 'how do I...' questions"
      ],
      "examples": [
        {
          "user_query": "How do I deploy verticles?",
          "command": "mcp search \"deployment\" --limit 5",
          "action": "Search for deployment documentation and provide relevant examples"
        },
        {
          "user_query": "Show me postgres examples",
          "command": "mcp search \"postgres\" --limit 3",
          "action": "Find postgres-related documentation and show code examples"
        }
      ]
    },
    {
      "name": "list_documents",
      "description": "List all indexed documentation files with metadata",
      "command": "mcp list-docs",
      "properties": {},
      "returns": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "integer"},
            "filename": {"type": "string"},
            "tokens": {"type": "integer"},
            "created_at": {"type": "string"}
          }
        }
      },
      "use_cases": [
        "User wants to see available documentation",
        "User asks 'what docs do you have?'",
        "User wants to browse available content"
      ],
      "examples": [
        {
          "user_query": "What documentation is available?",
          "command": "mcp list-docs",
          "action": "List all documents and present as a formatted list"
        }
      ]
    },
    {
      "name": "get_document",
      "description": "Retrieve full content of a specific document by filename",
      "command": "mcp get \"{filename}\"",
      "properties": {
        "filename": {
          "type": "string",
          "description": "Relative path to document from docs directory",
          "required": true,
          "examples": [
            "vertx/deployment-config.md",
            "vertx/templates/postgres-verticle.md",
            "mcp-overview.md"
          ]
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "filename": {"type": "string"},
          "content": {"type": "string"},
          "tokens": {"type": "integer"},
          "created_at": {"type": "string"}
        }
      },
      "use_cases": [
        "User wants full details of a specific document",
        "Search results show relevant file that needs full content",
        "User asks for complete configuration or code example"
      ],
      "examples": [
        {
          "user_query": "Show me the full deployment configuration guide",
          "command": "mcp get \"vertx/deployment-config.md\"",
          "action": "Retrieve and present full document content"
        }
      ]
    },
    {
      "name": "generate_verticle",
      "description": "Generate complete Vert.x verticle code from template including Java code, Gradle dependencies, configuration, and deployment instructions",
      "command": "mcp generate {type}",
      "properties": {
        "type": {
          "type": "string",
          "description": "Type of verticle to generate",
          "required": true,
          "enum": ["postgres", "http"],
          "examples": ["postgres", "http"]
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "type": {"type": "string"},
          "name": {"type": "string"},
          "description": {"type": "string"},
          "verticle_code": {"type": "string", "description": "Complete Java source code"},
          "gradle_dependencies": {"type": "array", "items": {"type": "string"}},
          "config_example": {"type": "object", "description": "JSON configuration"},
          "deployment_example": {"type": "string", "description": "Java deployment code"},
          "use_cases": {"type": "array", "items": {"type": "string"}}
        }
      },
      "use_cases": [
        "User asks to generate verticle code",
        "User wants to create a new Vert.x component",
        "User needs code template for specific verticle type"
      ],
      "examples": [
        {
          "user_query": "Generate a PostgreSQL verticle",
          "command": "mcp generate postgres",
          "action": "Generate postgres verticle and present formatted code with dependencies"
        },
        {
          "user_query": "Create an HTTP server verticle",
          "command": "mcp generate http",
          "action": "Generate HTTP verticle with routing examples and show complete setup"
        }
      ]
    },
    {
      "name": "list_verticle_types",
      "description": "List all available verticle template types with descriptions and dependencies",
      "command": "mcp list-verticles",
      "properties": {},
      "returns": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "type": {"type": "string"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "gradle_deps": {"type": "array", "items": {"type": "string"}}
          }
        }
      },
      "use_cases": [
        "User asks what verticle types are available",
        "User wants to see generation options",
        "User asks 'what can you generate?'"
      ],
      "examples": [
        {
          "user_query": "What verticle types can you generate?",
          "command": "mcp list-verticles",
          "action": "List all available types with descriptions"
        }
      ]
    },
    {
      "name": "quick_search",
      "description": "Quick search for documentation (alias for search with limit=5)",
      "command": "mcp ask \"{question}\"",
      "properties": {
        "question": {
          "type": "string",
          "description": "Quick question or search query",
          "required": true,
          "examples": ["postgres pooling", "http middleware", "deployment options"]
        }
      },
      "returns": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "integer"},
            "filename": {"type": "string"},
            "snippet": {"type": "string"},
            "tokens": {"type": "integer"},
            "created_at": {"type": "string"}
          }
        },
        "maxItems": 5
      },
      "use_cases": [
        "User asks a quick question",
        "User wants fast answer without full search",
        "User prefixes with 'how', 'what', 'show me'"
      ],
      "examples": [
        {
          "user_query": "How does postgres connection pooling work?",
          "command": "mcp ask \"postgres connection pooling\"",
          "action": "Quick search and provide concise answer from results"
        }
      ]
    }
  ]
}
```

## Usage Instructions

### For AI Assistants (Copilot, Claude, etc.)

When a user asks a question:

1. **Identify the appropriate tool** from the schema above
2. **Check use_cases** to match user intent
3. **Build the command** using the command template and properties
4. **Execute the command** in the terminal
5. **Parse the JSON response**
6. **Format and present** the results to the user

### Response Format Template

When presenting generated verticle code:

```markdown
## {Verticle Name}

{Description from response}

### Implementation

\`\`\`java
{verticle_code}
\`\`\`

### Gradle Dependencies

\`\`\`gradle
dependencies {
    {gradle_dependencies as individual lines}
}
\`\`\`

### Configuration

\`\`\`json
{config_example}
\`\`\`

### Deployment

\`\`\`java
{deployment_example}
\`\`\`
```

When presenting search results:

```markdown
I found relevant documentation:

{For each result:}
**{filename}**
{snippet}

{If more detail needed, suggest using get_document with specific filename}
```

## Tool Selection Decision Tree

```
User asks a question
  ├─ Contains "generate", "create", "make" + verticle type?
  │   └─ USE: generate_verticle
  │
  ├─ Asks "what types", "available", "options"?
  │   └─ USE: list_verticle_types
  │
  ├─ Asks "how to", "show me", pattern/concept question?
  │   ├─ Quick answer needed?
  │   │   └─ USE: quick_search (ask)
  │   └─ Detailed answer needed?
  │       └─ USE: search_documents
  │
  ├─ Wants "full", "complete", "entire" specific document?
  │   └─ USE: get_document
  │
  └─ Wants to see "all docs", "available docs"?
      └─ USE: list_documents
```

## Error Handling

If a tool returns an error in JSON:

```json
{"error": "Error message here", "available_types": [...]}
```

**Action**: Explain the error to the user and suggest alternatives based on `available_types` or other hints in the error response.

## Context

- **Project**: Fast MCP Local - MCP server with document management and Vert.x code generation
- **69 tests**: Comprehensive test coverage
- **11 documents**: Indexed markdown documentation
- **2 verticle types**: postgres, http (extensible)
- **Template-based**: No LLM/AI in generation, pure template extraction
- **Gradle-first**: All dependencies in Gradle format

## Performance Notes

- All commands return JSON
- Average response time: < 100ms
- Database: SQLite (documents.db)
- Token counting: tiktoken (GPT-4 cl100k_base encoding)

## File Locations

- Templates: `docs/vertx/templates/`
- Schemas: `docs/vertx/schemas/`
- Deployment guide: `docs/vertx/deployment-config.md`
- Tests: `tests/` (69 tests)
- CLI: `src/fast_mcp_local/cli.py`

---

**Remember**: Always execute commands, parse JSON responses, and format results for human readability!
