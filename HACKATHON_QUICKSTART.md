# Hackathon Quick Start Guide

**Goal**: Get your team productive in 15 minutes ⚡

---

## Pre-Hackathon Setup (Do This BEFORE Day 1)

### Everyone

1. **Clone Repository**
   ```bash
   git clone https://github.com/karthik78180/fast-mcp-local.git
   cd fast-mcp-local
   ```

2. **Set Up Python Environment**
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip3 install -e ".[dev]"
   ```

3. **Verify Installation**
   ```bash
   pytest  # Should see 120+ tests passing
   python3 -m fast_mcp_local.server --help
   ```

4. **Install Node.js Tools** (for MCP Inspector)
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

5. **Set Up IDE**
   - Install VS Code or IntelliJ IDEA
   - Install GitHub Copilot extension
   - Install Claude Code CLI (if using Claude)

---

## Role-Specific Setup

### Role 1: Backend Developer (Templates)

**Install Java Development Tools**:
```bash
# Verify Java installed
java -version  # Should be Java 11+

# Familiarize with Vert.x
# Review: docs/vertx/templates/platform-async-handler.md
```

**Test Template Generation**:
```bash
# Start server
python3 -m fast_mcp_local.server &

# Test generation via CLI
mcp generate platform-async
mcp list-verticles
```

**Your First Task**: Add a company-specific template
- Copy `docs/vertx/templates/platform-async-handler.md` to `docs/vertx/templates/company-user-crud.md`
- Replace with actual company verticle code
- Create schema: `docs/vertx/schemas/company-user-crud.json`

---

### Role 2: Content Manager (Documentation)

**Gather Company Docs**:
- [ ] Access company Confluence
- [ ] Access internal wikis
- [ ] Collect Slack conversations with code examples
- [ ] Get access to company GitHub repos

**Set Up Documentation Directory**:
```bash
mkdir -p docs/company
mkdir -p docs/company/examples
```

**Test Document Indexing**:
```bash
python3 -c "
from fast_mcp_local.loader import load_documents
from fast_mcp_local.database import init_db

init_db()
load_documents('docs/vertx')  # Test with existing docs
"
```

**Your First Task**: Add 5 company docs
- Create `docs/company/platform-overview.md`
- Create `docs/company/configuration-guide.md`
- Create `docs/company/best-practices.md`
- Create `docs/company/troubleshooting.md`
- Create `docs/company/faq.md`

---

### Role 3: QA Engineer (Testing)

**Start MCP Inspector**:
```bash
npx @modelcontextprotocol/inspector python3 -m fast_mcp_local.server
```

This will open a web UI at `http://localhost:6274` where you can:
- See all available MCP tools
- Test each tool interactively
- Inspect request/response JSON

**Test All Tools**:
- [ ] `search_documents` - search for "postgres"
- [ ] `get_all_documents` - list all docs
- [ ] `get_document` - get specific doc
- [ ] `generate_verticle` - generate "platform-async"
- [ ] `list_verticle_types` - list all types
- [ ] `score_codebase` - score a Java file
- [ ] `list_migrations` - list migrations
- [ ] `get_migration_guide` - get v1-to-v2 guide

**Your First Task**: Create test checklist
- Document expected behavior for each tool
- Test with valid and invalid inputs
- Log bugs in shared Google Doc

---

### Role 4: DevEx Engineer (AI Integration)

**Set Up GitHub Copilot**:
1. Open VS Code
2. Install GitHub Copilot extension
3. Sign in with GitHub account
4. Verify Copilot is active (should see icon in status bar)

**Test Copilot Chat**:
1. Open Copilot Chat (Ctrl+Shift+I or Cmd+Shift+I)
2. Ask: "How do I use this MCP server?"
3. Check if it references `.github/copilot-instructions.md`

**Set Up Claude Code** (Optional):
```bash
# Install Claude Code CLI
# Follow: https://docs.claude.com/en/docs/claude-code

# Test integration
claude code "Search for postgres verticle examples"
```

**Your First Task**: Create demo scenarios
- Write 5 prompts for Copilot to test
- Record screenshots of Copilot responses
- Document what works vs what doesn't

---

### Role 5: DevOps (Infrastructure)

**Create Docker Setup**:
```bash
# Create Dockerfile
cat > Dockerfile <<'EOF'
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -e ".[dev]"

CMD ["python3", "-m", "fast_mcp_local.server"]
EOF

# Build and test
docker build -t fast-mcp-local .
docker run -p 8000:8000 fast-mcp-local
```

**Set Up GitHub Actions** (if time permits):
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -e ".[dev]"
      - run: pytest
```

**Your First Task**: Create deployment plan
- Document infrastructure requirements
- Create docker-compose.yml
- Plan demo environment setup

---

## Day 1 Morning Checklist (First Hour)

**Everyone meets at**: [Time, Location]

### Team Lead
- [ ] Review roles and responsibilities
- [ ] Set up Slack channel: `#hackathon-fast-mcp`
- [ ] Create shared Google Doc for notes
- [ ] Assign specific templates/docs to each person

