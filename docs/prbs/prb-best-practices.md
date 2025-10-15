# PRB Best Practices for SRE Teams

## What is a PRB?

A PRB (Problem Record) is a detailed document that captures:
- What happened during an incident
- Why it happened (root cause)
- How it was resolved
- How to prevent it from happening again
- Lessons learned for the team

## When to Create a PRB

Create a PRB for:
- **Critical incidents**: Customer-impacting outages
- **High severity**: Significant degradation of service
- **Recurring issues**: Problems that happen multiple times
- **Near misses**: Issues caught before customer impact
- **Learning opportunities**: Incidents with valuable lessons

## PRB Structure

###  1. Incident Summary
Quick overview with key metadata:
- PRB ID, Date, Severity, Status
- Affected systems
- Customer/business impact
- Duration

**Best Practice**: Write this section first, update as incident progresses

### 2. Timeline
Chronological sequence of events, actions, and observations

**Best Practices**:
- Use precise timestamps (HH:MM in consistent timezone)
- Include both automated alerts and human actions
- Note when key decisions were made
- Document communication with stakeholders
- Minimum 3-5 timeline entries

**Example**:
```
- 14:30 - CloudWatch alarm: API 5xx rate > 10%
- 14:32 - SRE on-call acknowledged, started investigation
- 14:35 - Identified database connection pool exhausted
- 14:40 - Killed slow queries, pool recovered
- 14:50 - Services healthy, error rate normal
```

### 3. Root Cause Analysis
Detailed technical explanation of what caused the incident

**Best Practices**:
- Explain the PRIMARY cause
- List CONTRIBUTING factors
- Use "5 Whys" technique to dig deep
- Include code snippets, configs, or logs if relevant
- Avoid blame - focus on systems and processes

**Template**:
```markdown
## Root Cause Analysis
[What actually caused the failure]

### Contributing Factors
- [Factor 1: Why it wasn't caught earlier]
- [Factor 2: Why impact was severe]

### Why It Happened
[Systemic reasons behind the incident]
```

### 4. Resolution
What was done to resolve the incident

**Best Practices**:
- Separate immediate actions from permanent fixes
- Explain verification steps
- Include rollback plans if applicable

**Template**:
```markdown
## Resolution
### Immediate Actions
1. [Emergency fix]
2. [Mitigation step]

### Permanent Fix
[Long-term solution]

### Verification
[How we confirmed it was fixed]
```

### 5. Action Items
Follow-up tasks with owners and due dates

**Best Practices**:
- Use checkboxes: `- [ ]` or `- [x]`
- **Always** include owner: `@username`
- **Always** include due date: `YYYY-MM-DD`
- Prioritize: Immediate (P0), Short-term (P1), Long-term (P2)
- Be specific and actionable

**Example**:
```markdown
## Action Items
- [ ] Add database connection pool monitoring (Owner: @sre-team, Due: 2024-01-20)
- [ ] Implement query timeout (Owner: @backend-team, Due: 2024-01-22)
- [ ] Update load testing to include new endpoints (Owner: @qa-team, Due: 2024-02-01)
```

### 6. Prevention
How to prevent this from happening again

**Best Practices**:
- Separate short-term and long-term measures
- Focus on systems, not people
- Include monitoring, alerting, process changes
- Reference action items

**Template**:
```markdown
## Prevention
### Short-term Measures
- [Quick wins, implemented immediately]

### Long-term Improvements
- [Strategic changes, require more time]
```

### 7. Lessons Learned
Key insights and improvements

**Best Practices**:
- Be honest: what went well, what didn't
- Focus on learning, not blame
- Acknowledge what you got lucky with
- Share widely with team

**Template**:
```markdown
## Lessons Learned
### What Went Well
- [Positive aspect 1]

### What Could Be Improved
- [Area for improvement 1]

### What We Got Lucky With
- [Things that could have made it worse]
```

## Writing Tips

### Be Specific
❌ Bad: "Database was slow"
✅ Good: "Query on users table took 45 seconds due to missing index on created_at column"

