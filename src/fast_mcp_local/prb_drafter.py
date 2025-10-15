"""PRB (Problem Record) Drafter for SRE teams.

Generates PRB drafts from incident descriptions and provides templates.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional


class PRBDrafter:
    """Generates PRB drafts and templates."""

    def __init__(self):
        """Initialize PRB drafter."""
        self.templates = self._load_templates()

    def draft_prb(self, incident_description: str,
                  severity: str = "High",
                  affected_systems: Optional[List[str]] = None) -> str:
        """Generate a PRB draft from incident description.

        Args:
            incident_description: Description of the incident
            severity: Severity level (Critical/High/Medium/Low)
            affected_systems: List of affected systems

        Returns:
            PRB draft in markdown format
        """
        # Extract key information from description
        info = self._extract_incident_info(incident_description)

        # Generate PRB ID
        prb_id = self._generate_prb_id()

        # Generate title
        title = info.get("title", "Incident Summary")

        # Create draft
        draft = self._create_prb_template(
            prb_id=prb_id,
            title=title,
            description=incident_description,
            severity=severity,
            affected_systems=affected_systems or info.get("systems", []),
            suggested_root_cause=info.get("potential_cause"),
            suggested_actions=info.get("suggested_actions", [])
        )

        return draft

    def create_prb_from_template(self, template_type: str = "standard") -> str:
        """Create a blank PRB from template.

        Args:
            template_type: Template type (standard, critical, postmortem)

        Returns:
            PRB template in markdown format
        """
        template = self.templates.get(template_type, self.templates["standard"])
        return template

    def suggest_sections(self, partial_prb: str) -> List[Dict]:
        """Suggest missing sections for a partial PRB.

        Args:
            partial_prb: Partial PRB content

        Returns:
            List of suggested sections with templates
        """
        # Extract existing sections
        existing_sections = self._extract_existing_sections(partial_prb)

        # Required sections
        required = [
            "Incident Summary",
            "Timeline",
            "Root Cause Analysis",
            "Resolution",
            "Action Items",
            "Prevention"
        ]

        # Find missing sections
        missing = [s for s in required if s not in existing_sections]

        # Generate suggestions
        suggestions = []
        for section in missing:
            suggestions.append({
                "section": section,
                "template": self._get_section_template(section),
                "priority": "required" if section in required else "optional",
                "description": self._get_section_description(section)
            })

        return suggestions

    def enhance_prb(self, prb_content: str, enhancement_type: str = "all") -> str:
        """Enhance an existing PRB with additional details.

        Args:
            prb_content: Existing PRB content
            enhancement_type: Type of enhancement (timeline, actions, analysis, all)

        Returns:
            Enhanced PRB content
        """
        enhanced = prb_content

        if enhancement_type in ["timeline", "all"]:
            enhanced = self._enhance_timeline(enhanced)

        if enhancement_type in ["actions", "all"]:
            enhanced = self._enhance_action_items(enhanced)

        if enhancement_type in ["analysis", "all"]:
            enhanced = self._enhance_analysis(enhanced)

        return enhanced

    def _load_templates(self) -> Dict[str, str]:
        """Load PRB templates."""
        templates = {}

        # Standard PRB template
        templates["standard"] = """# PRB-{prb_id}: {title}

## Incident Summary
- **PRB ID**: PRB-{prb_id}
- **Date**: {date}
- **Severity**: {severity}
- **Status**: Open
- **Affected Systems**: {systems}
- **Impact**: [Describe customer/business impact]
- **Duration**: [HH:MM]

## Timeline
- HH:MM - [Initial detection/alert]
- HH:MM - [Investigation started]
- HH:MM - [Root cause identified]
- HH:MM - [Fix applied]
- HH:MM - [Incident resolved]

## Root Cause Analysis
[Detailed explanation of what caused the incident]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### Why It Happened
[Explanation of underlying reasons]

## Resolution
[What was done to resolve the incident]

### Immediate Actions
- [Action 1]
- [Action 2]