### All Team Members
- [ ] Verify environment setup working
- [ ] Run tests: `pytest`
- [ ] Start MCP server: `python3 -m fast_mcp_local.server`
- [ ] Test one CLI command
- [ ] Report any setup issues

---

## Company-Specific Customization Checklist

### 1. Add Company Templates (Role 1)

**Template Locations**:
- `docs/vertx/templates/company-{name}-verticle.md` - Template markdown
- `docs/vertx/schemas/company-{name}.json` - Metadata JSON

**Template Format**:
```markdown
# Company {Name} Verticle

## Description
[What this verticle does in company context]

## Verticle Code
```java
package com.company.verticles;

import com.company.api.AsyncHandler;  // Company-specific import
// ... actual company code ...
```

## Gradle Dependencies
```gradle
dependencies {
    implementation 'com.company:platform-api:1.0.0'
    // ... actual company dependencies ...
}
```

## Configuration
```json
{
  "database": {
    "host": "company-postgres.internal",
    // ... actual company config ...
  }
}
```
```

**Priority Templates to Add**:
1. Company user CRUD verticle (most common)
2. Company authentication verticle
3. Company payment processing verticle
4. Company notification verticle
5. Company file upload verticle

---

### 2. Add Company Documentation (Role 2)

**Priority Documents**:

**docs/company/platform-overview.md**:
```markdown
# Company Vert.x Platform Overview

## Architecture
[Company platform architecture]

## Handler Types
- AsyncHandler: [When to use]
- SyncHandler: [When to use]
- MultipartHandler: [When to use]

## Configuration Structure
[Explain lambda.json and config.json]
```

**docs/company/configuration-guide.md**:
```markdown
# Configuration Guide

## Environment Variables
- `DB_PASSWORD`: Database password
- `API_KEY`: External API key
[List all environment variables]

## Configuration Files
- `lambda.json`: [Metadata schema]
- `config.json`: [Endpoint configuration]
```

**docs/company/best-practices.md**:
```markdown
# Best Practices

## Resource Management
- Always close database connections in stop()
- Use try-finally for resource cleanup

## Configuration
- Use config().getData() to access configuration
- Never hardcode credentials

## Error Handling
- Return proper HTTP status codes
- Log errors with context
```

