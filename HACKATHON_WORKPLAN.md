# 2-Day Hackathon Work Plan - PRB SRE Assistant

**Project**: PRB SRE Assistant - AI-powered Problem Record management for SRE teams
**Duration**: 2 Days (16 hours total)
**Team Size**: 3-5 members
**Goal**: Customize PRB Assistant for company use and deliver compelling demo

---

## Executive Summary

### What We're Building

**PRB SRE Assistant is already implemented** with 10 MCP tools for complete PRB lifecycle management. This hackathon focuses on:

1. **Adding company PRB data** (20+ past incidents)
2. **Customizing templates** for company PRB format
3. **Testing with real data** from your incident management system
4. **Integrating with AI tools** (Claude Code, GitHub Copilot)
5. **Creating winning presentation** (15-20 slides + 5-7 min demo)

### Success Criteria

**Day 1 End**: 20+ PRBs indexed, templates customized, demo ready
**Day 2 End**: Presentation polished, rehearsed 3+ times, ready to win! 🏆

---

## Team Roles

| Role | Primary Responsibility | Key Deliverable | Time Investment |
|------|------------------------|-----------------|-----------------|
| **SRE/Content Manager** | Add company PRB data | 20+ PRBs indexed and searchable | 40% data, 30% testing, 30% presentation |
| **Backend Developer** | Customize templates & scoring | Company-specific templates working | 50% customization, 30% testing, 20% presentation |
| **QA Engineer** | Test all features thoroughly | Comprehensive test report | 60% testing, 20% documentation, 20% presentation |
| **DevEx Engineer** | AI integration & demo prep | Working demos + backup video | 50% AI integration, 40% demo prep, 10% presentation |
| **DevOps/Presenter** | Infrastructure & presentation | Polished slides + smooth demo | 60% presentation, 30% demo setup, 10% infrastructure |

---

## Day 1: Customization & Testing (8 hours)

### Morning Session (9:00 AM - 1:00 PM)

#### Hour 1: Team Kickoff (9:00 AM - 10:00 AM)

**Everyone (30 min)**: Team standup
- Review project goals and deliverables
- Assign roles and specific tasks
- Set up Slack channel: `#hackathon-prb-assistant`
- Create shared Google Doc for notes/issues
- Review existing codebase walkthrough

**Everyone (30 min)**: Environment verification
- [ ] Run tests: `pytest` (verify 25 tests pass)
- [ ] Start MCP server: `python3 -m fast_mcp_local.server`
- [ ] Test CLI: `prb search "database"`
- [ ] Test example: `prb analyze docs/prbs/examples/prb-2024-001-database-connection-pool-exhaustion.md`
- [ ] Report any setup issues immediately

---

#### Hour 2: Data Collection & Setup (10:00 AM - 11:00 AM)

**SRE/Content Manager**:
- [ ] Access company incident management system (Jira, ServiceNow, Confluence)
- [ ] Export 5-10 past PRBs to markdown format
- [ ] Create `docs/prbs/company/` directory
- [ ] Add first batch of PRBs
- [ ] Test indexing: restart MCP server and search

**Backend Developer**:
- [ ] Review company PRB template/format
- [ ] Identify required vs optional sections for company
- [ ] Review `src/fast_mcp_local/prb_drafter.py` (templates lines 72-381)
- [ ] Review `src/fast_mcp_local/prb_analyzer.py` (scoring lines 34-51)
- [ ] Plan customization approach

**QA Engineer**:
- [ ] Test all 10 CLI commands systematically
- [ ] Document expected vs actual behavior
- [ ] Create comprehensive test checklist
- [ ] Set up test results tracking document
- [ ] Identify any bugs or issues

**DevEx Engineer**:
- [ ] Install Claude Code CLI (if using Claude)
- [ ] Configure GitHub Copilot in VS Code (if using Copilot)
- [ ] Test MCP server integration with AI tool
- [ ] Create list of 5-7 demo scenarios
- [ ] Take baseline screenshots

**DevOps/Presenter**:
- [ ] Create presentation outline (15-20 slides structure)
- [ ] Plan demo flow (5-7 minutes total)
- [ ] Set up demo laptop and test
- [ ] Test projector connection and A/V
- [ ] Create backup plan document

---

#### Hour 3: Implementation Begins (11:00 AM - 12:00 PM)

