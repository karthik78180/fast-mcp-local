# File Dependencies for PRB SRE Assistant

**Understanding what files each feature relies on**

---

## Current Features (PRB Branch)

### ✅ Feature 1: PRB Search & Discovery

**What it does**: Full-text search across all PRB documentation

**Files it relies on**:

```
docs/prbs/                          # Searches EVERYTHING in docs/prbs/ recursively
├── examples/                       # Example PRBs
│   ├── prb-2024-001-database-connection-pool-exhaustion.md
│   └── prb-2024-002-memory-leak-kubernetes-pod.md
├── company/                        # YOUR COMPANY PRBs (add here!)
│   ├── prb-*.md                   # Past incident PRBs
│   └── ...                        # More PRBs
├── prb-best-practices.md          # PRB writing guide
└── *.md                           # Any markdown files
```

**How it works**:
1. On startup, scans all `.md` files in `docs/prbs/` recursively
2. Indexes content in SQLite database (`documents.db`)
3. Full-text search using SQLite FTS5 with token counting

**MCP Tools**:
- `search_prbs(query, limit)` - Full-text search with contextual snippets
- `get_prb(filename)` - Get specific PRB by relative path
- `list_prbs()` - List all indexed PRBs with metadata

**CLI Commands**:
```bash
prb search "database timeout"
prb get "prb-2024-001-database-connection-pool-exhaustion.md"
prb list
```

**Performance**: < 50ms search with SQLite FTS5

**Example**:
```bash
prb search "database connection pool"
# Searches all markdown files in docs/prbs/
# Returns matching PRBs with contextual snippets
```

---

### ✅ Feature 2: PRB Drafting & Templates

**What it does**: Generates PRB drafts from incident descriptions

**Files it relies on**:
```
src/fast_mcp_local/prb_drafter.py   # Template definitions (hardcoded)
```

**Templates Built-In** (no external files needed):
1. **Standard Template** - Most incidents (High/Medium severity)
   - Basic structure with all required sections
   - Suitable for database issues, performance problems, service degradations

2. **Critical Template** - Complete outages
   - Executive summary for leadership
   - Detailed impact analysis (customer, business, revenue)
   - Communication log for stakeholders

3. **Postmortem Template** - Detailed retrospective
   - Timeline in table format
   - "What went well" / "What went wrong" / "Where we got lucky"
   - Action items with priority levels (P0/P1/P2)

**How it works**:
1. Parse incident description to extract key information (systems, causes, actions)
2. Select appropriate template based on severity
3. Auto-populate fields (PRB ID, date, severity, systems, timeline)
4. Return formatted markdown PRB draft

**MCP Tools**:
- `draft_prb(description, severity, systems)` - Generate complete PRB draft
- `create_prb_template(type)` - Get blank template (standard/critical/postmortem)
- `suggest_prb_sections(partial_prb)` - Suggest missing sections for incomplete PRBs

**CLI Commands**:
```bash
prb draft "API gateway returned 503 errors" --severity Critical --systems "api,db"
prb template --type critical
prb suggest my-draft.md
```

**Performance**: < 100ms draft generation

**Example**:
```bash
prb draft "Database connection pool exhausted at 14:30, causing API 503 errors" \
  --severity Critical \
  --systems "database,api-gateway"
# Returns: Complete PRB draft with auto-populated fields
```

---

### ✅ Feature 3: PRB Analysis & Quality Scoring

**What it does**: Analyzes PRB completeness and quality with scoring

**Files it relies on**:
```
src/fast_mcp_local/prb_analyzer.py  # Scoring algorithm (hardcoded)
```

**Scoring Rules** (built-in, no external files):

**Required Sections (70% weight)**:
1. Incident Summary - PRB ID, date, severity, status, impact, duration
2. Timeline - Minimum 3 events with timestamps
3. Root Cause Analysis - Technical explanation
4. Resolution - Immediate actions + permanent fix
5. Action Items - With owners (@username) and due dates (YYYY-MM-DD)
6. Prevention - Short-term + long-term measures

**Section Completeness (30% weight)**:
- Word count thresholds per section
- Metadata completeness (PRB ID, severity, date)
- Action item quality (owner and due date specified)

