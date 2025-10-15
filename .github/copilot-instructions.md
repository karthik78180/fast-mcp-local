# GitHub Copilot Workspace Instructions

## Project Overview

This is **Fast MCP Local**, a Model Context Protocol (MCP) server that provides:
1. Document management with intelligent search
2. Vert.x verticle code generation from templates
3. SQLite-based document indexing with token counting

## Available Tools (via CLI)

You have access to the following CLI commands to help with development:

### 1. Search Documentation
```bash
python3 -m fast_mcp_local.cli search "query" [--limit N]
```
**Use when:** User asks about concepts, patterns, or how to do something
**Returns:** JSON with relevant document snippets

**Examples:**
- "How do I deploy verticles?" → `python3 -m fast_mcp_local.cli search "deployment"`
- "Show postgres examples" → `python3 -m fast_mcp_local.cli search "postgres"`

### 2. List All Documents
```bash
python3 -m fast_mcp_local.cli list-docs
```
**Use when:** User wants to know what documentation is available
**Returns:** JSON with all document filenames and metadata

### 3. Get Document Content
```bash
python3 -m fast_mcp_local.cli get "filename"
```
**Use when:** User wants full content of a specific document
**Returns:** JSON with complete document content

**Examples:**
- `python3 -m fast_mcp_local.cli get "vertx/deployment-config.md"`
- `python3 -m fast_mcp_local.cli get "vertx/templates/postgres-verticle.md"`

### 4. Generate Verticle Code
```bash
python3 -m fast_mcp_local.cli generate <verticle_type>
```
**Use when:** User asks to generate Vert.x verticle code
**Available types:** `postgres`, `http`
**Returns:** JSON with Java code, Gradle dependencies, config, and deployment example

**Examples:**
- "Generate a postgres verticle" → `python3 -m fast_mcp_local.cli generate postgres`
- "Create an HTTP server verticle" → `python3 -m fast_mcp_local.cli generate http`

### 5. List Verticle Types
```bash
python3 -m fast_mcp_local.cli list-verticles
```
**Use when:** User wants to know what verticle types are available
**Returns:** JSON with all available verticle templates and descriptions

## Usage Guidelines for Copilot

### When to Use These Tools

**Always use these tools before answering questions about:**
- Vert.x verticle patterns
- Deployment configurations
- Available templates
- How to configure specific verticles
- Code generation capabilities

**Workflow:**
1. User asks a question → Search docs first
2. User wants code → Use generate command
3. Provide answer based on tool output
4. Include relevant code snippets from tool results

### Example Conversations

**User:** "How do I create a PostgreSQL verticle?"

**Copilot should:**
1. Run: `python3 -m fast_mcp_local.cli generate postgres`
2. Parse the JSON response
3. Show the user:
   - The verticle Java code
   - Gradle dependencies needed
   - Configuration example
   - Deployment instructions

**User:** "What deployment options are available?"

**Copilot should:**
1. Run: `python3 -m fast_mcp_local.cli search "deployment" --limit 3`
2. Read the snippets
3. If needed: `python3 -m fast_mcp_local.cli get "vertx/deployment-config.md"`
4. Provide a summary with examples

**User:** "Show me all available verticle types"

**Copilot should:**
1. Run: `python3 -m fast_mcp_local.cli list-verticles`
2. Parse JSON
3. Present as a formatted list with descriptions

## Response Format

When using tool output, structure your response like this:

```markdown
I found relevant information. Let me show you:

[Summary of the answer]

Here's the code/configuration:

```[language]
[code from tool output]
```

You'll also need these dependencies:
- [list from tool output]

For deployment, [deployment instructions from tool output]
```

## Important Notes

1. **Always run tools from project root directory**
2. **Parse JSON responses** - all tools return JSON
3. **Check for errors** - tool output may contain `{"error": "..."}`
4. **Provide context** - explain what the generated code does
5. **Include dependencies** - always show Gradle dependencies for verticles

## Project Structure

```
fast-mcp-local/
├── docs/                    # Documentation source
│   └── vertx/              # Vert.x templates
│       ├── templates/      # Verticle code templates
│       └── schemas/        # Verticle metadata
├── src/fast_mcp_local/
│   ├── server.py           # MCP server
│   ├── cli.py              # CLI wrapper (use this!)
│   └── ...
└── tests/
```

## Testing Tools

Before using a tool in a response, you can test it:

```bash
# Test search
python3 -m fast_mcp_local.cli search "test query"

# Test generation
python3 -m fast_mcp_local.cli generate postgres

# Test listing
python3 -m fast_mcp_local.cli list-docs
```

## Error Handling

If a tool returns an error:
1. Check the error message in JSON response
2. Suggest alternative approach to user
3. Explain what went wrong

Example:
```json
{"error": "Unknown verticle type: redis", "available_types": ["postgres", "http"]}
```
→ Tell user: "Redis verticle template isn't available yet. Available types are: postgres, http"

## Architecture Context

- **Document indexing:** Markdown files in `docs/` are automatically indexed
- **Token counting:** Uses tiktoken (GPT-4 encoding) for all documents
- **Template-based generation:** No LLM involved, pure template extraction
- **Gradle-first:** All dependencies are in Gradle format
- **54 tests:** Comprehensive test coverage

## When User Asks to Add New Features

1. Search existing docs to understand current patterns
2. Check if similar functionality exists
3. Follow existing code structure
4. Run tests after changes: `pytest`
5. Use existing templates as reference

## Common Patterns

**Search then Generate:**
```bash
# First understand what's available
python3 -m fast_mcp_local.cli search "postgres"

# Then generate code
python3 -m fast_mcp_local.cli generate postgres
```

**Get specific details:**
```bash
# List what's available
python3 -m fast_mcp_local.cli list-docs

# Get full content
python3 -m fast_mcp_local.cli get "vertx/deployment-config.md"
```

---

**Remember:** These tools give you access to the project's documentation and code generation capabilities. Use them proactively to provide accurate, contextual responses!
