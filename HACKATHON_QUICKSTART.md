# 2-Day Hackathon Quick Start Guide - PRB SRE Assistant

**Goal**: Get your team productive in 15 minutes and ready to demo PRB SRE Assistant

---

## Pre-Hackathon Setup (Do This BEFORE Day 1)

### Everyone

**1. Clone Repository**
```bash
git clone https://github.com/karthik78180/fast-mcp-local.git
cd fast-mcp-local
git checkout feature/prb-sre-assistant
```

**2. Set Up Python Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

**3. Verify Installation**
```bash
# Run tests (should see 25 tests passing)
pytest

# Test MCP server
python3 -m fast_mcp-local.server --help

# Test CLI
prb search "database"
prb list
```

**4. Test PRB Tools**
```bash
# Search example PRBs
prb search "database timeout"

# Draft a PRB
prb draft "Test incident" --severity High

# Analyze example PRB
prb analyze docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
```

**5. Familiarize with Codebase**
```bash
# Review main modules
cat src/fast_mcp_local/server.py          # 10 MCP tools
cat src/fast_mcp_local/prb_analyzer.py    # PRB analysis and scoring
cat src/fast_mcp_local/prb_drafter.py     # PRB drafting and templates
```

---

## Role-Specific Setup

### Role 1: SRE/Content Manager (PRB Data Collection)

**Your Job**: Collect and prepare company PRB data for indexing

**Pre-Hackathon Tasks**:
1. [ ] Access company incident management system (Jira, ServiceNow, Confluence)
2. [ ] Export past PRBs (last 6-12 months)
3. [ ] Convert to markdown format if needed
4. [ ] Organize by date or category

**Setup**:
```bash
# Create company PRB directory
mkdir -p docs/prbs/company

# Copy your company PRBs
cp ~/exports/incidents/*.md docs/prbs/company/

# Verify files
ls -l docs/prbs/company/
```

**Test Indexing**:
```bash
# Start server to index PRBs
python3 -m fast_mcp_local.server

# You should see:
# 📚 Loading documents from docs/prbs...
# ✅ Loaded: X docs, Y tokens

# Test search
prb search "your incident keyword"
prb list
```

**Day 1 Focus**:
- Add 20+ company PRBs
- Test search functionality
- Identify PRB formatting issues
- Document any data quality problems

---

### Role 2: Backend Developer (Template Customization)

**Your Job**: Customize PRB templates for company format

**Pre-Hackathon Tasks**:
1. [ ] Review company PRB format/template
2. [ ] Identify required vs optional sections
3. [ ] Note any company-specific fields
4. [ ] Review example PRBs

**Setup**:
```bash
# Review existing templates
prb template --type standard > standard-template.md
prb template --type critical > critical-template.md
prb template --type postmortem > postmortem-template.md

# Review template source code
cat src/fast_mcp_local/prb_drafter.py  # Lines 72-381
```

**Test Template Generation**:
```bash
# Draft PRB with different templates
prb draft "Test incident" --severity High
prb draft "Critical outage" --severity Critical
```

**Day 1 Focus**:
- Modify templates in `prb_drafter.py` to match company format
- Add company-specific sections
- Test draft generation with real incident descriptions
- Verify metadata extraction works

---

### Role 3: QA Engineer (Testing & Validation)

**Your Job**: Test all PRB features and ensure quality

**Pre-Hackathon Tasks**:
1. [ ] Set up Python environment
2. [ ] Run all tests successfully
3. [ ] Test all 10 CLI commands
4. [ ] Test MCP server

**Setup**:
```bash
# Run test suite
pytest -v

# Test each CLI command
prb search "database"
prb list
prb get "prb-2024-001-database-connection-pool-exhaustion.md"
prb draft "Test" --severity High
prb template --type standard
prb suggest docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
prb analyze docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
prb validate docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
prb actions docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
prb parse docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md
```

**Create Test Checklist**:
```markdown
# PRB Assistant Test Checklist

## Search & Discovery
- [ ] Search returns relevant PRBs
- [ ] List shows all indexed PRBs
- [ ] Get retrieves correct PRB content

## Drafting & Templates
- [ ] Draft generates valid PRB structure
- [ ] Templates include all required sections
- [ ] Suggest identifies missing sections

## Analysis & Quality
- [ ] Analyze scores PRBs correctly
- [ ] Validate checks required sections
- [ ] Parse extracts structured data

## Action Items
- [ ] Extract finds all action items
- [ ] Owner detection works (@username)
- [ ] Due date extraction works (YYYY-MM-DD)
```

**Day 1 Focus**:
- Test with company PRB data
- Document any bugs or issues
- Create comprehensive test report
- Validate all features work with real data

