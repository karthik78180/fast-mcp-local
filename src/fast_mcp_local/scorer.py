"""Code scoring module for analyzing codebase compliance.

Analyzes code against predefined patterns and scoring rules.
Generates compliance scores and detailed reports.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from .pattern_matcher import PatternMatcher, PatternMatch


def get_patterns_dir() -> Path:
    """Get the patterns directory path."""
    current_dir = Path(__file__).parent
    patterns_dir = current_dir.parent.parent / "docs" / "patterns"
    return patterns_dir


def load_pattern_rules(pattern_id: str) -> Optional[Dict]:
    """Load pattern rules from JSON file.

    Args:
        pattern_id: Pattern identifier (e.g., 'vertx-best-practices')

    Returns:
        Dictionary with pattern rules or None if not found
    """
    patterns_dir = get_patterns_dir()

    # Try pattern-specific directory first
    pattern_file = patterns_dir / pattern_id / "scoring-rules.json"
    if not pattern_file.exists():
        # Try schemas directory
        pattern_file = patterns_dir / "schemas" / f"{pattern_id}.json"

    if not pattern_file.exists():
        return None

    try:
        with open(pattern_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def list_patterns() -> str:
    """List all available scoring patterns.

    Returns:
        JSON string with array of available patterns
    """
    patterns_dir = get_patterns_dir()

    if not patterns_dir.exists():
        return json.dumps([])

    patterns = []
    # Scan for pattern directories
    for pattern_dir in patterns_dir.iterdir():
        if pattern_dir.is_dir() and pattern_dir.name != "schemas":
            # Try to load metadata
            rules_file = pattern_dir / "scoring-rules.json"
            if rules_file.exists():
                try:
                    with open(rules_file, 'r', encoding='utf-8') as f:
                        rules = json.load(f)
                        patterns.append({
                            "pattern_id": rules.get("pattern_id", pattern_dir.name),
                            "name": rules.get("name", pattern_dir.name),
                            "description": rules.get("description", ""),
                            "categories": list(rules.get("categories", {}).keys()),
                            "total_rules": sum(len(cat.get("rules", []))
                                             for cat in rules.get("categories", {}).values())
                        })
                except (json.JSONDecodeError, IOError):
                    continue

    return json.dumps(patterns, indent=2)


def get_pattern_metadata(pattern_id: str) -> str:
    """Get pattern metadata and scoring criteria.

    Args:
        pattern_id: Pattern identifier

    Returns:
        JSON string with pattern metadata or error
    """
    rules = load_pattern_rules(pattern_id)

    if rules is None:
        return json.dumps({
            "error": f"Pattern '{pattern_id}' not found",
            "available_patterns": json.loads(list_patterns())
        })

    # Calculate totals
    categories = rules.get("categories", {})
    total_possible_score = 0

    for category_name, category_data in categories.items():
        for rule in category_data.get("rules", []):
            score = rule.get("score", 0)
            if score > 0:  # Only count positive scores
                total_possible_score += score

    metadata = {
        "pattern_id": rules.get("pattern_id"),
        "name": rules.get("name"),
        "description": rules.get("description"),
        "version": rules.get("version"),
        "categories": {name: {
            "weight": cat.get("weight"),
            "rule_count": len(cat.get("rules", []))
        } for name, cat in categories.items()},
        "total_possible_score": total_possible_score,
        "passing_threshold": rules.get("passing_threshold", 70)
    }

    return json.dumps(metadata, indent=2)


def score_codebase(codebase_path: str, pattern_id: str) -> str:
    """Score a codebase against a pattern.

    Args:
        codebase_path: Path to codebase directory or file
        pattern_id: Pattern identifier

    Returns:
        JSON string with scoring results
    """
    rules_data = load_pattern_rules(pattern_id)

    if rules_data is None:
        return json.dumps({
            "error": f"Pattern '{pattern_id}' not found"
        })

    path = Path(codebase_path)
    if not path.exists():
        return json.dumps({
            "error": f"Path '{codebase_path}' does not exist"
        })

    # Initialize matcher
    matcher = PatternMatcher()

    # Collect all rules
    all_rules = []
    categories = rules_data.get("categories", {})

    for category_name, category_data in categories.items():
        for rule in category_data.get("rules", []):
            rule_copy = rule.copy()
            rule_copy["category"] = category_name
            all_rules.append(rule_copy)

    # Scan codebase
    if path.is_file():
        matches = matcher.scan_file(path, all_rules)
        files_scanned = 1
    else:
        matches = matcher.scan_directory(path, all_rules)
        # Count Java files
        files_scanned = len(list(path.rglob('*.java')))

    # Calculate scores
    score_result = calculate_score(matches, all_rules, rules_data)
    score_result["summary"]["files_scanned"] = files_scanned
    score_result["codebase_path"] = str(codebase_path)

    return json.dumps(score_result, indent=2)


def calculate_score(matches: List[PatternMatch], rules: List[Dict],
                   rules_data: Dict) -> Dict:
    """Calculate final score from pattern matches.

    Args:
        matches: List of pattern matches found
        rules: List of all rules
        rules_data: Full rules data structure

    Returns:
        Dictionary with scoring results
    """
    # Initialize scores
    category_scores = {}
    categories = rules_data.get("categories", {})

    for category_name, category_data in categories.items():
        category_scores[category_name] = {
            "score": 0,
            "max": 0,
            "violations": 0,
            "passed": 0
        }

    violations = []

    # Process matches
    for match in matches:
        # Find the rule
        rule = next((r for r in rules if r.get("id") == match.rule_id), None)
        if not rule:
            continue

        category = rule.get("category")
        score_value = rule.get("score", 0)

        # Add violation
        violations.append({
            "rule_id": match.rule_id,
            "rule_name": rule.get("name"),
            "severity": match.severity,
            "category": category,
            "file": match.file_path,
            "line": match.line_number,
            "matched": match.matched_text,
            "message": rule.get("description"),
            "suggestion": rule.get("suggestion", ""),
            "reference_doc": rule.get("reference_doc", "")
        })

        # Update category scores
        if category in category_scores:
            if score_value < 0:  # Penalty
                category_scores[category]["score"] += score_value
                category_scores[category]["violations"] += 1

    # Calculate max scores and positive matches
    for rule in rules:
        category = rule.get("category")
        score_value = rule.get("score", 0)

        if category in category_scores:
            if score_value > 0:
                category_scores[category]["max"] += score_value
                # Check if this positive pattern was found
                found = any(m.rule_id == rule.get("id") for m in matches)
                if found:
                    category_scores[category]["score"] += score_value
                    category_scores[category]["passed"] += 1

    # Calculate overall score
    total_score = sum(cat["score"] for cat in category_scores.values())
    total_max = sum(cat["max"] for cat in category_scores.values())

    # Ensure score doesn't go negative
    total_score = max(0, total_score)

    overall_score = int((total_score / total_max * 100)) if total_max > 0 else 0

    # Assign grade
    if overall_score >= 90:
        grade = "A"
    elif overall_score >= 80:
        grade = "B"
    elif overall_score >= 70:
        grade = "C"
    elif overall_score >= 60:
        grade = "D"
    else:
        grade = "F"

    return {
        "pattern_id": rules_data.get("pattern_id"),
        "overall_score": overall_score,
        "grade": grade,
        "max_score": 100,
        "category_scores": category_scores,
        "summary": {
            "files_scanned": 0,  # Will be filled by caller
            "violations_found": len(violations),
            "best_practices_followed": sum(cat["passed"] for cat in category_scores.values()),
            "critical_issues": len([v for v in violations if v["severity"] == "critical"]),
            "high_issues": len([v for v in violations if v["severity"] == "high"])
        },
        "violations": violations[:20],  # Limit to top 20 for readability
        "recommendations": generate_recommendations(violations, rules_data)
    }


def generate_recommendations(violations: List[Dict], rules_data: Dict) -> List[str]:
    """Generate actionable recommendations from violations.

    Args:
        violations: List of violations found
        rules_data: Full rules data

    Returns:
        List of recommendation strings
    """
    recommendations = []

    # Group by category
    category_violations = {}
    for violation in violations:
        category = violation.get("category", "other")
        if category not in category_violations:
            category_violations[category] = []
        category_violations[category].append(violation)

    # Generate category-specific recommendations
    for category, cat_violations in category_violations.items():
        if len(cat_violations) >= 3:
            recommendations.append(
                f"Address {len(cat_violations)} {category} issues to improve compliance"
            )

    # Add specific critical recommendations
    critical = [v for v in violations if v.get("severity") == "critical"]
    if critical:
        recommendations.insert(0, f"⚠️  Fix {len(critical)} critical issues immediately")

    # Add reference docs
    unique_docs = set(v.get("reference_doc") for v in violations if v.get("reference_doc"))
    if unique_docs:
        recommendations.append(f"Review documentation: {', '.join(list(unique_docs)[:3])}")

    return recommendations[:10]  # Top 10 recommendations


def get_compliance_report(pattern_id: str, codebase_path: str) -> str:
    """Get detailed compliance report in markdown format.

    Args:
        pattern_id: Pattern identifier
        codebase_path: Path to codebase

    Returns:
        Markdown formatted compliance report
    """
    # Get JSON score
    score_json = score_codebase(codebase_path, pattern_id)
    score_data = json.loads(score_json)

    if "error" in score_data:
        return f"# Error\n\n{score_data['error']}"

    # Generate markdown report
    report_lines = []
    report_lines.append(f"# Code Compliance Report\n")
    report_lines.append(f"**Pattern:** {score_data['pattern_id']}")
    report_lines.append(f"**Codebase:** {score_data.get('codebase_path', 'N/A')}")
    report_lines.append(f"**Date:** {Path.ctime(Path(__file__))}\n")

    report_lines.append(f"## Overall Score: {score_data['overall_score']}/100 ({score_data['grade']})\n")

    # Category breakdown
    report_lines.append("## Category Scores\n")
    for category, scores in score_data['category_scores'].items():
        percentage = int(scores['score'] / scores['max'] * 100) if scores['max'] > 0 else 0
        report_lines.append(f"- **{category.title()}**: {percentage}% ({scores['score']}/{scores['max']})")
        report_lines.append(f"  - ✅ Passed: {scores['passed']}")
        report_lines.append(f"  - ❌ Violations: {scores['violations']}\n")

    # Summary
    summary = score_data['summary']
    report_lines.append("## Summary\n")
    report_lines.append(f"- Files Scanned: {summary['files_scanned']}")
    report_lines.append(f"- Violations Found: {summary['violations_found']}")
    report_lines.append(f"- Best Practices Followed: {summary['best_practices_followed']}")
    report_lines.append(f"- Critical Issues: {summary['critical_issues']}")
    report_lines.append(f"- High Priority Issues: {summary['high_issues']}\n")

    # Top violations
    if score_data['violations']:
        report_lines.append("## Top Issues\n")
        for i, violation in enumerate(score_data['violations'][:10], 1):
            severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(violation['severity'], "⚪")
            report_lines.append(f"{i}. {severity_icon} **{violation['rule_name']}**")
            report_lines.append(f"   - File: `{violation['file']}:{violation['line']}`")
            report_lines.append(f"   - Issue: {violation['message']}")
            if violation.get('suggestion'):
                report_lines.append(f"   - Fix: {violation['suggestion']}")
            if violation.get('reference_doc'):
                report_lines.append(f"   - Docs: {violation['reference_doc']}")
            report_lines.append("")

    # Recommendations
    if score_data['recommendations']:
        report_lines.append("## Recommendations\n")
        for rec in score_data['recommendations']:
            report_lines.append(f"- {rec}")

    return '\n'.join(report_lines)