### Verification
[How resolution was verified]

## Action Items
- [ ] [Action item 1] (Owner: @username, Due: YYYY-MM-DD)
- [ ] [Action item 2] (Owner: @username, Due: YYYY-MM-DD)
- [ ] [Action item 3] (Owner: @username, Due: YYYY-MM-DD)

## Prevention
[How to prevent this from happening again]

### Short-term Measures
- [Measure 1]

### Long-term Improvements
- [Improvement 1]

## Lessons Learned
[Key takeaways from this incident]

### What Went Well
- [Point 1]

### What Could Be Improved
- [Point 1]

## Communication Log
- HH:MM - [Communication to stakeholders]

## Monitoring & Alerts
[Changes to monitoring/alerting]

---
**Created**: {date}
**Last Updated**: {date}
**Owner**: [SRE Team/Individual]
"""

        # Critical incident template
        templates["critical"] = """# PRB-{prb_id}: [CRITICAL] {title}

⚠️ **CRITICAL INCIDENT** ⚠️

## Executive Summary
[Brief 2-3 sentence summary for leadership]

## Incident Summary
- **PRB ID**: PRB-{prb_id}
- **Date**: {date}
- **Severity**: Critical
- **Status**: Open
- **Affected Systems**: {systems}
- **Customer Impact**: [Number of affected users/revenue impact]
- **Business Impact**: [Business impact description]
- **Duration**: [HH:MM]
- **Detection Time**: [Time from occurrence to detection]
- **Resolution Time**: [Time from detection to resolution]

## Timeline
- HH:MM - [Alert triggered]
- HH:MM - [SRE on-call paged]
- HH:MM - [War room established]
- HH:MM - [Investigation started]
- HH:MM - [Root cause identified]
- HH:MM - [Fix implemented]
- HH:MM - [Monitoring confirmed resolution]
- HH:MM - [All-clear given]

## Root Cause Analysis
[Detailed technical explanation]

### Primary Cause
[Main cause]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### Failure Points
- [What failed]
- [What should have caught this]

## Resolution
[Detailed resolution steps]

### Emergency Actions Taken
1. [Action 1]
2. [Action 2]

### Rollback Plan
[If rollback was performed or considered]

## Impact Analysis
### Customer Impact
- **Users Affected**: [Number/percentage]
- **Duration**: [HH:MM]
- **Services Impacted**: [List]

### Business Impact
- **Revenue Impact**: [Amount if applicable]
- **SLA Breach**: [Yes/No, details]
- **Reputational Impact**: [Description]

## Action Items
### Immediate (Within 24 hours)
- [ ] [Critical action] (Owner: @username, Due: YYYY-MM-DD)

### Short-term (Within 1 week)
- [ ] [Important action] (Owner: @username, Due: YYYY-MM-DD)

### Long-term (Within 1 month)
- [ ] [Strategic improvement] (Owner: @username, Due: YYYY-MM-DD)

## Prevention
### Immediate Safeguards
- [Safeguard 1]

### System Improvements
- [Improvement 1]

### Process Changes
- [Change 1]

## Lessons Learned
[Key lessons for organization]

## Communication Log
- HH:MM - [@stakeholder] - [Message]

## Post-Incident Review
- **Scheduled Date**: [YYYY-MM-DD]
- **Attendees**: [List]

---
**Created**: {date}
**Incident Commander**: [Name]
**Technical Lead**: [Name]
"""

        # Postmortem template
        templates["postmortem"] = """# Postmortem: PRB-{prb_id} - {title}

**Date**: {date}

## Overview
[High-level summary]

## What Happened
[Narrative description of the incident]

## Impact
- **Duration**: [HH:MM]
- **Users Affected**: [Number]
- **Services Impacted**: [List]
- **Data Loss**: [Yes/No, extent]

## Root Cause
[Detailed root cause analysis]

## Timeline (all times in [timezone])
| Time | Event | Actions Taken |
|------|-------|---------------|
| HH:MM | [Event] | [Actions] |