---

### Role 4: DevEx Engineer (AI Integration & Demo)

**Your Job**: Test AI integration (Claude Code, GitHub Copilot) and prepare demo

**Pre-Hackathon Tasks**:
1. [ ] Install Claude Code CLI (if using Claude)
2. [ ] Install GitHub Copilot in VS Code (if using Copilot)
3. [ ] Test MCP server integration
4. [ ] Prepare demo scenarios

**Setup - Claude Code**:
```bash
# Install Claude Code CLI
# Follow: https://docs.claude.com/en/docs/claude-code

# Test integration
claude code "Search for database incidents in PRBs"
claude code "Draft a PRB for API outage"
```

**Setup - GitHub Copilot**:
1. Open VS Code
2. Install GitHub Copilot extension
3. Configure MCP server (see README.md for config)
4. Test in Copilot Chat

**Demo Scenarios to Prepare**:

**Scenario 1: Search Past PRBs**
```
Prompt: "Search for past database timeout incidents"
Expected: Shows relevant PRBs with snippets
```

**Scenario 2: Draft PRB**
```
Prompt: "Draft a PRB for: API gateway returned 503 errors at 14:30, database connection pool exhausted"
Expected: Returns complete PRB draft
```

**Scenario 3: Analyze PRB**
```
Prompt: "Analyze this PRB for completeness: [paste PRB content]"
Expected: Returns score, grade, strengths, weaknesses
```

**Day 1 Focus**:
- Test AI integration with company data
- Create 5-7 demo scenarios
- Record demo video (backup plan)
- Take screenshots of successful interactions

---

### Role 5: DevOps (Infrastructure & Presentation)

**Your Job**: Prepare demo environment and presentation materials

**Pre-Hackathon Tasks**:
1. [ ] Set up demo laptop
2. [ ] Test projector connection
3. [ ] Create presentation outline
4. [ ] Plan deployment approach

**Setup - Demo Environment**:
```bash
# Test on presentation laptop
python3 -m fast_mcp_local.server

# Test CLI works
prb search "database"

# Prepare backup demo (video)
# Record screen showing all features
```

**Presentation Outline**:
```
1. Problem Statement (2 min)
   - SRE pain points
   - Time wasted on PRB creation

2. Our Solution (2 min)
   - PRB SRE Assistant overview
   - 4 core capabilities

3. Live Demo (5-7 min)
   - Search past PRBs
   - Draft new PRB
   - Analyze PRB quality
   - Extract action items

4. Business Value (2 min)
   - Productivity gains (87% faster PRB creation)
   - ROI analysis (1,300% first year)

5. Production Roadmap (1 min)
   - 8-week implementation plan
   - Next steps

6. Q&A (3-5 min)
```

**Day 1 Focus**:
- Create presentation slides (15-20 slides)
- Test A/V equipment
- Record backup demo video
- Prepare for common questions

---

## Day 1 Morning Checklist (First Hour)

**Team Meeting**: [Time, Location]

### Team Lead
- [ ] Review roles and responsibilities
- [ ] Set up team Slack channel: `#hackathon-prb-assistant`
- [ ] Create shared Google Doc for notes/issues
- [ ] Assign specific tasks to each person
- [ ] Set deadlines for Day 1

### All Team Members
- [ ] Verify environment setup working
- [ ] Run tests: `pytest` (should see 25 tests passing)
- [ ] Start MCP server: `python3 -m fast_mcp_local.server`
- [ ] Test one CLI command
- [ ] Report any setup issues immediately

---

## Key Tasks for 2-Day Hackathon

### Day 1: Customization & Testing

**Morning (4 hours)**:
- Role 1: Add 20+ company PRBs to `docs/prbs/company/`
- Role 2: Customize templates in `prb_drafter.py`
- Role 3: Test all features with company data
- Role 4: Test AI integration with Claude/Copilot
- Role 5: Create presentation structure

**Afternoon (4 hours)**:
- Role 1: Test search quality, fix data issues
- Role 2: Customize scoring rules if needed
- Role 3: Create comprehensive test report
- Role 4: Record demo video
- Role 5: Create presentation slides (first draft)

### Day 2: Polish & Demo

**Morning (4 hours)**:
- All: Final testing and bug fixes
- Role 4: Refine demo scenarios
- Role 5: Polish presentation slides
- All: Rehearse presentation (2x)

**Afternoon (2 hours)**:
- All: Final presentation rehearsal
- All: Test A/V equipment
- All: Backup everything to cloud/USB
- All: Final checklist review

**Presentation (1 hour)**:
- Deliver 10-15 minute presentation
- Live demo (with video backup)
- Q&A