**SRE/Content Manager**:
- [ ] Add 10+ more company PRBs (total 15+ so far)
- [ ] Test search with company-specific terminology
- [ ] Note any formatting inconsistencies in exported PRBs
- [ ] Document data quality issues to address

**Backend Developer**:
- [ ] Start customizing PRB templates in `prb_drafter.py`
- [ ] Add company-specific sections (e.g., "Customer Impact", "SLA Status")
- [ ] Test draft generation: `prb draft "Test incident" --severity High`
- [ ] Verify auto-populated metadata matches company needs

**QA Engineer**:
- [ ] Test with first batch of company PRBs
- [ ] Verify search returns relevant results for company data
- [ ] Test draft generation with real incident descriptions from company
- [ ] Log all issues in shared Google Doc with severity

**DevEx Engineer**:
- [ ] Create 3-5 specific demo prompts for AI
- [ ] Test Claude Code: `claude code "Search for database incidents in our PRBs"`
- [ ] Test GitHub Copilot Chat with MCP integration
- [ ] Document what works well vs what doesn't
- [ ] Start planning demo script

**DevOps/Presenter**:
- [ ] Start creating presentation slides
- [ ] Problem statement slides (2 slides: current pain points)
- [ ] Solution overview slides (2 slides: PRB Assistant capabilities)
- [ ] Begin planning demo flow with timing

---

#### Hour 4: Deep Work (12:00 PM - 1:00 PM)

**SRE/Content Manager**:
- [ ] Reach target: 20+ company PRBs indexed
- [ ] Test search with various keywords and phrases
- [ ] Verify all PRBs are discoverable
- [ ] Create list of sample search queries for demo

**Backend Developer**:
- [ ] Complete template customization for all 3 templates
- [ ] Test standard, critical, and postmortem templates
- [ ] Customize scoring rules if needed (`prb_analyzer.py`)
- [ ] Test analysis: `prb analyze company-prb.md`

**QA Engineer**:
- [ ] Complete initial feature testing checklist
- [ ] Test edge cases (empty PRBs, malformed markdown)
- [ ] Verify action item extraction with company format
- [ ] Test with 5+ diverse company PRBs

**DevEx Engineer**:
- [ ] Refine AI demo scenarios based on testing
- [ ] Record successful interactions (screenshots/screen recording)
- [ ] Test all 3 main demos (search, draft, analyze)
- [ ] Create backup plan if live AI demo fails

**DevOps/Presenter**:
- [ ] Complete presentation structure (all slide titles)
- [ ] Add demo slides (3-4 slides with placeholders)
- [ ] Add business value slides (ROI, time savings metrics)
- [ ] Add production roadmap slide (8-week plan)

---

**LUNCH BREAK (1:00 PM - 2:00 PM)** 🍕

---

### Afternoon Session (2:00 PM - 6:00 PM)

#### Hour 5: Polish & Integration (2:00 PM - 3:00 PM)

**SRE/Content Manager**:
- [ ] Improve PRB data quality (fix any formatting issues)
- [ ] Add missing metadata to PRBs if needed
- [ ] Create 2-3 "golden" PRB examples for demo
- [ ] Test and document search relevance quality

**Backend Developer**:
- [ ] Fine-tune template output based on testing
- [ ] Test with 10+ different real incident descriptions
- [ ] Verify scoring is reasonable for company PRBs
- [ ] Document any remaining customization needs

**QA Engineer**:
- [ ] Run full test suite: `pytest -v`
- [ ] Fix any broken tests if found
- [ ] Create comprehensive test report document
- [ ] Sign off on quality if all tests pass

**DevEx Engineer**:
- [ ] Start recording demo video (backup plan)
- [ ] Record search demo (1-2 min)
- [ ] Record draft PRB demo (2-3 min)
- [ ] Record analyze PRB demo (1-2 min)

**DevOps/Presenter**:
- [ ] Finalize all presentation slides
- [ ] Add screenshots and visuals to slides
- [ ] Create Q&A preparation document
- [ ] Test presentation flow and timing

---

#### Hour 6: First Demo Rehearsal (3:00 PM - 4:00 PM)

**Everyone**: Demo rehearsal #1