**Grading Scale**:
- A (90-100%): Excellent, ready for review
- B (80-89%): Good, minor improvements needed
- C (70-79%): Fair, some sections need expansion
- D (60-69%): Poor, significant work required
- F (< 60%): Incomplete, major rework needed

**How it works**:
1. Parse PRB markdown structure to extract sections, metadata, timeline, action items
2. Validate presence of required sections
3. Calculate section completeness based on word counts and metadata
4. Generate improvement suggestions and estimate time to complete
5. Return comprehensive analysis with score, grade, strengths, weaknesses

**MCP Tools**:
- `analyze_prb(content)` - Comprehensive analysis with score, grade, recommendations
- `validate_prb(content)` - Validate structure and required sections
- `parse_prb(content)` - Parse and extract structured data

**CLI Commands**:
```bash
prb analyze my-prb.md
prb validate my-prb.md
prb parse my-prb.md
```

**Performance**: < 200ms analysis

**Example**:
```bash
prb analyze docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
# Returns: Completeness score (85.5%), grade (B), strengths, weaknesses, suggestions
```

---

### ✅ Feature 4: Action Item Management

**What it does**: Extracts and tracks action items from PRBs

**Files it relies on**:
```
src/fast_mcp_local/prb_analyzer.py  # Action item extraction (hardcoded)
```

**Action Item Parsing** (built-in, no external files):

**Extraction Rules**:
- Markdown checkboxes: `- [ ]` (pending) or `- [x]` (completed)
- Owner pattern: `@username` or `Owner: @username`
- Due date pattern: `YYYY-MM-DD` or `Due: YYYY-MM-DD`
- Line number tracking for reference

**How it works**:
1. Scan PRB content for markdown checkboxes in Action Items section
2. Extract description, owner, due date using regex patterns
3. Determine status (pending vs completed) based on checkbox state
4. Generate summary statistics (total, pending, completed, with owner, with due date)
5. Return structured JSON with all action items

**MCP Tools**:
- `extract_action_items(content)` - Extract all action items with metadata

**CLI Commands**:
```bash
prb actions my-prb.md
```

**Performance**: < 50ms extraction

**Example**:
```bash
prb actions docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
# Returns: 7 action items with owners, due dates, status, and summary stats
```

---

## File Structure Summary

### PRB Branch:

```
fast-mcp-local/
├── src/fast_mcp_local/
│   ├── server.py              # MCP server (10 PRB tools)
│   ├── cli.py                 # CLI wrapper (10 commands)
│   ├── database.py            # SQLite document storage (FTS5)
│   ├── loader.py              # Document indexing with token counting
│   ├── prb_analyzer.py        # PRB parsing, validation, scoring (580 lines)
│   └── prb_drafter.py         # PRB template generation and drafting (480 lines)
│
├── docs/prbs/
│   ├── examples/              # Example PRBs (2 complete examples)
│   │   ├── prb-2024-001-database-connection-pool-exhaustion.md
│   │   └── prb-2024-002-memory-leak-kubernetes-pod.md
│   ├── company/               # YOUR COMPANY PRBs GO HERE
│   │   └── (add your past PRBs here)
│   └── prb-best-practices.md  # PRB writing guide (490 lines)
│
├── tests/
│   ├── test_database.py       # Database tests (13 tests)
│   └── test_loader.py         # Loader tests (12 tests)
│
├── documents.db               # SQLite database (auto-generated)
├── README.md                  # Main project documentation
├── HACKATHON_SUBMISSION.md    # Full hackathon pitch
└── DEPENDENCIES.md            # This file
```

---

## For Your SRE Team

### To Add Company PRBs:

**Step 1**: Copy past PRBs to docs/prbs/company/
```bash
mkdir -p docs/prbs/company
cp ~/incidents/*.md docs/prbs/company/
```

**Step 2**: Restart MCP server to re-index
```bash
python3 -m fast_mcp_local.server
# Automatically indexes all .md files in docs/prbs/
```

**Step 3**: Test it works
```bash
prb search "your incident keywords"
prb list
```

### To Customize PRB Templates:

PRB templates are currently **hardcoded** in `src/fast_mcp_local/prb_drafter.py:72-381`.

