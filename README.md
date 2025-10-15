# PRB SRE Assistant

**AI-powered Problem Record (PRB) management for SRE teams**

Quickly draft, analyze, and manage incident PRBs using MCP (Model Context Protocol) tools integrated with your IDE and AI assistants.

---

## 🎯 What is This?

PRB SRE Assistant helps SRE teams handle incident response and postmortems by:

1. **Drafting PRBs** from incident descriptions automatically
2. **Analyzing PRB quality** and completeness with scoring
3. **Searching past PRBs** to learn from similar incidents
4. **Validating PRB structure** to ensure all sections are present
5. **Extracting action items** with owners and due dates
6. **Suggesting improvements** based on best practices

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install

```bash
# Clone and install
git clone https://github.com/karthik78180/fast-mcp-local.git
cd fast-mcp-local
git checkout feature/prb-sre-assistant

# Create virtual environment and install
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Step 2: Test the CLI

```bash
# Search past PRBs
prb search "database timeout"

# List all PRBs
prb list

# Draft a new PRB
prb draft "API gateway returned 503 errors" --severity Critical

# Get a template
prb template --type critical
```

### Step 3: Test the MCP Server

```bash
# Start the server
python3 -m fast_mcp_local.server

# In another terminal, test tools
# (or use with Claude Code, GitHub Copilot, etc.)
```

---

## 📦 What's Included

### 10 MCP Tools

**Search & Discovery:**
1. `search_prbs(query, limit)` - Search past PRB documentation
2. `get_prb(filename)` - Get specific PRB content
3. `list_prbs()` - List all available PRBs

**PRB Drafting:**
4. `draft_prb(description, severity, systems)` - Generate PRB from incident
5. `create_prb_template(type)` - Get blank template (standard/critical/postmortem)
6. `suggest_prb_sections(partial_prb)` - Suggest missing sections

**PRB Analysis:**
7. `analyze_prb(content)` - Analyze completeness and quality
8. `validate_prb(content)` - Validate structure
9. `extract_action_items(content)` - Extract all action items
10. `parse_prb(content)` - Parse and extract structured data

### 10 CLI Commands

```bash
prb search <query>              # Search past PRBs
prb list                        # List all PRBs
prb get <filename>              # Get specific PRB

prb draft <description>         # Generate PRB draft
prb template [--type TYPE]      # Get blank template
prb suggest <prb-file>          # Suggest missing sections

prb analyze <prb-file>          # Analyze quality
prb validate <prb-file>         # Validate structure
prb actions <prb-file>          # Extract action items
prb parse <prb-file>            # Parse structured data
```

### Documentation

- **PRB Best Practices** (`docs/prbs/prb-best-practices.md`) - Complete guide
- **Example PRBs** (`docs/prbs/examples/`) - Real-world examples
  - Database connection pool exhaustion
  - Memory leak in Kubernetes pod

---

## 💡 Use Cases

### Use Case 1: On-Call SRE During Incident

**Scenario**: You're on-call and just got paged for a production incident.

```bash
# 1. Draft a PRB immediately
prb draft "API gateway returning 503 errors, database timeouts observed" \
  --severity Critical \
  --systems "api-gateway,database"

# Output: PRB draft with timestamp, structure, suggested actions

# 2. Copy the draft, start filling in timeline as incident progresses
# 3. Search for similar past incidents
prb search "database timeout"

# 4. Learn from past resolutions
prb get "prb-2024-001-database-connection-pool-exhaustion.md"
```

**Result**: PRB started in < 2 minutes, similar incidents found to guide response.

### Use Case 2: Post-Incident PRB Review

**Scenario**: Incident resolved, need to finalize PRB before post-incident meeting.

```bash
# 1. Analyze your draft PRB
prb analyze incident-draft.md

# Output:
# {
#   "completeness_score": 75.5,
#   "grade": "C",
#   "strengths": ["All required sections present", "Detailed timeline"],
#   "weaknesses": ["Timeline needs more detail", "No action items defined"],
#   "improvement_suggestions": [
#     "Add action items with owners and due dates",
#     "Expand Root Cause Analysis section"
#   ]
# }

