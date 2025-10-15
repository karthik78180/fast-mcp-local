"""PRB (Problem Record) Analyzer for SRE teams.

Analyzes PRB documents for completeness, extracts key information,
and validates structure.
"""

import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class PRBSection:
    """Represents a section in a PRB document."""
    name: str
    content: str
    present: bool
    completeness: int  # 0-100


@dataclass
class ActionItem:
    """Represents an action item from a PRB."""
    description: str
    owner: Optional[str] = None
    due_date: Optional[str] = None
    status: str = "pending"
    line_number: Optional[int] = None


@dataclass
class PRBMetadata:
    """Metadata extracted from a PRB."""
    prb_id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    affected_systems: List[str] = None
    impact: Optional[str] = None
    duration: Optional[str] = None

    def __post_init__(self):
        if self.affected_systems is None:
            self.affected_systems = []


class PRBAnalyzer:
    """Analyzes PRB documents for completeness and quality."""

    # Required sections for a complete PRB
    REQUIRED_SECTIONS = [
        "Incident Summary",
        "Timeline",
        "Root Cause Analysis",
        "Resolution",
        "Action Items",
        "Prevention",
    ]

    # Optional but recommended sections
    OPTIONAL_SECTIONS = [
        "Lessons Learned",
        "Communication Log",
        "Rollback Plan",
        "Monitoring Impact",
    ]

    def __init__(self):
        """Initialize PRB analyzer."""
        pass

    def parse_prb(self, prb_content: str) -> Dict:
        """Parse PRB markdown content and extract structure.

        Args:
            prb_content: PRB content in markdown format

        Returns:
            Dictionary with parsed PRB data
        """
        sections = self._extract_sections(prb_content)
        metadata = self._extract_metadata(prb_content)
        action_items = self._extract_action_items(prb_content)
        timeline = self._extract_timeline(prb_content)

        return {
            "metadata": asdict(metadata),
            "sections": [asdict(s) for s in sections],
            "action_items": [asdict(a) for a in action_items],
            "timeline": timeline,
        }

    def validate_prb(self, prb_content: str) -> Dict:
        """Validate PRB completeness and structure.

        Args:
            prb_content: PRB content in markdown format

        Returns:
            Validation report with score and missing sections
        """
        parsed = self.parse_prb(prb_content)

        # Check required sections
        present_sections = [s["name"] for s in parsed["sections"] if s["present"]]
        missing_required = [s for s in self.REQUIRED_SECTIONS if s not in present_sections]
        missing_optional = [s for s in self.OPTIONAL_SECTIONS if s not in present_sections]

        # Calculate completeness score
        required_score = ((len(self.REQUIRED_SECTIONS) - len(missing_required)) /
                         len(self.REQUIRED_SECTIONS) * 100)

        # Check section content quality
        section_quality = []
        for section in parsed["sections"]:
            if section["present"]:
                quality = self._assess_section_quality(section["name"], section["content"])
                section_quality.append({
                    "section": section["name"],
                    "quality": quality,
                    "completeness": section["completeness"]
                })

        # Calculate overall score
        avg_section_completeness = (sum(s["completeness"] for s in section_quality) /
                                    len(section_quality) if section_quality else 0)
        overall_score = (required_score * 0.7 + avg_section_completeness * 0.3)

        # Generate validation report
        validation = {
            "overall_score": round(overall_score, 2),
            "grade": self._calculate_grade(overall_score),
            "required_sections_present": len(self.REQUIRED_SECTIONS) - len(missing_required),
            "required_sections_total": len(self.REQUIRED_SECTIONS),
            "missing_required_sections": missing_required,
            "missing_optional_sections": missing_optional,
            "section_quality": section_quality,
            "metadata_complete": self._validate_metadata(parsed["metadata"]),
            "action_items_count": len(parsed["action_items"]),
            "timeline_events": len(parsed["timeline"]),
            "recommendations": self._generate_recommendations(
                missing_required, missing_optional, parsed
            )
        }

        return validation

    def extract_action_items(self, prb_content: str) -> List[Dict]:
        """Extract all action items from PRB.

        Args:
            prb_content: PRB content in markdown format

        Returns:
            List of action items with details
        """
        action_items = self._extract_action_items(prb_content)
        return [asdict(item) for item in action_items]

    def analyze_completeness(self, prb_content: str) -> Dict:
        """Analyze PRB completeness and provide suggestions.

        Args:
            prb_content: PRB content in markdown format

        Returns:
            Analysis report with suggestions
        """
        validation = self.validate_prb(prb_content)
        parsed = self.parse_prb(prb_content)

        analysis = {
            "completeness_score": validation["overall_score"],
            "grade": validation["grade"],
            "summary": self._generate_summary(validation, parsed),
            "strengths": self._identify_strengths(validation, parsed),
            "weaknesses": self._identify_weaknesses(validation, parsed),
            "improvement_suggestions": validation["recommendations"],
            "estimated_completion_time": self._estimate_completion_time(validation)
        }

        return analysis

    def _extract_sections(self, content: str) -> List[PRBSection]:
        """Extract all sections from PRB content."""
        sections = []

        # Find all markdown headers
        lines = content.split('\n')
        current_section = None
        current_content = []

        for i, line in enumerate(lines):
            # Check for section headers (## Section Name)
            header_match = re.match(r'^##\s+(.+)$', line.strip())
            if header_match:
                # Save previous section
                if current_section:
                    section_content = '\n'.join(current_content).strip()
                    sections.append(PRBSection(
                        name=current_section,
                        content=section_content,
                        present=bool(section_content),
                        completeness=self._calculate_section_completeness(
                            current_section, section_content
                        )
                    ))

                # Start new section
                current_section = header_match.group(1)
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            section_content = '\n'.join(current_content).strip()
            sections.append(PRBSection(
                name=current_section,
                content=section_content,
                present=bool(section_content),
                completeness=self._calculate_section_completeness(
                    current_section, section_content
                )
            ))

        return sections

    def _extract_metadata(self, content: str) -> PRBMetadata:
        """Extract metadata from PRB content."""
        metadata = PRBMetadata()

        # Extract PRB ID
        prb_id_match = re.search(r'PRB[- ]?(\d{4}[- ]\d{3})', content, re.IGNORECASE)
        if prb_id_match:
            metadata.prb_id = prb_id_match.group(0)

        # Extract title (from H1 or first line)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata.title = title_match.group(1).strip()

        # Extract date
        date_match = re.search(r'\*\*Date\*\*:\s*(.+)', content)
        if date_match:
            metadata.date = date_match.group(1).strip()

        # Extract severity
        severity_match = re.search(r'\*\*Severity\*\*:\s*(\w+)', content)
        if severity_match:
            metadata.severity = severity_match.group(1).strip()

        # Extract status
        status_match = re.search(r'\*\*Status\*\*:\s*(\w+)', content)
        if status_match:
            metadata.status = status_match.group(1).strip()

        # Extract affected systems
        systems_match = re.search(r'\*\*Affected Systems\*\*:\s*(.+)', content)
        if systems_match:
            systems_str = systems_match.group(1).strip()
            metadata.affected_systems = [s.strip() for s in systems_str.split(',')]

        # Extract impact
        impact_match = re.search(r'\*\*Impact\*\*:\s*(.+)', content)
        if impact_match:
            metadata.impact = impact_match.group(1).strip()

        # Extract duration
        duration_match = re.search(r'\*\*Duration\*\*:\s*(.+)', content)
        if duration_match:
            metadata.duration = duration_match.group(1).strip()

        return metadata

    def _extract_action_items(self, content: str) -> List[ActionItem]:
        """Extract action items from PRB content."""
        action_items = []

        # Find action items section
        lines = content.split('\n')
        in_action_section = False

        for i, line in enumerate(lines):
            if re.search(r'^##\s+Action Items', line, re.IGNORECASE):
                in_action_section = True
                continue
            elif in_action_section and re.match(r'^##\s+', line):
                in_action_section = False
                break

            if in_action_section:
                # Match checkbox items: - [ ] or - [x]
                checkbox_match = re.match(r'^[-*]\s+\[([ xX])\]\s+(.+)$', line.strip())
                if checkbox_match:
                    status = "completed" if checkbox_match.group(1).lower() == 'x' else "pending"
                    description = checkbox_match.group(2).strip()

                    # Extract owner (Owner: @name or @name)
                    owner_match = re.search(r'@(\w+)', description)
                    owner = owner_match.group(1) if owner_match else None

                    # Extract due date (Due: YYYY-MM-DD)
                    due_match = re.search(r'Due:\s*(\d{4}-\d{2}-\d{2})', description)
                    due_date = due_match.group(1) if due_match else None

                    action_items.append(ActionItem(
                        description=description,
                        owner=owner,
                        due_date=due_date,
                        status=status,
                        line_number=i + 1
                    ))

        return action_items

    def _extract_timeline(self, content: str) -> List[Dict]:
        """Extract timeline events from PRB content."""
        timeline = []

        # Find timeline section
        lines = content.split('\n')
        in_timeline_section = False

        for line in lines:
            if re.search(r'^##\s+Timeline', line, re.IGNORECASE):
                in_timeline_section = True
                continue
            elif in_timeline_section and re.match(r'^##\s+', line):
                in_timeline_section = False
                break

            if in_timeline_section:
                # Match timeline entries: - HH:MM - Event or HH:MM - Event
                time_match = re.match(r'^[-*]\s*(\d{1,2}:\d{2})\s*[-–—]\s*(.+)$', line.strip())
                if time_match:
                    timeline.append({
                        "time": time_match.group(1),
                        "event": time_match.group(2).strip()
                    })

        return timeline

    def _calculate_section_completeness(self, section_name: str, content: str) -> int:
        """Calculate completeness score for a section (0-100)."""
        if not content:
            return 0

        # Basic length check
        word_count = len(content.split())

        # Minimum word counts for different sections
        min_words = {
            "Incident Summary": 30,
            "Timeline": 20,
            "Root Cause Analysis": 50,
            "Resolution": 40,
            "Action Items": 20,
            "Prevention": 30,
            "Lessons Learned": 30,
        }

        min_required = min_words.get(section_name, 20)

        if word_count >= min_required:
            return 100
        else:
            return min(int((word_count / min_required) * 100), 100)

    def _assess_section_quality(self, section_name: str, content: str) -> str:
        """Assess quality of a section (excellent/good/fair/poor)."""
        completeness = self._calculate_section_completeness(section_name, content)

        if completeness >= 90:
            return "excellent"
        elif completeness >= 70:
            return "good"
        elif completeness >= 50:
            return "fair"
        else:
            return "poor"

    def _validate_metadata(self, metadata: Dict) -> Dict:
        """Validate metadata completeness."""
        required_fields = ["prb_id", "title", "date", "severity", "status"]
        present = {field: bool(metadata.get(field)) for field in required_fields}

        return {
            "complete": all(present.values()),
            "present_fields": [k for k, v in present.items() if v],
            "missing_fields": [k for k, v in present.items() if not v],
            "completeness_percentage": (sum(present.values()) / len(required_fields)) * 100
        }

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _generate_recommendations(self, missing_required: List[str],
                                  missing_optional: List[str],
                                  parsed: Dict) -> List[str]:
        """Generate recommendations for improving PRB."""
        recommendations = []

        # Missing required sections
        if missing_required:
            for section in missing_required:
                recommendations.append(f"Add required section: {section}")

        # Missing metadata
        metadata_validation = self._validate_metadata(parsed["metadata"])
        for field in metadata_validation["missing_fields"]:
            recommendations.append(f"Add missing metadata field: {field}")

        # Action items
        if len(parsed["action_items"]) == 0:
            recommendations.append("Add action items with owners and due dates")
        else:
            incomplete_actions = [a for a in parsed["action_items"]
                                if not a["owner"] or not a["due_date"]]
            if incomplete_actions:
                recommendations.append(
                    f"{len(incomplete_actions)} action items missing owner or due date"
                )

        # Timeline
        if len(parsed["timeline"]) < 3:
            recommendations.append("Add more timeline entries (minimum 3 events)")

        # Section quality
        for section in parsed["sections"]:
            if section["present"] and section["completeness"] < 70:
                recommendations.append(
                    f"Expand {section['name']} section (currently {section['completeness']}% complete)"
                )

        return recommendations

    def _generate_summary(self, validation: Dict, parsed: Dict) -> str:
        """Generate a summary of PRB analysis."""
        score = validation["overall_score"]
        grade = validation["grade"]

        metadata = parsed["metadata"]
        title = metadata.get("title", "Untitled PRB")
        prb_id = metadata.get("prb_id", "Unknown ID")

        summary = f"PRB {prb_id}: {title}\n"
        summary += f"Overall Quality: {score:.1f}% (Grade: {grade})\n"
        summary += f"Required Sections: {validation['required_sections_present']}/{validation['required_sections_total']}\n"
        summary += f"Action Items: {validation['action_items_count']}\n"
        summary += f"Timeline Events: {validation['timeline_events']}"

        return summary

    def _identify_strengths(self, validation: Dict, parsed: Dict) -> List[str]:
        """Identify strengths in the PRB."""
        strengths = []

        # All required sections present
        if validation["required_sections_present"] == validation["required_sections_total"]:
            strengths.append("All required sections present")

        # High quality sections
        high_quality = [s for s in validation["section_quality"]
                       if s["quality"] in ["excellent", "good"]]
        if len(high_quality) >= 4:
            strengths.append(f"{len(high_quality)} sections with good/excellent quality")

        # Complete action items
        complete_actions = [a for a in parsed["action_items"]
                          if a["owner"] and a["due_date"]]
        if complete_actions and len(complete_actions) == len(parsed["action_items"]):
            strengths.append("All action items have owners and due dates")

        # Detailed timeline
        if len(parsed["timeline"]) >= 5:
            strengths.append(f"Detailed timeline with {len(parsed['timeline'])} events")

        # Complete metadata
        if validation["metadata_complete"]["complete"]:
            strengths.append("Complete metadata")

        return strengths if strengths else ["PRB has basic structure"]

    def _identify_weaknesses(self, validation: Dict, parsed: Dict) -> List[str]:
        """Identify weaknesses in the PRB."""
        weaknesses = []

        # Missing required sections
        if validation["missing_required_sections"]:
            weaknesses.append(
                f"Missing {len(validation['missing_required_sections'])} required sections"
            )

        # Low quality sections
        poor_quality = [s for s in validation["section_quality"]
                       if s["quality"] in ["fair", "poor"]]
        if poor_quality:
            weaknesses.append(
                f"{len(poor_quality)} sections need more detail"
            )

        # No action items
        if validation["action_items_count"] == 0:
            weaknesses.append("No action items defined")

        # Sparse timeline
        if validation["timeline_events"] < 3:
            weaknesses.append("Timeline needs more detail")

        # Incomplete metadata
        if not validation["metadata_complete"]["complete"]:
            missing = len(validation["metadata_complete"]["missing_fields"])
            weaknesses.append(f"Incomplete metadata ({missing} fields missing)")

        return weaknesses if weaknesses else ["No major weaknesses identified"]

    def _estimate_completion_time(self, validation: Dict) -> str:
        """Estimate time needed to complete PRB."""
        score = validation["overall_score"]
        missing_sections = len(validation["missing_required_sections"])

        if score >= 90:
            return "5-10 minutes (minor polish)"
        elif score >= 70:
            return "15-30 minutes (add missing details)"
        elif score >= 50:
            return "30-60 minutes (significant work needed)"
        else:
            return "1-2 hours (major rework required)"