**docs/company/examples/** (add 5-10 real company verticles)

---

### 3. Add Company Scoring Rules (Role 1 + Role 3)

**File**: `docs/patterns/company-best-practices/scoring-rules.json`

```json
{
  "pattern_id": "company-best-practices",
  "name": "Company Vert.x Best Practices",
  "description": "Evaluate verticles against company standards",
  "passing_threshold": 70,
  "categories": {
    "configuration": {
      "weight": 20,
      "description": "Proper configuration access",
      "rules": [
        {
          "id": "config-access",
          "name": "Uses config().getData()",
          "pattern_type": "presence",
          "pattern": "config\\(\\)\\.getData\\(\\)",
          "score": 10,
          "severity": "high",
          "suggestion": "Use config().getData() for configuration access"
        }
      ]
    },
    "imports": {
      "weight": 15,
      "description": "Correct imports",
      "rules": [
        {
          "id": "company-imports",
          "name": "Uses company handler interfaces",
          "pattern_type": "presence",
          "pattern": "import com\\.company\\.api\\.(AsyncHandler|SyncHandler|MultipartHandler)",
          "score": 10,
          "severity": "high",
          "suggestion": "Import company handler interfaces"
        }
      ]
    }
  }
}
```

---

### 4. Update Copilot Instructions (Role 4)

**File**: `.github/copilot-instructions.md`

```markdown
# GitHub Copilot Instructions for Company Vert.x Platform

## Context
This repository uses Company's custom Vert.x platform.

## Platform Architecture
- **AsyncHandler**: Non-blocking operations (PostgreSQL, HTTP clients, Redis)
  - Thread model: Event loop (never block!)
  - Examples: Database queries, REST API calls
- **SyncHandler**: Blocking operations (SOAP, JDBC, file I/O)
  - Thread model: Worker pool (blocking is safe)
  - Examples: SOAP services, legacy databases
- **MultipartHandler**: File uploads
  - Thread model: Worker pool (file I/O is safe)
  - Examples: Image uploads, document storage

## Code Generation
To generate verticle code, use the MCP server:
```bash
mcp search "postgres async handler"
mcp generate company-user-crud
mcp score ./MyVerticle.java --pattern company-best-practices
```

## Configuration Pattern
All verticles use this configuration structure:
```
config/{VerticleName}.v{version}/
├── lambda.json    # Metadata (artifactId, endpoint, handlerType)
└── config.json    # Endpoint config (database, API settings)
```

Access config via: `config().getData().getJsonObject("database")`

## Best Practices
1. Use config().getData() for configuration
2. Initialize resources in start()
3. Clean up resources in stop()
4. Never block the event loop in AsyncHandler
5. Always close database connections
6. Return proper HTTP status codes

## Common Patterns
- PostgreSQL queries: Use AsyncHandler with PgPool
- SOAP calls: Use SyncHandler with SOAPConnection
- File uploads: Use MultipartHandler with FileUpload
```

---

## Testing Your Customizations

### Test Template Generation
```bash
# Generate company template
mcp generate company-user-crud

# Verify output includes:
# - Java code with company imports
# - Gradle dependencies with company artifacts
# - Configuration with company patterns
```

### Test Document Search
```bash
# Search for company docs
mcp search "company configuration"

# Verify results include company-specific docs
```

### Test Code Scoring
```bash
# Score a company verticle
mcp score ./src/main/java/com/company/verticles/UserVerticle.java \
  --pattern company-best-practices

# Verify company-specific rules are checked
```

---

## Common Issues & Solutions

### Issue: "No module named 'fast_mcp_local'"
**Solution**:
```bash
# Make sure you're in virtual environment
source .venv/bin/activate

# Reinstall package
pip install -e ".[dev]"
```

### Issue: MCP Inspector won't start
**Solution**:
```bash
# Check if port 6274 is already in use
lsof -i :6274

# Kill existing process
kill -9 [PID]

# Restart inspector
npx @modelcontextprotocol/inspector python3 -m fast_mcp_local.server
```

### Issue: Tests failing
**Solution**:
```bash
# Clean up database
rm documents.db

# Reinstall dependencies
pip install -e ".[dev]"

# Run tests
pytest -v
```

### Issue: Template not showing in list_verticle_types
**Solution**:
- Verify schema exists in `docs/vertx/schemas/`
- Verify template exists in `docs/vertx/templates/`
- Restart MCP server
- Check JSON schema is valid: `python -m json.tool docs/vertx/schemas/your-template.json`

### Issue: Documents not searchable
**Solution**:
```bash
# Re-index documents
python3 -c "
from fast_mcp_local.loader import load_documents
from fast_mcp_local.database import init_db

init_db()
load_documents('docs/company')
"

# Verify indexing
sqlite3 documents.db "SELECT filename FROM documents WHERE filename LIKE '%company%';"
```

---

## Quick Commands Reference

```bash
# Development
pytest                          # Run tests
pytest -v                       # Verbose tests
pytest --cov                    # With coverage

# MCP Server
python3 -m fast_mcp_local.server           # Start server
npx @modelcontextprotocol/inspector \
  python3 -m fast_mcp_local.server         # Start with inspector

# CLI
mcp search "query"                         # Search docs
mcp list-docs                              # List all docs
mcp generate template-name                 # Generate code
mcp list-verticles                         # List templates
mcp score ./File.java --pattern pattern-id # Score code
mcp list-patterns                          # List patterns

# Database
sqlite3 documents.db                       # Open database
sqlite3 documents.db "SELECT * FROM documents;"  # Query docs

# Git
git status                                 # Check status
git add .                                  # Stage changes
git commit -m "message"                    # Commit
git push                                   # Push to remote
```

---

## Success Metrics

**By end of hackathon, you should have**:

- [ ] **3-5 company templates** working and tested
- [ ] **20+ company docs** indexed and searchable
- [ ] **Company scoring rules** implemented and tested
- [ ] **GitHub Copilot integration** working
- [ ] **Working demo** (live + video backup)
- [ ] **Presentation ready** (15-20 slides)
- [ ] **All tests passing** (120+ tests)
- [ ] **Team confident** in presenting

---

## Emergency Contacts

**During Hackathon**:
- Team Slack: `#hackathon-fast-mcp`
- Team Lead: [Name, Phone]
- Technical Questions: [Name, Phone]

**Technical Support**:
- Python Issues: [Resource/Person]
- Vert.x Questions: [Resource/Person]
- Infrastructure: [Resource/Person]

---

## Motivational Reminder

**Remember**:
- ✅ **Done is better than perfect** - Ship working software
- ✅ **Focus on demo** - What looks good in 5 minutes?
- ✅ **Test early, test often** - Don't wait until last minute
- ✅ **Help each other** - We win as a team
- ✅ **Have fun!** - This is a hackathon, enjoy it!

---

**You've got this! 🚀**

**Start hacking in**: [Hackathon Start Time]
**Present in**: [Presentation Time]

---

**Questions?** Check the full docs:
- `HACKATHON_SUBMISSION.md` - Full project overview
- `HACKATHON_WORKPLAN.md` - Detailed 2-day plan
- `README.md` - Technical documentation
- `design/` - Architecture documentation