## Resolution
[How the incident was resolved]

## What Went Well
- [Point 1]
- [Point 2]

## What Went Wrong
- [Point 1]
- [Point 2]

## Where We Got Lucky
- [Point 1]

## Action Items
| Priority | Action | Owner | Due Date | Status |
|----------|--------|-------|----------|--------|
| P0 | [Action] | @username | YYYY-MM-DD | Open |

## Lessons Learned
1. [Lesson 1]
2. [Lesson 2]

---
**Contributors**: [Names]
**Review Date**: [YYYY-MM-DD]
"""

        return templates

    def _generate_prb_id(self) -> str:
        """Generate a unique PRB ID."""
        now = datetime.now()
        # Format: YYYY-NNN (year + sequential number)
        # In production, this would check existing PRBs
        return f"{now.year}-{now.month:02d}{now.day:02d}"

    def _extract_incident_info(self, description: str) -> Dict:
        """Extract key information from incident description."""
        info = {}

        # Extract potential title
        lines = description.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            # Remove common prefixes
            first_line = re.sub(r'^(incident|alert|error|issue):\s*', '', first_line, flags=re.IGNORECASE)
            info["title"] = first_line[:100]  # Limit length

        # Extract system names (look for common patterns)
        systems = []
        system_patterns = [
            r'\b(api|database|db|cache|redis|kafka|kubernetes|k8s|nginx|load balancer|cdn)\b',
            r'\b([a-z]+-service|[a-z]+-server|[a-z]+-backend)\b',
        ]
        for pattern in system_patterns:
            matches = re.findall(pattern, description.lower())
            systems.extend(matches)
        info["systems"] = list(set(systems))[:5]  # Limit to 5 systems

        # Look for potential causes
        cause_keywords = ["due to", "caused by", "because of", "after", "when"]
        for keyword in cause_keywords:
            if keyword in description.lower():
                # Extract text after keyword
                parts = description.lower().split(keyword)
                if len(parts) > 1:
                    potential_cause = parts[1].split('.')[0].strip()
                    info["potential_cause"] = potential_cause
                    break

        # Suggest common actions based on keywords
        actions = []
        if "high cpu" in description.lower() or "performance" in description.lower():
            actions.append("Review resource utilization metrics")
            actions.append("Analyze application performance logs")

        if "memory" in description.lower():
            actions.append("Investigate memory leaks")
            actions.append("Review memory allocation patterns")

        if "database" in description.lower() or "db" in description.lower():
            actions.append("Review database query performance")
            actions.append("Check database connection pool settings")

        if "network" in description.lower() or "timeout" in description.lower():
            actions.append("Investigate network connectivity")
            actions.append("Review network latency metrics")

        info["suggested_actions"] = actions

        return info

    def _create_prb_template(self, prb_id: str, title: str, description: str,
                            severity: str, affected_systems: List[str],
                            suggested_root_cause: Optional[str] = None,
                            suggested_actions: List[str] = None) -> str:
        """Create a PRB template with provided information."""
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M")

        systems_str = ", ".join(affected_systems) if affected_systems else "[List systems]"

        draft = f"""# PRB-{prb_id}: {title}

## Incident Summary
- **PRB ID**: PRB-{prb_id}
- **Date**: {date}
- **Severity**: {severity}
- **Status**: Draft
- **Affected Systems**: {systems_str}
- **Impact**: [Describe customer/business impact]
- **Duration**: [HH:MM - ongoing or HH:MM duration]

### Incident Description
{description}

## Timeline
- {time} - [Initial detection/alert]
- {time} - [Investigation started]
- [Add more timeline events as they occur]

## Root Cause Analysis
"""

        if suggested_root_cause:
            draft += f"**Preliminary analysis**: {suggested_root_cause}\n\n"
        else:
            draft += "[Under investigation]\n\n"

        draft += """[Provide detailed explanation once root cause is identified]

### Contributing Factors
- [Factor 1]
- [Factor 2]

## Resolution
[Document resolution steps as they are performed]