# 2. Validate structure
prb validate incident-draft.md

# 3. Extract action items to track
prb actions incident-draft.md

# 4. Improve based on feedback, re-analyze until A/B grade
```

**Result**: High-quality PRB ready for review, nothing missed.

### Use Case 3: PRB Template for Team

**Scenario**: Establish PRB standards for your SRE team.

```bash
# 1. Get a template
prb template --type standard > team-prb-template.md

# 2. For critical incidents
prb template --type critical > critical-incident-template.md

# 3. For detailed retrospectives
prb template --type postmortem > postmortem-template.md

# 4. Share templates with team via wiki/git
```

**Result**: Consistent PRB format across all team incidents.

### Use Case 4: IDE Integration (Copilot Chat / Claude Code)

**Scenario**: Use PRB tools directly in your IDE while writing PRB.

In VS Code with Copilot Chat or Claude Code:

```
@prb-sre-assistant draft_prb(
  incident_description="Database connection pool exhausted at 14:30...",
  severity="Critical",
  affected_systems="api,database"
)

# Get instant PRB draft in chat
# Copy to file, continue editing with AI assistance
```

In Chat:
```
"Analyze this PRB for completeness"
# AI uses analyze_prb() tool automatically
# Gets structured feedback
```

**Result**: PRB drafting and analysis without leaving your editor.

---

## 🛠️ Architecture

```
PRB SRE Assistant
├── MCP Server (server.py)
│   ├── 10 MCP tools for PRB management
│   └── Document search via SQLite FTS5
│
├── PRB Analyzer (prb_analyzer.py)
│   ├── Parse PRB markdown structure
│   ├── Validate completeness (scoring algorithm)
│   ├── Extract action items, timeline, metadata
│   └── Generate improvement recommendations
│
├── PRB Drafter (prb_drafter.py)
│   ├── Generate PRB from incident description
│   ├── 3 templates (standard, critical, postmortem)
│   ├── Suggest missing sections
│   └── Extract incident metadata from text
│
└── CLI (cli.py)
    └── 10 commands wrapping MCP tools
```

---

## 📚 PRB Structure

A complete PRB contains:

```markdown
# PRB-YYYY-NNN: [Title]

## Incident Summary
- PRB ID, Date, Severity, Status
- Affected Systems, Impact, Duration

## Timeline
- HH:MM - Event/action
- HH:MM - Event/action

## Root Cause Analysis
[Detailed technical explanation]

## Resolution
[How it was fixed]

## Action Items
- [ ] Action (Owner: @user, Due: YYYY-MM-DD)

## Prevention
[How to prevent recurrence]

## Lessons Learned
[Key insights]
```

See `docs/prbs/prb-best-practices.md` for complete guide.

---

## 🎓 PRB Scoring Algorithm

PRBs are scored 0-100% based on:

**Required Sections (70% weight)**:
- Incident Summary
- Timeline (minimum 3 events)
- Root Cause Analysis
- Resolution
- Action Items (with owners and due dates)
- Prevention

**Section Completeness (30% weight)**:
- Word count thresholds per section
- Metadata completeness
- Action item details (owner, due date)

**Grading**:
- A: 90-100% - Excellent, ready for review
- B: 80-89% - Good, minor improvements needed
- C: 70-79% - Fair, some sections need expansion
- D: 60-69% - Poor, significant work required
- F: < 60% - Incomplete, major rework needed

---

## 🔌 IDE Integration

### VS Code (Copilot Chat or Claude Code)

In your project, create `.vscode/settings.json`:

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "servers": {
        "prb-sre-assistant": {
          "command": "python3",
          "args": ["-m", "fast_mcp_local.server"],
          "cwd": "/path/to/fast-mcp-local",
          "env": {
            "PYTHONPATH": "/path/to/fast-mcp-local/src"
          }
        }
      }
    }
  },
  "github.copilot.chat.mcp.enabled": true
}
```

