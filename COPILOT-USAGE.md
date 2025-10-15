# GitHub Copilot Usage Guide

## Quick Reference for Copilot Chat

This document explains how to use the Fast MCP Local CLI with GitHub Copilot Chat.

## Available Commands

### 1. Search Documentation
```bash
mcp search "<query>" --limit <n>
```

**When to use:** User asks about concepts, patterns, or how to do something

**Examples:**
- "How to deploy verticles?" → `mcp search "deployment"`
- "Show postgres configuration" → `mcp search "postgres config"`
- "Explain connection pooling" → `mcp search "connection pooling"`

### 2. Generate Verticle Code
```bash
mcp generate <type>
```

**Available types:** `postgres`, `http`

**When to use:** User wants to generate Vert.x verticle code

**Returns:** Complete verticle with:
- Java source code
- Gradle dependencies
- Configuration example
- Deployment instructions

**Examples:**
- "Create a PostgreSQL verticle" → `mcp generate postgres`
- "Generate HTTP server" → `mcp generate http`

### 3. List Verticle Types
```bash
mcp list-verticles
```

**When to use:** User asks what verticle types are available

**Returns:** JSON with all templates, descriptions, and dependencies

### 4. List All Documents
```bash
mcp list-docs
```

**When to use:** User wants to see available documentation

**Returns:** JSON with all document filenames and metadata

### 5. Get Specific Document
```bash
mcp get "<filename>"
```

**When to use:** User wants full content of a specific document

**Examples:**
- `mcp get "vertx/deployment-config.md"`
- `mcp get "vertx/templates/postgres-verticle.md"`

### 6. Quick Ask
```bash
mcp ask "<question>"
```

**Alias for search** - returns top 5 results

**Examples:**
- `mcp ask "postgres pooling"`
- `mcp ask "http middleware"`

## Example Workflows

### Workflow 1: Generate Verticle

**User:** "I need a PostgreSQL verticle"

**Copilot should:**
1. Execute: `mcp generate postgres`
2. Parse JSON response
3. Present:
   ```markdown
   Here's your PostgreSQL verticle:

   **Java Code:**
   ```java
   [verticle_code from JSON]
   ```

   **Gradle Dependencies:**
   ```gradle
   [dependencies from JSON]
   ```

   **Configuration:**
   ```json
   [config_example from JSON]
   ```

   **Deployment:**
   ```java
   [deployment_example from JSON]
   ```
   ```

### Workflow 2: Answer Question

**User:** "How do I configure postgres connection pooling?"

**Copilot should:**
1. Execute: `mcp search "postgres connection pooling" --limit 3`
2. Read snippets from JSON
3. If more detail needed: `mcp get "<relevant-file>"`
4. Answer with code examples from results

### Workflow 3: List Options

**User:** "What verticle types can I generate?"

**Copilot should:**
1. Execute: `mcp list-verticles`
2. Parse JSON array
3. Present formatted list:
   ```
   Available verticle types:

   1. **postgres** - PostgreSQL Verticle
      Database client for PostgreSQL operations
      Dependencies: vertx-core, vertx-pg-client

   2. **http** - HTTP Server Verticle
      REST API server with Vert.x Web
      Dependencies: vertx-core, vertx-web
   ```

## Response Template

When presenting generated code:

```markdown
## [Verticle Name]

[Brief description]

### Implementation

```java
[verticle code]
```

### Gradle Dependencies

Add to your `build.gradle`:

```gradle
dependencies {
    [list dependencies]
}
```

### Configuration

```json
[config example]
```

### Deployment

```java
[deployment example]
```

### Use Cases

- [list use cases from JSON]
```

## Error Handling

If command returns error:
```json
{"error": "Unknown verticle type: redis", "available_types": ["postgres", "http"]}
```

**Tell user:**
"The redis verticle template isn't available yet. Available types are: postgres, http"

## Tips for Effective Usage

1. **Always parse JSON responses** - all commands return structured JSON
2. **Check for errors first** - look for `{"error": "..."}` in response
3. **Combine search + get** - search to find, get for full details
4. **Use --limit** to control result size
5. **Present code with context** - explain what it does, not just show it

## Common Questions

**Q: "How do I deploy a verticle?"**
→ `mcp search "deployment" --limit 3`
→ If needed: `mcp get "vertx/deployment-config.md"`

**Q: "Show me a postgres verticle"**
→ `mcp generate postgres`

**Q: "What can this tool generate?"**
→ `mcp list-verticles`

**Q: "Find examples of HTTP endpoints"**
→ `mcp search "http endpoints" --limit 5`

## Project Context

- **54 tests** - comprehensive test coverage
- **11 documents** - indexed markdown documentation
- **2 verticle types** - postgres, http (extensible)
- **Template-based** - no LLM, pure extraction
- **Gradle-first** - all dependencies in Gradle format

## File Locations

- **Templates:** `docs/vertx/templates/`
- **Schemas:** `docs/vertx/schemas/`
- **Deployment guide:** `docs/vertx/deployment-config.md`
- **Tests:** `tests/`

---

**Remember:** Execute commands, parse JSON, present formatted results!