---

## Common Issues & Solutions

### Issue: "No PRBs found"
**Solution**:
```bash
# Check docs/prbs/ has .md files
ls -la docs/prbs/

# Re-index documents
rm documents.db
python3 -m fast_mcp_local.server
```

### Issue: "Tests failing"
**Solution**:
```bash
# Clean up database
rm documents.db

# Reinstall dependencies
pip install -e ".[dev]"

# Run tests with verbose output
pytest -v
```

### Issue: "MCP server won't start"
**Solution**:
```bash
# Check Python version (need 3.10+)
python3 --version

# Check for port conflicts
lsof -i :8000

# Run with debug output
python3 -m fast_mcp_local.server --verbose
```

### Issue: "Templates don't match company format"
**Solution**:
```python
# Edit src/fast_mcp_local/prb_drafter.py
# Modify TEMPLATES dictionary (lines 72-381)
# Add/remove sections as needed
```

### Issue: "Scoring seems wrong"
**Solution**:
```python
# Edit src/fast_mcp_local/prb_analyzer.py
# Modify REQUIRED_SECTIONS (lines 34-41)
# Modify scoring weights (lines 192-203)
```

---

## Quick Commands Reference

```bash
# Search & Discovery
prb search "database timeout"
prb list
prb get "filename.md"

# Drafting & Templates
prb draft "incident description" --severity Critical --systems "api,db"
prb template --type critical
prb suggest my-draft.md

# Analysis & Quality
prb analyze my-prb.md
prb validate my-prb.md
prb parse my-prb.md

# Action Items
prb actions my-prb.md

# Development
pytest                              # Run all tests
pytest -v                           # Verbose output
python3 -m fast_mcp_local.server   # Start MCP server

# Git
git status
git add .
git commit -m "message"
git push
```

---

## Success Criteria

**By End of Day 1**:
- [ ] 20+ company PRBs indexed and searchable
- [ ] Templates customized for company format
- [ ] All 10 MCP tools tested and working
- [ ] AI integration (Claude/Copilot) tested
- [ ] Demo scenarios prepared
- [ ] Presentation slides created (first draft)
- [ ] All tests passing

**By End of Day 2**:
- [ ] Final testing complete
- [ ] Demo video recorded (backup)
- [ ] Presentation slides polished
- [ ] Presentation rehearsed 3+ times
- [ ] A/V equipment tested
- [ ] Team ready to present

---

## Demo Flow (5-7 minutes)

### Demo 1: Search Past PRBs (1-2 min)
```bash
prb search "database connection pool"
# Shows: 3 relevant past PRBs with snippets
# Impact: 97% faster than manual search (15-20 min → 30 sec)
```

### Demo 2: Draft New PRB (2-3 min)
```bash
prb draft "API gateway returned 503 errors at 14:30, database connection pool exhausted" \
  --severity Critical \
  --systems "api-gateway,database"
# Shows: Complete PRB draft with all sections
# Impact: 87% faster PRB creation (2-4 hours → 15-30 min)
```

### Demo 3: Analyze PRB Quality (2 min)
```bash
prb analyze my-draft-prb.md
# Shows: Completeness score (75.5%), grade (C)
# Shows: Weaknesses and improvement suggestions
# Impact: Objective quality metrics, ensures nothing is missed
```

### Demo 4: AI Integration (optional, 1-2 min)
```
# In Claude Code or GitHub Copilot Chat
"Search for past database incidents"
"Draft a PRB for the API outage we just had"
# Shows: AI can use PRB tools automatically
```

---

## Backup Plans

**If Live Demo Fails**:
1. Play pre-recorded video
2. Show screenshots with narration
3. Describe workflows verbally

**If Presentation Laptop Fails**:
1. Switch to backup laptop (have project ready)
2. Use phone/tablet to present slides
3. Whiteboard the architecture

**If Internet Down**:
1. All demos work offline (no API dependencies)
2. Have presentation slides on USB drive
3. Have demo video on USB drive

---

## Emergency Contacts

**During Hackathon**:
- Team Slack: `#hackathon-prb-assistant`
- Team Lead: [Name, Phone]
- Technical Issues: [Name, Phone]
- A/V Support: [Name, Phone]

---

## Motivational Reminder

**Remember**:
- ✅ **Done is better than perfect** - Focus on working demo
- ✅ **Impact over features** - Show ROI and business value
- ✅ **Practice makes perfect** - Rehearse presentation 3+ times
- ✅ **Have fun!** - This is a hackathon, enjoy it!

---

**You've got this! 🚀**

**Presentation Time**: [Date/Time]

**Let's win this hackathon!** 🏆
