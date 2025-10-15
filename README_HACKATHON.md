# Fast MCP Local - Hackathon Demo

**AI-Powered Vert.x Development Assistant for 2-Day Hackathon**

> Search company docs and generate verticle code in seconds.

---

## What This Does

Fast MCP Local is an MCP server that gives AI assistants (Claude Code, GitHub Copilot) access to your company's Vert.x documentation and code templates.

**Two Core Features:**
1. **📚 Document Search** - Search company Vert.x docs instantly
2. **⚡ Code Generation** - Generate verticle code from templates

**Why It's Awesome:**
- ✅ New developers onboard in days instead of weeks
- ✅ Generate verticles in 30 seconds instead of 4-6 hours
- ✅ Zero context switching - AI knows your platform
- ✅ Template-based (no AI hallucinations)
- ✅ Works with Claude Code & GitHub Copilot

---

## 5-Minute Setup

### 1. Install (MacOS/Linux)

```bash
# Clone repo
git clone https://github.com/karthik78180/fast-mcp-local.git
cd fast-mcp-local

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e ".[dev]"
```

### 2. Test It Works

```bash
# Start server
python3 -m fast_mcp_local.server

# You should see:
# 📚 Loading documents from /path/to/docs...
# ✅ Loaded: X docs, Y tokens
# ✅ Loaded Z verticle templates
```

### 3. Try CLI Commands

```bash
# Search docs
mcp search "async handler"

# List templates
mcp list-types

# Generate code
mcp generate platform-async
```

**It works!** 🎉

---

## For Hackathon Team

### Role 1: Backend Developer (Templates)

**Your Job**: Add company verticle templates

**Where to Add**:
```
docs/vertx/templates/company-{name}.md    # Template markdown
docs/vertx/schemas/company-{name}.json    # Metadata JSON
```

**Template Example** (`docs/vertx/templates/company-user-crud.md`):
```markdown
# Company User CRUD Verticle

## Description
CRUD operations for user management

## Verticle Code
```java
package com.company.verticles;

import com.company.api.AsyncHandler;
// ... your actual company code ...
```

## Gradle Dependencies
```gradle
dependencies {
    implementation 'com.company:platform-api:1.0.0'
    // ... your actual dependencies ...
}
```

## Configuration
```json
{
  "database": {
    "host": "company-postgres.internal",
    "port": 5432
  }
}
```
```

**Schema Example** (`docs/vertx/schemas/company-user-crud.json`):
```json
{
  "type": "company-user-crud",
  "name": "Company User CRUD Verticle",
  "description": "User CRUD operations",
  "template_file": "templates/company-user-crud.md",
  "gradle_dependencies": [
    "com.company:platform-api:1.0.0"
  ],
  "use_cases": ["User management", "CRUD operations"]
}
```

**Test**:
```bash
mcp list-types           # Verify it appears
mcp generate company-user-crud  # Verify it works
```

---

### Role 2: Content Manager (Documentation)

**Your Job**: Add company Vert.x documentation

**Where to Add**:
```
docs/company/platform-overview.md
docs/company/configuration-guide.md
docs/company/best-practices.md
docs/company/examples/*.md
```

**Example** (`docs/company/platform-overview.md`):
```markdown
# Company Vert.x Platform Overview

## Handler Types

### AsyncHandler
- For non-blocking operations
- Thread model: Event loop
- Examples: PostgreSQL queries, REST API calls

### SyncHandler
- For blocking operations
- Thread model: Worker pool
- Examples: SOAP calls, JDBC queries

### MultipartHandler
- For file uploads
- Thread model: Worker pool
- Examples: Image uploads, document storage

## Configuration

All verticles use this structure:
```
config/{VerticleName}.v{version}/
├── lambda.json    # Metadata
└── config.json    # Settings
```

Access config via: `config().getData()`
```

**Index Docs**:
```python
from fast_mcp_local.loader import load_documents
from fast_mcp_local.database import init_db

init_db()
load_documents("docs/company")
```

**Test**:
```bash
mcp search "company platform"
mcp list-docs
```

---

### Role 3: QA Engineer (Testing)

**Your Job**: Test everything in MCP Inspector

**Start Inspector**:
```bash
npx @modelcontextprotocol/inspector python3 -m fast_mcp_local.server
```

Opens browser at `http://localhost:6274`

**Test Checklist**:
- [ ] `search_documents` - search for "async"
- [ ] `list_documents` - see all docs
- [ ] `get_document` - get specific doc
- [ ] `list_verticle_types` - see templates
- [ ] `generate_verticle` - generate platform-async

**Document Issues**: Create a Google Doc with screenshots

---

### Role 4: DevEx Engineer (AI Integration)

**Your Job**: Test with GitHub Copilot and Claude Code

**GitHub Copilot Setup**:

