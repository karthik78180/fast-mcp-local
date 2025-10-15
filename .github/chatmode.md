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
    },
    {
      "name": "list_migrations",
      "description": "List all available migration guides with metadata",
      "command": "mcp list-migrations",
      "properties": {},
      "returns": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "migration_id": {"type": "string"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "source_version": {"type": "string"},
            "target_version": {"type": "string"},
            "openrewrite_dependency": {"type": "object"},
            "prerequisites": {"type": "object"},
            "total_steps": {"type": "integer"},
            "estimated_time": {"type": "string"}
          }
        }
      },
      "use_cases": [
        "User asks about available migrations",
        "User wants to see migration options",
        "User asks 'what migrations can I run?'"
      ],
      "examples": [
        {
          "user_query": "What migrations are available?",
          "command": "mcp list-migrations",
          "action": "List all migrations with versions and descriptions"
        }
      ]
    },
    {
      "name": "get_migration_metadata",
      "description": "Get migration metadata including versions, dependencies, prerequisites, and steps count",
      "command": "mcp migration-info {migration_id}",
      "properties": {
        "migration_id": {
          "type": "string",
          "description": "Migration identifier",
          "required": true,
          "examples": ["v1-to-v2"]
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "migration_id": {"type": "string"},
          "name": {"type": "string"},
          "description": {"type": "string"},
          "source_version": {"type": "string"},
          "target_version": {"type": "string"},
          "openrewrite_dependency": {
            "type": "object",
            "properties": {
              "group": {"type": "string"},
              "artifact": {"type": "string"},
              "version": {"type": "string"},
              "recipe_class": {"type": "string"}
            }
          },
          "prerequisites": {"type": "object"},
          "total_steps": {"type": "integer"},
          "estimated_time": {"type": "string"}
        }
      },
      "use_cases": [
        "User wants to know migration requirements",
        "User asks about migration dependencies",
        "User wants to see migration overview"
      ],
      "examples": [
        {
          "user_query": "What are the requirements for v1 to v2 migration?",
          "command": "mcp migration-info v1-to-v2",
          "action": "Show prerequisites, dependencies, and estimated time"
        }
      ]
    },
    {
      "name": "get_migration_guide",
      "description": "Get complete migration guide with all documentation including overview, steps, and gradle setup",
      "command": "mcp migration-guide {migration_id}",
      "properties": {
        "migration_id": {
          "type": "string",
          "description": "Migration identifier",
          "required": true,
          "examples": ["v1-to-v2"]
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "migration_id": {"type": "string"},
          "metadata": {"type": "object"},
          "guide": {"type": "string", "description": "Overview and migration guide markdown"},
          "steps": {"type": "string", "description": "Step-by-step instructions markdown"},
          "gradle_setup": {"type": "string", "description": "Gradle configuration reference"}
        }
      },
      "use_cases": [
        "User wants complete migration documentation",
        "User asks for full migration guide",
        "User needs all migration information"
      ],
      "examples": [
        {
          "user_query": "Show me the complete v1 to v2 migration guide",
          "command": "mcp migration-guide v1-to-v2",
          "action": "Present full migration guide with all sections"
        }
      ]
    },
    {
      "name": "get_migration_step",
      "description": "Get specific step instructions from migration guide with detailed actions and troubleshooting",
      "command": "mcp migration-step {migration_id} {step_number}",
      "properties": {
        "migration_id": {
          "type": "string",
          "description": "Migration identifier",
          "required": true,
          "examples": ["v1-to-v2"]
        },
        "step_number": {
          "type": "integer",
          "description": "Step number (1-based)",
          "required": true,
          "minimum": 1,
          "examples": [1, 2, 3, 4, 5]
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "migration_id": {"type": "string"},
          "step_number": {"type": "integer"},
          "total_steps": {"type": "integer"},
          "content": {"type": "string", "description": "Step instructions in markdown"}
        }
      },
      "use_cases": [
        "User wants to follow migration step-by-step",
        "User asks for specific migration step",
        "User needs detailed instructions for current step"
      ],
      "examples": [
        {
          "user_query": "Show me step 1 of the v1 to v2 migration",
          "command": "mcp migration-step v1-to-v2 1",
          "action": "Display step 1 instructions with actions and verification"
        },
        {
          "user_query": "What's the next step in migration?",
          "command": "mcp migration-step v1-to-v2 {current_step + 1}",
          "action": "Show next step instructions and guide user through it"
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
  ├─ Migration-related?
  │   ├─ "what migrations", "available migrations"?
  │   │   └─ USE: list_migrations
  │   │
  │   ├─ "migration requirements", "migration info"?
  │   │   └─ USE: get_migration_metadata
  │   │
  │   ├─ "full migration guide", "complete guide"?
  │   │   └─ USE: get_migration_guide
  │   │
  │   └─ "step X", "next step", specific step number?
  │       └─ USE: get_migration_step
  │
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

- **Project**: Fast MCP Local - MCP server with document management, Vert.x code generation, and OpenRewrite migrations
- **87 tests**: Comprehensive test coverage
- **14 documents**: Indexed markdown documentation (including migration guides)
- **2 verticle types**: postgres, http (extensible)
- **1 migration**: v1-to-v2 OpenRewrite migration (extensible)
- **Template-based**: No LLM/AI in generation, pure template extraction
- **Gradle-first**: All dependencies in Gradle format
- **Migration support**: Guided OpenRewrite-based code migrations with step-by-step instructions

## Performance Notes

- All commands return JSON
- Average response time: < 100ms
- Database: SQLite (documents.db)
- Token counting: tiktoken (GPT-4 cl100k_base encoding)

## File Locations

- Verticle templates: `docs/vertx/templates/`
- Verticle schemas: `docs/vertx/schemas/`
- Migration guides: `docs/migrations/*/`
- Migration schemas: `docs/migrations/schemas/`
- Tests: `tests/` (87 tests)
- CLI: `src/fast_mcp_local/cli.py`
- Server: `src/fast_mcp_local/server.py`

---

**Remember**: Always execute commands, parse JSON responses, and format results for human readability!