### Use Data
❌ Bad: "Many customers affected"
✅ Good: "1,247 customers affected (15% of active users during incident window)"

### Write for Your Audience
- **Engineering team**: Include technical details, code snippets, metrics
- **Leadership**: Add business impact, customer impact, cost
- **Future responders**: Document runbook steps that worked

### Update as You Go
- Start PRB as soon as incident is declared
- Update timeline in real-time
- Fill in analysis sections after resolution
- Schedule post-incident review within 24-48 hours

## Severity Guidelines

### Critical
- Complete service outage
- Data loss or corruption
- Security breach
- **PRB Required**: Yes, within 24 hours

### High
- Significant service degradation
- Multiple users affected
- SLA breach
- **PRB Required**: Yes, within 48 hours

### Medium
- Minor service degradation
- Small subset of users affected
- No SLA breach
- **PRB Required**: Recommended

### Low
- Internal issue, no customer impact
- Successfully prevented incident
- **PRB Required**: Optional (good for learning)

## PRB Templates

### Standard Template
Use for most incidents (High/Medium severity)

### Critical Incident Template
Use for complete outages, data loss, security breaches
- Includes executive summary
- More detailed impact analysis
- Post-incident review section

### Postmortem Template
Use for detailed retrospective analysis
- Timeline in table format
- "What went well" / "What went wrong"
- "Where we got lucky"

## Common Mistakes to Avoid

### 1. Vague Timeline
❌ "Issue occurred in the afternoon"
✅ "14:35 - Database connection pool exhausted"

### 2. Missing Action Items
Every PRB should have 3-5 concrete action items with owners

### 3. Blame Culture
❌ "John deployed bad code"
✅ "Code review process didn't catch missing index"

### 4. Missing Prevention
Always explain how to prevent recurrence

### 5. No Follow-up
Track action items to completion, don't let PRBs collect dust

## Using PRB Tools

### Drafting a New PRB
```bash
# Generate from incident description
prb draft "API gateway returned 503 errors due to database timeout"

# Use a template
prb template critical
```

### Analyzing Existing PRB
```bash
# Check completeness
prb analyze my-prb.md

# Validate structure
prb validate my-prb.md

# Extract action items
prb actions my-prb.md
```

### Searching Past PRBs
```bash
# Find similar incidents
prb search "database connection pool"

# List all PRBs
prb list
```

## Post-Incident Review

Schedule within 24-48 hours of incident resolution

**Agenda**:
1. Review timeline (10 min)
2. Discuss root cause (15 min)
3. Review action items (10 min)
4. Discuss prevention measures (15 min)
5. Capture lessons learned (10 min)

**Attendees**:
- Incident responders
- Service owners
- SRE team lead
- Engineering manager (for critical incidents)

**Output**:
- Finalized PRB document
- Agreed action items with owners
- Any process improvements identified

## Sharing PRBs

### Internal Sharing
- Post in engineering Slack channel
- Add to PRB repository/wiki
- Reference in sprint retrospectives
- Include in onboarding materials

### External Communication
For customer-facing incidents:
- Write separate customer-facing summary
- Focus on impact and resolution
- Less technical detail
- Emphasize prevention measures

## Measuring Success

Good PRB practices lead to:
- Faster incident response (learned from past incidents)
- Fewer recurring incidents (prevention measures work)
- Better team collaboration (shared understanding)
- Improved systems (action items completed)

**Metrics to track**:
- Mean time to detection (MTTD)
- Mean time to resolution (MTTR)
- Recurring incident rate
- Action item completion rate

## Resources

- [Google SRE Book - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [Atlassian Incident Postmortem Guide](https://www.atlassian.com/incident-management/postmortem)
- [PagerDuty Postmortem Template](https://postmortems.pagerduty.com/)

## Examples

See `examples/` directory for real PRB examples:
- `prb-2024-001-database-connection-pool-exhaustion.md`
- `prb-2024-002-memory-leak-kubernetes-pod.md`

---

**Remember**: The goal of a PRB is to LEARN and IMPROVE, not to assign blame. Focus on systems, processes, and how we can do better next time.