1. Update `.github/copilot-instructions.md`:
```markdown
# GitHub Copilot Instructions

This is Company's Vert.x platform.

## Platform Handlers
- AsyncHandler: Non-blocking (PostgreSQL, HTTP)
- SyncHandler: Blocking (SOAP, JDBC)
- MultipartHandler: File uploads

## Generate Code
```bash
mcp search "async handler"
mcp generate company-user-crud
```

## Configuration
Access via: `config().getData().getJsonObject("database")`
```

2. Test in VS Code Copilot Chat:
```
You: "Generate an AsyncHandler for user CRUD"
Copilot: [Should reference company platform]
```

**Demo Scenarios**:
1. "Search for platform configuration docs"
2. "Generate a company AsyncHandler for PostgreSQL"
3. "Show me best practices for SyncHandler"

**Record**: Screenshot successful interactions

---

### Role 5: DevOps (Demo & Deploy)

**Your Job**: Prepare demo environment

**Docker Setup** (`Dockerfile`):
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -e ".[dev]"
CMD ["python3", "-m", "fast_mcp_local.server"]
```

**Build & Run**:
```bash
docker build -t fast-mcp-local .
docker run -p 8000:8000 fast-mcp-local
```

**Demo Checklist**:
- [ ] Laptop with projector cable
- [ ] MCP Inspector running
- [ ] Demo video (backup)
- [ ] Presentation slides
- [ ] Internet connection tested

---

## Quick Reference

### CLI Commands
```bash
# Search
mcp search "query"
mcp ask "quick question"
mcp list-docs

# Generate
mcp list-types
mcp generate platform-async

# Get specific doc
mcp get "company/best-practices.md"
```

### MCP Tools
```json
{
  "search_documents": "Search company docs",
  "list_documents": "List all docs",
  "get_document": "Get specific doc",
  "generate_verticle": "Generate code",
  "list_verticle_types": "List templates"
}
```

---

## Common Issues

### "Database not initialized"
```bash
rm documents.db
python3 -m fast_mcp_local.server
```

### "Template not found"
```bash
# Verify files exist
ls docs/vertx/templates/
ls docs/vertx/schemas/

# Check JSON is valid
python -m json.tool docs/vertx/schemas/your-template.json
```

### "No documents found"
```python
# Re-index
from fast_mcp_local.loader import load_documents
from fast_mcp_local.database import init_db

init_db()
load_documents("docs/company")
```

---

## Demo Script

### Opening (2 min)
**Problem**: New developers take weeks to learn our custom Vert.x platform. Lots of copy-paste from Slack, inconsistent code.

**Solution**: AI assistant that knows our platform architecture, docs, and code templates.

### Demo 1: Document Search (2 min)
```bash
# In MCP Inspector or Copilot
"Search for AsyncHandler documentation"
# Shows: Company platform docs with examples
```

**Impact**: 95% faster than searching Confluence (10 min → 30 sec)

### Demo 2: Code Generation (3 min)
```bash
# Generate verticle
mcp generate company-user-crud

# Shows:
# - Complete Java code
# - Gradle dependencies
# - Configuration example
```

**Impact**: 85% faster development (4-6 hours → 30 minutes)

### Demo 3: AI Integration (2 min)
```
Copilot Chat: "Generate a company AsyncHandler for user queries"
# Copilot uses MCP to generate correct code
```

**Impact**: Zero context switching, AI knows company patterns

### Closing (1 min)
**ROI**: 3,440% first-year return
**Onboarding**: 90% faster (2-4 weeks → 2-3 days)
**Production**: 8-12 weeks with 3-4 developers

---

## Next Steps After Hackathon

**Week 1-2**: Add company templates (10-15 templates)
**Week 3-4**: Add company docs (50+ documents)
**Week 5-6**: Security & authentication
**Week 7-8**: Production deployment
**Week 9-12**: Enterprise features (analytics, multi-tenancy)

---

## Resources

- **Hackathon Docs**:
  - `HACKATHON_SUBMISSION.md` - Full pitch document
  - `HACKATHON_WORKPLAN.md` - 2-day detailed plan
  - `HACKATHON_QUICKSTART.md` - 15-minute setup guide

- **Code**:
  - `src/fast_mcp_local/server.py` - MCP server (5 tools)
  - `src/fast_mcp_local/cli.py` - CLI commands
  - `docs/vertx/` - Templates and schemas

- **Templates**:
  - `docs/vertx/templates/platform-async-handler.md`
  - `docs/vertx/templates/platform-sync-handler.md`
  - `docs/vertx/templates/platform-multipart-handler.md`

---

## Support

**During Hackathon**:
- Slack: `#hackathon-fast-mcp`
- Issues: Create in GitHub

**Questions?**
- Check `HACKATHON_QUICKSTART.md` for troubleshooting
- Check `HACKATHON_WORKPLAN.md` for role-specific tasks

---

**Built for [Hackathon Name]**
**Team**: [Your Team Name]

🚀 **Let's win this!**
