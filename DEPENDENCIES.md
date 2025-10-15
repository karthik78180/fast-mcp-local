# File Dependencies for MCP Server Features

## Current Features (Full Version)

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

### ✅ Feature 3: Migration Guides (`list_migrations`, `get_migration_guide`)

**What it does**: Provides step-by-step OpenRewrite migration guides

**Files it relies on**:

```
docs/migrations/
├── schemas/                    # Migration metadata
│   └── v1-to-v2.json          # V1 to V2 migration metadata
│
└── v1-to-v2/                  # Migration documentation
    ├── migration-guide.md      # Overview and introduction
    ├── steps.md                # Step-by-step instructions
    └── gradle-setup.md         # Gradle configuration reference
```

**How it works**:
1. Read metadata from `schemas/{migration-id}.json`
2. Read guide docs from `migrations/{migration-id}/`
3. Extract specific steps from `steps.md` using regex
4. Return as JSON

**Example**:
```bash
mcp list-migrations
# Lists all migrations from schemas/*.json

mcp migration-guide v1-to-v2
# Reads: schemas/v1-to-v2.json + v1-to-v2/*.md
# Returns: Complete guide with all docs

mcp migration-step v1-to-v2 1
# Extracts Step 1 from v1-to-v2/steps.md
```

---

### ✅ Feature 4: Code Scoring (`score_codebase`, `get_compliance_report`)

**What it does**: Analyzes code against best practices and anti-patterns

**Files it relies on**:

```
docs/patterns/
└── vertx/                      # Vert.x scoring patterns
    ├── scoring-rules.json      # Rule definitions with patterns
    ├── best-practices.md       # Best practices guide
    └── anti-patterns.md        # Anti-patterns guide
```

**How it works**:
1. Read scoring rules from `patterns/{category}/scoring-rules.json`
2. Scan codebase files (Java, etc.)
3. Match patterns using regex
4. Calculate score based on rule weights
5. Generate compliance report

**Example**:
```bash
mcp list-patterns
# Lists all patterns from patterns/**/scoring-rules.json

mcp score ./MyVerticle.java --pattern vertx-best-practices
# Reads: patterns/vertx/scoring-rules.json
# Scans: MyVerticle.java
# Returns: Score, violations, recommendations

mcp compliance ./verticles/ --pattern vertx-best-practices
# Same but returns markdown report
```

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

### Full Version (Current):

```
fast-mcp-local/
├── src/fast_mcp_local/
│   ├── server.py              # MCP server (13 tools)
│   ├── cli.py                 # CLI wrapper (15 commands)
│   ├── database.py            # SQLite document storage
│   ├── loader.py              # Document indexing
│   ├── template_extractor.py  # Extract code from markdown
│   ├── metadata.py            # Load template metadata
│   ├── migration.py           # Migration guide management
│   ├── scorer.py              # Code scoring module
│   └── pattern_matcher.py     # Pattern matching engine
│
├── docs/
│   ├── vertx/
│   │   ├── templates/         # 5 verticle templates (.md)
│   │   └── schemas/           # 5 metadata files (.json)
│   ├── migrations/            # Migration guides
│   │   ├── schemas/           # Migration metadata (.json)
│   │   └── v1-to-v2/          # Migration docs (.md)
│   ├── patterns/              # Code scoring patterns
│   │   └── vertx/             # Vert.x patterns
│   └── company/               # YOUR DOCS GO HERE
│
├── documents.db               # SQLite database (auto-generated)
├── README_HACKATHON.md        # Hackathon guide
└── DEPENDENCIES.md            # This file
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
| `list_migrations` | `docs/migrations/schemas/*.json` | Add migration metadata JSON |
| `get_migration_guide` | `docs/migrations/{id}/*.md` | Add migration docs (3 files) |
| `score_codebase` | `docs/patterns/**/scoring-rules.json` | Add scoring rules JSON |
| `get_compliance_report` | `docs/patterns/**/scoring-rules.json` + best-practices/anti-patterns `.md` | Add pattern docs |
| Database indexing | `docs/` folder | Auto-scans on startup |

---

**Last Updated**: After restoring migrations and scoring
**Branch**: `feature/minimal-hackathon-demo`
**Status**: Full version with all features
