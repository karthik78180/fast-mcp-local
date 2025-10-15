# File Dependencies for MCP Server Features

## Current Features (Minimal Version)

### ✅ Feature 1: Code Generation (`generate_verticle`)

**What it does**: Generates verticle Java code from templates

**Files it relies on**:

```
docs/vertx/
├── schemas/                    # Metadata for each template
│   ├── platform-async.json     # AsyncHandler metadata
│   ├── platform-sync.json      # SyncHandler metadata
│   ├── platform-multipart.json # MultipartHandler metadata
│   ├── postgres.json           # Standard PostgreSQL metadata
│   └── http.json               # Standard HTTP metadata
│
└── templates/                  # Template markdown files
    ├── platform-async-handler.md     # AsyncHandler code template
    ├── platform-sync-handler.md      # SyncHandler code template
    ├── platform-multipart-handler.md # MultipartHandler code template
    ├── postgres-verticle.md          # Standard PostgreSQL template
    └── http-verticle.md              # Standard HTTP template
```

**How it works**:
1. Read metadata from `schemas/{type}.json` to get template file path
2. Read template from `templates/{template_file}`
3. Extract Java code, Gradle dependencies, and config from markdown
4. Return as JSON

**Example**:
```bash
mcp generate platform-async
# Reads: schemas/platform-async.json
# Reads: templates/platform-async-handler.md
# Returns: Java code + dependencies + config
```

---

### ✅ Feature 2: Document Search (`search_documents`)

**What it does**: Full-text search across all documentation

**Files it relies on**:

```
docs/                           # Searches EVERYTHING in docs/ recursively
├── vertx/
│   ├── templates/*.md          # Platform templates
│   ├── README.md               # Vertx documentation
│   └── deployment-config.md    # Deployment guide
├── company/                    # YOUR COMPANY DOCS (add here!)
│   ├── README.md
│   ├── platform-overview.md    # Add your docs
│   ├── configuration-guide.md  # Add your docs
│   └── examples/*.md           # Add your docs
├── building-tools.md           # General docs
├── fastmcp-guide.md            # MCP guide
└── mcp-overview.md             # MCP overview
```

**How it works**:
1. On startup, scans all `.md` files in `docs/` recursively
2. Indexes content in SQLite database (`documents.db`)
3. Full-text search using SQLite FTS5

**Example**:
```bash
mcp search "async handler"
# Searches all markdown files
# Returns matching docs with snippets
```

---

## ❌ Removed Features (Not in Minimal Version)

### Migration System (Removed)

**Previously relied on**:
```
docs/migrations/
├── schemas/
│   └── v1-to-v2.json           # Migration metadata
└── v1-to-v2/
    ├── migration-guide.md       # Overview
    ├── steps.md                 # Step-by-step
    └── gradle-setup.md          # Gradle config
```

**Status**: ❌ Removed in minimal version (too complex for 2-day hackathon)

**To restore**: Check branch `feature/platform-handler-templates` or git history

---

### Code Scoring System (Removed)

**Previously relied on**:
```
docs/patterns/
└── vertx/
    ├── scoring-rules.json       # Scoring rules
    ├── best-practices.md        # Best practices
    └── anti-patterns.md         # Anti-patterns
```

**Status**: ❌ Removed in minimal version (too complex for 2-day hackathon)

**To restore**: Check branch `feature/platform-handler-templates` or git history

---

## For Your Hackathon Team

### To Add Company Templates:

**Step 1**: Create template markdown file
```bash
vi docs/vertx/templates/company-user-crud.md
```

**Step 2**: Create metadata JSON file
```bash
vi docs/vertx/schemas/company-user-crud.json
```

**Step 3**: Test it works
```bash
mcp list-types              # Should see your template
mcp generate company-user-crud  # Should generate code
```

### To Add Company Documentation:

**Step 1**: Create markdown files
```bash
vi docs/company/platform-overview.md
vi docs/company/best-practices.md
vi docs/company/examples/user-crud-example.md
```

**Step 2**: Re-index documents
```python
from fast_mcp_local.loader import load_documents
from fast_mcp_local.database import init_db

init_db()
load_documents("docs")
```

**Step 3**: Test it works
```bash
mcp search "company platform"
mcp list-docs
```

---

## File Structure Summary

### Minimal Version (Current):

```
fast-mcp-local/
├── src/fast_mcp_local/
│   ├── server.py              # MCP server (5 tools)
│   ├── cli.py                 # CLI wrapper (7 commands)
│   ├── database.py            # SQLite document storage
│   ├── loader.py              # Document indexing
│   ├── template_extractor.py  # Extract code from markdown
│   └── metadata.py            # Load template metadata
│
├── docs/
│   ├── vertx/
│   │   ├── templates/         # 5 verticle templates (.md)
│   │   └── schemas/           # 5 metadata files (.json)
│   └── company/               # YOUR DOCS GO HERE
│
├── documents.db               # SQLite database (auto-generated)
└── README_HACKATHON.md        # Start here!
```

### Key Files for Hackathon:

**You will edit**:
- ✅ `docs/vertx/templates/company-*.md` - Add company templates
- ✅ `docs/vertx/schemas/company-*.json` - Add template metadata
- ✅ `docs/company/*.md` - Add company documentation

**You won't edit**:
- ❌ `src/fast_mcp_local/server.py` - Already has all features
- ❌ `src/fast_mcp_local/cli.py` - Already has all commands
- ❌ Database files - Auto-managed

---

## Quick Reference

| Feature | Depends On | Action |
|---------|------------|--------|
| `generate_verticle` | `docs/vertx/schemas/*.json` + `docs/vertx/templates/*.md` | Add 2 files per template |
| `search_documents` | All `.md` files in `docs/` | Add `.md` files anywhere in `docs/` |
| Database indexing | `docs/` folder | Auto-scans on startup |

---

**Last Updated**: After minimal refactor
**Branch**: `feature/minimal-hackathon-demo`