**DevEx Engineer (lead)**:
- Present demo flow (aim for 5-7 minutes)
- Demo 1: Search past PRBs (1-2 min)
- Demo 2: Draft new PRB (2-3 min)
- Demo 3: Analyze PRB quality (2 min)
- Demo 4 (optional): AI integration (1 min)

**Team Feedback Session**:
- What worked well?
- What needs improvement?
- Timing adjustments needed?
- Identify potential failure points
- Discuss backup plans

**Action Items from Feedback**:
- [ ] Polish demo scripts
- [ ] Fix identified issues
- [ ] Adjust timing
- [ ] Prepare backup materials

---

#### Hour 7: Documentation & Testing (4:00 PM - 5:00 PM)

**SRE/Content Manager**:
- [ ] Document PRB data collection process for company
- [ ] Create guide for adding more PRBs in future
- [ ] Note data quality requirements and best practices
- [ ] Prepare answers for data-related questions

**Backend Developer**:
- [ ] Document all customizations made (with line numbers)
- [ ] Create "how to customize for your company" guide
- [ ] Prepare technical architecture explanation
- [ ] Prepare for technical Q&A

**QA Engineer**:
- [ ] Finalize comprehensive test report
- [ ] Document all features tested with results
- [ ] List any known issues and workarounds
- [ ] Create Day 2 smoke test checklist

**DevEx Engineer**:
- [ ] Finish recording and editing demo video
- [ ] Add voiceover or captions if helpful
- [ ] Export to multiple formats for backup
- [ ] Upload to cloud (Google Drive/Dropbox) + USB drive

**DevOps/Presenter**:
- [ ] Complete all presentation slides (100%)
- [ ] Add team member photos/names to intro slide
- [ ] Create backup slides (text-only in case demo fails)
- [ ] Print speaker notes or handouts if needed

---

#### Hour 8: Day 1 Wrap-up (5:00 PM - 6:00 PM)

**Everyone (30 min)**: Full presentation rehearsal #2
- Complete presentation flow (10-15 min total)
- Live demo with timer (5-7 min)
- Practice transitions between speakers
- Q&A practice with common questions

**Everyone (15 min)**: Feedback and improvements
- What worked well in rehearsal?
- What still needs fixing?
- Timing issues identified?
- Role clarity and handoffs
- Demo execution quality

**Everyone (15 min)**: Day 2 planning
- Review remaining tasks for morning
- Confirm morning priorities and schedule
- Set final rehearsal times
- Confirm emergency contacts
- Assign morning tasks

**End of Day 1 Checklist**:
- [ ] 20+ company PRBs indexed and searchable
- [ ] Templates customized for company format
- [ ] All 10 MCP tools tested and working
- [ ] AI integration tested
- [ ] Demo scenarios prepared and rehearsed
- [ ] Presentation slides 100% complete
- [ ] Demo video recorded (backup)
- [ ] All tests passing (25 tests)
- [ ] Team confident about tomorrow

---

## Day 2: Polish & Presentation (8 hours)

### Morning Session (9:00 AM - 1:00 PM)

#### Hour 9: Final Testing (9:00 AM - 10:00 AM)

**Everyone (15 min)**: Morning standup
- Review Day 1 accomplishments
- Confirm Day 2 priorities
- Address any overnight concerns
- Final role assignments

**SRE/Content Manager (45 min)**:
- [ ] Final PRB data verification (all indexed correctly)
- [ ] Test search with exact demo keywords
- [ ] Prepare PRB statistics (count, topics, time periods)
- [ ] Prepare for data-related questions from judges

**Backend Developer (45 min)**:
- [ ] Final template testing with edge cases
- [ ] Run full test suite one more time: `pytest -v`
- [ ] Review technical architecture for Q&A
- [ ] Document any last-minute adjustments made

**QA Engineer (45 min)**:
- [ ] Run smoke tests on demo laptop
- [ ] Verify all CLI commands work perfectly
- [ ] Test MCP server startup (timing and output)
- [ ] Confirm database is fully indexed
- [ ] Verify backup laptop is ready

**DevEx Engineer (45 min)**:
- [ ] Test AI integration one final time
- [ ] Verify demo video plays correctly (test multiple players)
- [ ] Organize backup demo materials (screenshots, scripts)
- [ ] Check all demo screenshots are clear and labeled

