# Company Documentation

**This directory is for your company-specific Vert.x documentation.**

## What to Add Here

### 1. Platform Overview
Create `platform-overview.md` explaining your custom Vert.x platform:
- Handler types (AsyncHandler, SyncHandler, MultipartHandler)
- Configuration structure
- Deployment process
- Platform-specific conventions

### 2. Configuration Guide
Create `configuration-guide.md` with:
- Config file structure (lambda.json, config.json)
- Environment variables
- Common configuration patterns
- Examples for different handler types

### 3. Best Practices
Create `best-practices.md` with:
- When to use each handler type
- Resource management patterns
- Error handling conventions
- Testing guidelines
- Code review checklist

### 4. Examples Directory
Add real company verticle examples to `examples/`:
```
examples/
├── user-crud-example.md       # AsyncHandler example
├── payment-soap-example.md    # SyncHandler example
├── file-upload-example.md     # MultipartHandler example
└── ...
```

### 5. FAQ & Troubleshooting
Create `faq.md` and `troubleshooting.md` with common questions and issues.

## Quick Start

### Add Your First Doc

1. Create a markdown file in this directory:
```bash
vi docs/company/platform-overview.md
```

2. Write your documentation using markdown

3. Index the documents:
```python
from fast_mcp_local.loader import load_documents
from fast_mcp_local.database import init_db

init_db()
load_documents("docs/company")
```

4. Test it works:
```bash
mcp search "platform overview"
mcp list-docs
```

## Tips

- **Use descriptive titles**: First line should be `# Your Title`
- **Add code examples**: Use \`\`\`java code blocks
- **Keep it simple**: Focus on what developers actually need
- **Real examples**: Copy-paste actual company code (sanitized)
- **Update regularly**: Keep docs in sync with platform changes

## Examples from Platform Docs

Check `docs/vertx/templates/` to see how platform handler docs are structured. Use similar patterns for company docs.