Then in Copilot Chat:
```
@prb-sre-assistant search_prbs("database timeout")
@prb-sre-assistant draft_prb("API errors observed...")
```

### IntelliJ IDEA (Copilot Plugin)

`Settings` > `Tools` > `GitHub Copilot` > `MCP Servers` > Add:
- Name: `prb-sre-assistant`
- Command: `python3`
- Args: `-m fast_mcp_local.server`
- Working Directory: `/path/to/fast-mcp-local`

---

## 📁 Add Your Own PRBs

```bash
# Add your company's PRBs to docs/prbs/
mkdir -p docs/prbs/company
cp ~/incidents/*.md docs/prbs/company/

# Restart MCP server to re-index
python3 -m fast_mcp_local.server

# Now searchable!
prb search "your incident keywords"
```

PRBs are automatically indexed from:
- `docs/prbs/examples/` - Example PRBs
- `docs/prbs/company/` - Your company PRBs (add yours here)
- `docs/prbs/` - Any markdown files

---

## 🧪 Examples

### Example 1: Draft PRB from Incident

```bash
$ prb draft "API gateway started returning 503 errors at 14:30. Investigation showed database connection pool was exhausted. All 100 connections were being held by slow queries." --severity Critical --systems "api-gateway,database"

{
  "prb_draft": "# PRB-2025-1015: API gateway started returning 503 errors at 14:30...\n\n## Incident Summary\n- **PRB ID**: PRB-2025-1015\n- **Date**: 2025-10-15\n- **Severity**: Critical\n...",
  "instructions": "Copy this draft and fill in placeholders as incident progresses"
}
```

### Example 2: Analyze PRB Quality

```bash
$ prb analyze my-incident.md

{
  "completeness_score": 85.5,
  "grade": "B",
  "summary": "PRB-2025-1015: Database Connection Pool Exhaustion\nOverall Quality: 85.5% (Grade: B)\nRequired Sections: 6/6\nAction Items: 7\nTimeline Events: 8",
  "strengths": [
    "All required sections present",
    "7 sections with good/excellent quality",
    "All action items have owners and due dates",
    "Detailed timeline with 8 events"
  ],
  "weaknesses": [
    "1 sections need more detail"
  ],
  "improvement_suggestions": [
    "Expand Prevention section (currently 65% complete)"
  ],
  "estimated_completion_time": "15-30 minutes (add missing details)"
}
```

### Example 3: Extract Action Items

```bash
$ prb actions my-incident.md

{
  "total_action_items": 7,
  "action_items": [
    {
      "description": "Add missing database index (Owner: @db-team, Due: 2024-01-15)",
      "owner": "db-team",
      "due_date": "2024-01-15",
      "status": "completed",
      "line_number": 67
    },
    ...
  ],
  "summary": {
    "pending": 4,
    "completed": 3,
    "with_owner": 7,
    "with_due_date": 7
  }
}
```

---

## 🤝 Contributing

This is an internal tool for SRE teams. To customize:

1. **Add your PRB templates** in `prb_drafter.py`
2. **Customize scoring rules** in `prb_analyzer.py`
3. **Add company-specific sections** to validation
4. **Extend CLI** with team-specific commands

---

## 📖 Documentation

- **Best Practices**: `docs/prbs/prb-best-practices.md`
- **Example PRBs**: `docs/prbs/examples/`
- **Architecture**: This README

---

## 🎯 Roadmap

Future enhancements:
- [ ] AI-powered root cause suggestions from past PRBs
- [ ] Automatic severity classification
- [ ] Integration with PagerDuty/ServiceNow
- [ ] PRB similarity scoring (find duplicates)
- [ ] Action item tracking dashboard
- [ ] Slack bot integration for PRB updates

---

## 📝 License

MIT License

---

## 🆘 Support

For issues or questions:
- Check `docs/prbs/prb-best-practices.md`
- Review example PRBs in `docs/prbs/examples/`
- Open an issue on GitHub

---

**Built for SRE teams who want to learn from every incident** 🚀

*"The goal of a PRB is not to assign blame, but to learn and improve."*