**Option 1**: Edit existing templates in code
```python
# Edit src/fast_mcp_local/prb_drafter.py
# Modify TEMPLATES dictionary (line 72-381)
```

**Option 2**: Use blank template as starting point
```bash
prb template --type standard > my-template.md
# Edit my-template.md to match your company format
```

### To Customize Scoring Rules:

PRB scoring rules are currently **hardcoded** in `src/fast_mcp_local/prb_analyzer.py:34-51`.

**To customize**:
```python
# Edit src/fast_mcp_local/prb_analyzer.py
# Modify REQUIRED_SECTIONS list (line 34-41)
# Modify OPTIONAL_SECTIONS list (line 43-48)
# Adjust scoring weights (line 192-203)
```

---

## Quick Reference

| Feature | Depends On | What to Add |
|---------|------------|-------------|
| PRB Search | All `.md` files in `docs/prbs/` | Add past PRBs to `docs/prbs/company/` |
| PRB Drafting | `prb_drafter.py` (hardcoded) | Edit templates in code or use blank template |
| PRB Analysis | `prb_analyzer.py` (hardcoded) | Edit scoring rules in code |
| Action Item Extraction | `prb_analyzer.py` (hardcoded) | No external files needed |
| Database Indexing | `docs/prbs/` folder | Auto-scans on startup |

---

## Key Differences from Vert.x Branch

**Vert.x Branch** (feature/minimal-hackathon-demo):
- Relies on external files: `docs/vertx/schemas/*.json`, `docs/vertx/templates/*.md`
- Requires company to create template files and schemas
- Migration and scoring patterns in `docs/migrations/`, `docs/patterns/`

**PRB Branch** (feature/prb-sre-assistant):
- Templates **hardcoded** in `prb_drafter.py` - No external files needed
- Scoring rules **hardcoded** in `prb_analyzer.py` - No external files needed
- Only requires: **PRB markdown files** in `docs/prbs/`

**Advantage**: Simpler deployment, no configuration needed - just add PRB files and go!

---

## Performance Characteristics

| Operation | Latency | Bottleneck |
|-----------|---------|------------|
| Search PRBs | < 50ms | SQLite FTS5 query |
| Draft PRB | < 100ms | Template string substitution |
| Analyze PRB | < 200ms | Regex parsing of markdown |
| Extract action items | < 50ms | Regex pattern matching |
| Load all PRBs | < 1s | Initial indexing (1000 PRBs) |

**Scalability**:
- Handles 1000+ PRB documents efficiently
- Sub-second search across all PRBs
- No external API dependencies
- Runs entirely on local SQLite database

---

## Production Deployment

### What Files You Need:

**Minimum**:
- `src/fast_mcp_local/` (Python source code)
- `docs/prbs/` (your company PRBs)
- `pyproject.toml` (dependencies)

**Auto-Generated**:
- `documents.db` (created on first run)

**Optional**:
- `docs/prbs/prb-best-practices.md` (PRB writing guide)
- `tests/` (unit tests)

### Database Management:

**First Run**:
```bash
python3 -m fast_mcp_local.server
# Creates documents.db and indexes all PRBs
```

**Adding New PRBs**:
```bash
# Add PRB files to docs/prbs/company/
# Restart server to re-index
python3 -m fast_mcp_local.server
```

**Database Reset** (if needed):
```bash
rm documents.db
python3 -m fast_mcp_local.server
# Rebuilds from scratch
```

---

## Testing

### Run Tests:
```bash
pytest                    # All tests
pytest tests/test_database.py  # Database tests only
pytest tests/test_loader.py    # Loader tests only
pytest -v                 # Verbose output
```

### Test Coverage:
- **database.py**: 13 tests (CRUD operations, search, FTS5)
- **loader.py**: 12 tests (document loading, token counting)
- **Total**: 25 tests, all passing

**Note**: No tests for `prb_analyzer.py` or `prb_drafter.py` yet - opportunity for improvement!

---

**Last Updated**: For PRB SRE Assistant branch
**Branch**: `feature/prb-sre-assistant`
**Status**: PRB-focused with hardcoded templates and scoring