**DevOps/Presenter (45 min)**:
- [ ] Test presentation laptop + projector connection
- [ ] Verify slides display correctly on projector
- [ ] Test presentation clicker/remote
- [ ] Confirm backup laptop is configured identically
- [ ] Test screen sharing if presenting remotely

---

#### Hour 10: Presentation Polish (10:00 AM - 11:00 AM)

**Everyone**: Final presentation refinement

**DevOps/Presenter (lead)**:
- [ ] Review each slide for clarity and consistency
- [ ] Ensure consistent formatting across all slides
- [ ] Add detailed speaker notes to each slide
- [ ] Time each section with stopwatch

**Content Improvements**:
- [ ] Add transitions between major sections
- [ ] Highlight key metrics (87% faster, $4.2M savings, 1,300% ROI)
- [ ] Add compelling visuals where appropriate
- [ ] Ensure fonts are readable from back of room (48pt+ for body text)
- [ ] Check color contrast for visibility

**Team Review Questions**:
- Does each slide support our story effectively?
- Are metrics easy to understand at a glance?
- Is demo flow clearly explained?
- Are we within time limit?
- Is the "ask" clear at the end?

---

#### Hour 11: Rehearsal #3 (11:00 AM - 12:00 PM)

**Everyone**: Full presentation rehearsal with strict timer

**Presentation Flow** (10-15 min total):

1. **Introduction** (1 min) - DevOps/Presenter
   - Team introduction with names and roles
   - Hook: "SREs spend 2-4 hours on each PRB"
   - Our solution in one sentence

2. **Problem Statement** (1-2 min) - SRE/Content Manager
   - Current SRE pain points (time, quality, learning)
   - Show real impact: 60-70% incomplete PRBs
   - Cost: $50K-$100K annually per team wasted

3. **Technical Solution** (2 min) - Backend Developer
   - Architecture overview (PRB Analyzer + Drafter + Search)
   - 10 MCP tools across 4 capabilities
   - Technology stack (FastMCP, SQLite FTS5, Python)
   - Emphasize: Already implemented, production-ready

4. **Live Demo** (5-7 min) - DevEx Engineer
   - **Demo 1**: Search past PRBs (1-2 min)
     - Show search for "database timeout"
     - Highlight: 97% faster (15-20 min → 30 sec)
   - **Demo 2**: Draft new PRB (2-3 min)
     - Draft from incident description
     - Show auto-populated structure
     - Highlight: 87% faster (2-4 hours → 15-30 min)
   - **Demo 3**: Analyze PRB quality (2 min)
     - Show scoring (85.5%, Grade B)
     - Show weaknesses and suggestions
     - Highlight: Objective quality metrics
   - **Demo 4** (optional): AI integration (1 min)
     - Quick Claude Code or Copilot demo

5. **Business Value** (2 min) - SRE/Content Manager
   - Productivity gains table (87% faster, 35% better quality)
   - Cost savings: $847.5K per team annually
   - ROI: 1,300% first year, payback < 2 months
   - For 5 teams: $4.2M annually

6. **Production Roadmap** (1 min) - DevOps/Presenter
   - 8-week implementation plan
   - 4 phases: deployment → integration → features → hardening
   - Next steps: Pilot with 1 team, expand to 5 teams

7. **Q&A** (3-5 min) - Everyone
   - Prepared answers for common questions
   - Each person covers their domain expertise

**Post-Rehearsal Feedback**:
- Timing acceptable? (adjust if needed)
- Transitions smooth between speakers?
- Demos work flawlessly?
- Message clear and compelling?
- Ready for Q&A?

---

**LUNCH BREAK (12:00 PM - 1:00 PM)** 🍕