### Actions Taken
- [Action 1]
- [Action 2]

## Action Items
"""

        if suggested_actions:
            for i, action in enumerate(suggested_actions, 1):
                draft += f"- [ ] {action} (Owner: @username, Due: YYYY-MM-DD)\n"
        else:
            draft += "- [ ] [Action item 1] (Owner: @username, Due: YYYY-MM-DD)\n"
            draft += "- [ ] [Action item 2] (Owner: @username, Due: YYYY-MM-DD)\n"

        draft += """
## Prevention
[How to prevent this from happening again - to be filled after resolution]

### Short-term Measures
- [Measure 1]

### Long-term Improvements
- [Improvement 1]

## Lessons Learned
[To be filled after incident resolution]

---
**Created**: {date} {time}
**Last Updated**: {date} {time}
**Owner**: [Your name/team]
""".format(date=date, time=time)

        return draft

    def _extract_existing_sections(self, prb_content: str) -> List[str]:
        """Extract section names from PRB content."""
        sections = []
        lines = prb_content.split('\n')

        for line in lines:
            # Match ## Section Name
            match = re.match(r'^##\s+(.+)$', line.strip())
            if match:
                sections.append(match.group(1))

        return sections

    def _get_section_template(self, section_name: str) -> str:
        """Get template for a specific section."""
        templates = {
            "Incident Summary": """## Incident Summary
- **PRB ID**: PRB-YYYY-NNN
- **Date**: YYYY-MM-DD
- **Severity**: Critical/High/Medium/Low
- **Status**: Open/In Progress/Resolved
- **Affected Systems**: [List systems]
- **Impact**: [Describe impact]
- **Duration**: [HH:MM]""",

            "Timeline": """## Timeline
- HH:MM - [Event description]
- HH:MM - [Action taken]
- HH:MM - [Result observed]""",

            "Root Cause Analysis": """## Root Cause Analysis
[Detailed explanation of what caused the incident]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### Why It Happened
[Underlying reasons]""",

            "Resolution": """## Resolution
[What was done to resolve the incident]

### Immediate Actions
- [Action 1]
- [Action 2]

### Verification
[How resolution was verified]""",

            "Action Items": """## Action Items
- [ ] [Action item 1] (Owner: @username, Due: YYYY-MM-DD)
- [ ] [Action item 2] (Owner: @username, Due: YYYY-MM-DD)""",

            "Prevention": """## Prevention
[How to prevent this from happening again]

### Short-term Measures
- [Measure 1]

### Long-term Improvements
- [Improvement 1]""",

            "Lessons Learned": """## Lessons Learned
[Key takeaways from this incident]

### What Went Well
- [Point 1]

### What Could Be Improved
- [Point 1]""",
        }

        return templates.get(section_name, f"## {section_name}\n[Content for {section_name}]")

    def _get_section_description(self, section_name: str) -> str:
        """Get description for a section."""
        descriptions = {
            "Incident Summary": "High-level overview with key metadata and impact summary",
            "Timeline": "Chronological sequence of events, actions, and observations",
            "Root Cause Analysis": "Detailed technical analysis of what caused the incident",
            "Resolution": "Steps taken to resolve the incident and verification methods",
            "Action Items": "Follow-up tasks with owners and due dates",
            "Prevention": "Measures to prevent similar incidents in the future",
            "Lessons Learned": "Key insights and improvements for the team",
        }

        return descriptions.get(section_name, f"Details for {section_name}")

    def _enhance_timeline(self, prb_content: str) -> str:
        """Enhance timeline section with suggested entries."""
        # This is a placeholder - in production would use AI/templates
        return prb_content

    def _enhance_action_items(self, prb_content: str) -> str:
        """Enhance action items section with suggestions."""
        # This is a placeholder - in production would suggest based on incident type
        return prb_content

    def _enhance_analysis(self, prb_content: str) -> str:
        """Enhance analysis sections with prompts."""
        # This is a placeholder - in production would provide analysis framework
        return prb_content