**Use lunch to**:
- Relax and destress
- Stay hydrated
- Light meal (don't overeat before presenting)
- Mental preparation
- Review speaker notes if helpful

---

### Afternoon Session (1:00 PM - 6:00 PM)

#### Hour 12: Final Rehearsal & Q&A Prep (1:00 PM - 2:00 PM)

**Everyone (30 min)**: Final full rehearsal #4

**Focus on**:
- [ ] Polishing any remaining rough spots
- [ ] Perfecting demo execution
- [ ] Smooth transitions and handoffs
- [ ] Confident delivery and energy
- [ ] Backup plan readiness

**Everyone (30 min)**: Q&A preparation session

**Common Questions to Prepare**:

1. **"How does this scale to 100+ SRE teams?"**
   - Answer (DevOps): SQLite handles 1000+ PRBs easily, can migrate to PostgreSQL for enterprise scale, horizontal scaling with load balancer

2. **"What about security and data privacy?"**
   - Answer (Backend Dev): On-premise deployment, data never leaves company network, authentication/authorization in Phase 1, audit logging available

3. **"How do we keep PRB templates updated?"**
   - Answer (Backend Dev): Templates are code (Python), version controlled, easy to update, can have multiple template versions

4. **"Can this integrate with our incident management system?"**
   - Answer (DevEx): Yes, Phase 2 includes PagerDuty, ServiceNow, Jira integration, MCP protocol makes integration straightforward

5. **"What's the actual production deployment timeline?"**
   - Answer (DevOps): 8 weeks with 2-3 developers, Phase 1 (2 weeks) gets basic functionality live, iterative rollout after that

6. **"How much does this cost to run in production?"**
   - Answer (DevOps): Minimal - Python app, SQLite database, ~$1K/year infrastructure for 100 users, primary cost is developer time

7. **"What if our PRB format is different?"**
   - Answer (Backend Dev): Templates are fully customizable (we can show code), takes 1-2 hours to adapt to new format

8. **"How do you handle PRB data quality issues?"**
   - Answer (SRE/Content): Search works even with inconsistent data, scoring system identifies incomplete PRBs, guide teams to improve quality

**Assign Question Owners**:
- Backend Developer: Technical/architecture/customization
- SRE/Content Manager: Data quality/PRB format/business process
- DevEx Engineer: AI integration/MCP protocol/tooling
- DevOps/Presenter: Deployment/scaling/infrastructure/cost
- QA Engineer: Testing/quality/reliability/performance

---

#### Hour 13-14: Buffer Time & Final Prep (2:00 PM - 4:00 PM)

**Use this buffer time for**:
- [ ] Addressing any last-minute issues
- [ ] Additional rehearsals if team requests
- [ ] Creating any missing backup materials
- [ ] Mental preparation and rest
- [ ] Reviewing notes
- [ ] Staying energized and positive

**Specific Final Tasks**:

**SRE/Content Manager**:
- [ ] Review PRB statistics one more time
- [ ] Prepare specific data quality examples to show
- [ ] Practice business value talking points
- [ ] Relax and stay confident

**Backend Developer**:
- [ ] Review codebase structure for demo
- [ ] Practice explaining architecture clearly
- [ ] Have technical answers rehearsed
- [ ] Double-check templates work

**QA Engineer**:
- [ ] Final smoke test 30 minutes before presentation
- [ ] Verify backup laptop configured correctly
- [ ] Have test report easily accessible
- [ ] Be ready to answer quality/testing questions

**DevEx Engineer**:
- [ ] Practice demo one more time on demo laptop
- [ ] Verify demo video is on multiple devices
- [ ] Prepare backup demo materials (screenshots)
- [ ] Mental preparation for live demo

**DevOps/Presenter**:
- [ ] Load presentation on USB drive (backup)
- [ ] Upload to cloud (Google Drive, Dropbox)
- [ ] Print speaker notes if helpful
- [ ] Review opening and closing remarks
- [ ] Stay calm, confident, energized

**Everyone**:
- [ ] Dress appropriately (business casual or as appropriate)
- [ ] Check appearance (camera-ready if recorded)
- [ ] Bring water bottle
- [ ] Have backup materials organized

---

#### Hour 15: Pre-Presentation Setup (4:00 PM - 5:00 PM)

**Everyone (30 min)**: Venue setup and equipment testing

**Venue Setup Checklist**:
- [ ] Test projector connection thoroughly
- [ ] Test presentation laptop (load slides, navigate through)
- [ ] Test internet connection if needed for demo
- [ ] Test audio if using video with sound
- [ ] Test demo laptop and environment
- [ ] Have backup laptop connected and ready
- [ ] Have demo video accessible on multiple devices
- [ ] Have USB drives with all materials ready
- [ ] Test screen sharing if remote presentation
- [ ] Verify clicker/remote works from back of room

**Final Slide Check**:
- [ ] Slides display correctly on projector
- [ ] Fonts are readable from back of room
- [ ] Colors look good (not washed out)
- [ ] Animations work if any
- [ ] Transitions are smooth

**Demo Environment Check**:
- [ ] MCP server starts correctly
- [ ] All CLI commands work
- [ ] Database is indexed with company PRBs
- [ ] Search returns expected results
- [ ] Draft generation works
- [ ] Analysis returns good scores
- [ ] Network is stable (if needed)

**Everyone (15 min)**: Team mental preparation
- Deep breaths and relaxation
- Positive visualization
- Remember: "We've built something amazing"
- Trust the preparation and rehearsals
- Support each other

**Everyone (15 min)**: Final team huddle
- Confirm speaker order and roles
- Check equipment one last time
- Address any last-minute concerns
- Team motivational moment
- Group fist bump or team cheer
- "Let's win this!" 🏆

---

#### Hour 16: PRESENTATION TIME! (5:00 PM - 6:00 PM)

**Showtime!** (10-15 min presentation + Q&A)

**Presentation Flow**:
1. Introduction (1 min)
2. Problem Statement (1-2 min)
3. Technical Solution (2 min)
4. **Live Demo** (5-7 min) - The star of the show!
5. Business Value (2 min)
6. Production Roadmap (1 min)
7. Q&A (3-5 min)

**Demo Backup Plan** (if something goes wrong):
- **Plan A**: Live demo (preferred)
- **Plan B**: Pre-recorded demo video
- **Plan C**: Screenshots with narration
- **Plan D**: Verbal walkthrough with architecture diagram

**During Presentation**:
- Speak clearly and project voice
- Make eye contact with audience/judges
- Show energy and enthusiasm
- Handle technical issues gracefully
- Support teammates during their sections
- Smile and enjoy the moment!

**During Q&A**:
- Listen carefully to each question
- Clarify if question is unclear
- Defer to appropriate team member
- Be honest if you don't know something
- Keep answers concise (1-2 minutes max)
- Thank judges for questions

**After Presentation**:
- [ ] Thank the audience and judges
- [ ] Answer any follow-up questions
- [ ] Network with judges and attendees
- [ ] Collect business cards if appropriate
- [ ] Gather feedback informally
- [ ] Take photos with team
- [ ] CELEBRATE THE ACCOMPLISHMENT! 🎉🏆

---

## Success Metrics & Evaluation

### End of Day 1 Checklist:
- [ ] **PRB Data**: 20+ company PRBs indexed and searchable
- [ ] **Customization**: Templates customized for company format
- [ ] **Testing**: All 10 MCP tools tested and working
- [ ] **AI Integration**: Claude Code or Copilot tested successfully
- [ ] **Demo Ready**: Demo scenarios prepared and rehearsed once
- [ ] **Presentation**: Slides 100% complete
- [ ] **Backup**: Demo video recorded
- [ ] **Quality**: All 25 tests passing

### End of Day 2 Checklist:
- [ ] **Final Testing**: All features verified on demo laptop
- [ ] **Rehearsals**: Presentation rehearsed 3+ times
- [ ] **Equipment**: All A/V equipment tested
- [ ] **Backup Plans**: Multiple backup plans in place
- [ ] **Q&A Prep**: Common questions prepared with answers
- [ ] **Team Ready**: Team confident, energized, ready to present
- [ ] **Materials**: Slides, demo, video all accessible

### Presentation Quality Metrics:
- [ ] **Timing**: Presentation fits within time limit (10-15 min)
- [ ] **Demo**: Live demo works flawlessly or backup ready
- [ ] **Clarity**: Message is clear and compelling
- [ ] **Energy**: Team shows enthusiasm and confidence
- [ ] **Q&A**: Questions answered confidently
- [ ] **Impact**: Judges understand the value and ROI

---

## Risk Mitigation Strategy

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Live demo fails during presentation | Medium | High | Have video backup + screenshots + verbal walkthrough prepared |
| Company PRB data has quality issues | High | Medium | Test extensively on Day 1, document known issues, show how tool handles imperfect data |
| Presentation runs too long | Medium | Medium | Practice with timer, have "must-say" vs "nice-to-say" marked on slides |
| Technical questions we can't answer | Low | Medium | Prepare comprehensive Q&A doc, be honest and offer to follow up |
| Team member unavailable Day 2 | Low | High | Cross-train on roles, have backup person for each role |
| Projector/laptop issues | Medium | High | Have backup laptop configured identically, test early |
| Network goes down during demo | Low | Medium | All demos work offline (no API dependencies), verify before presenting |
| Templates don't match company format perfectly | Medium | Low | Show customization process, emphasize easy to adapt |

---

## Communication & Coordination

### Communication Channels

**Slack Channel**: `#hackathon-prb-assistant`
- Use for: Quick questions, status updates, issue tracking, coordination
- Response expectation: < 15 minutes during hackathon hours

**Shared Google Doc**: Real-time collaborative notes
- Use for: Detailed notes, test results, feedback, Q&A prep
- Update continuously throughout both days

**Video Call** (if team is distributed):
- Use for: Standup meetings, rehearsals, coordination
- Tool: Zoom/Meet/Teams

### Check-in Schedule

| Time | Type | Duration | Purpose |
|------|------|----------|---------|
| 9:00 AM (Day 1 & 2) | Morning Standup | 15 min | Set daily priorities |
| 12:30 PM (Day 1 & 2) | Midday Sync | 10 min | Progress check |
| 5:30 PM (Day 1) | End-of-Day Review | 30 min | Day 1 wrap-up, Day 2 planning |
| 4:45 PM (Day 2) | Pre-Presentation Huddle | 15 min | Final check and motivation |

---

## Emergency Contacts & Support

**During Hackathon**:
- **Team Lead**: [Name, Phone, Email]
- **Technical Support**: [Name, Phone, Email]
- **A/V Support**: [Venue Contact, Phone]
- **Hackathon Organizers**: [Contact Info]

**Resources**:
- **GitHub Repository**: https://github.com/karthik78180/fast-mcp-local (branch: feature/prb-sre-assistant)
- **Documentation**: All docs in repo (README.md, FEATURES.md, etc.)
- **Example PRBs**: `docs/prbs/examples/`
- **Best Practices**: `docs/prbs/prb-best-practices.md`

---

## Motivational Reminders

> **"Done is better than perfect."** - Sheryl Sandberg

> **"The only way to do great work is to love what you do."** - Steve Jobs

> **"Innovation distinguishes between a leader and a follower."** - Steve Jobs

### Remember:
- ✅ **Focus on impact** - Show how this saves time and money
- ✅ **Tell a story** - Make it relatable to SRE teams
- ✅ **Practice makes perfect** - Rehearse until it's smooth
- ✅ **Support each other** - We win as a team
- ✅ **Have fun!** - Enjoy the hackathon experience
- ✅ **Be proud** - We've built something truly valuable

---

## Quick Reference Commands

### Most Used Commands

```bash
# Start MCP server
python3 -m fast_mcp_local.server

# Run tests
pytest
pytest -v  # verbose

# CLI commands
prb search "database timeout"
prb list
prb draft "incident description" --severity Critical
prb template --type standard
prb analyze my-prb.md
prb validate my-prb.md
prb actions my-prb.md

# Git commands
git status
git add .
git commit -m "message"
git push origin feature/prb-sre-assistant
```

---

## Final Checklist - Use This Before Presenting!

### 30 Minutes Before Presentation:

**Equipment**:
- [ ] Presentation laptop charged and working
- [ ] Demo laptop charged and working
- [ ] Backup laptop configured and ready
- [ ] Projector connection tested
- [ ] Clicker/remote working
- [ ] USB drives with all materials
- [ ] Demo video accessible on 3 devices
- [ ] Internet connection tested (if needed)

**Materials**:
- [ ] Presentation slides loaded
- [ ] Demo environment ready (MCP server running)
- [ ] PRBs indexed and searchable
- [ ] All CLI commands tested
- [ ] Backup materials organized

**Team**:
- [ ] Everyone knows their part
- [ ] Speaking order confirmed
- [ ] Timing practiced
- [ ] Q&A answers reviewed
- [ ] Team is energized and confident

**Mental Preparation**:
- [ ] Deep breaths
- [ ] Positive mindset
- [ ] Remember the value we're delivering
- [ ] Trust the preparation
- [ ] Ready to win! 🏆

---

**Good luck, team! You've got this! 🚀**

**Let's show them how PRB SRE Assistant transforms incident management!**

**Let's win this hackathon! 🏆🎉**

---

**Last Updated**: For PRB SRE Assistant 2-day hackathon
**Branch**: `feature/prb-sre-assistant`
**Status**: Ready for hackathon execution! 🎉
