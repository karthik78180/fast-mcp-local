"""Pattern matching engine for code analysis.

Supports multiple matching strategies:
- Regex-based pattern matching
- Text-based presence checking
- Future: AST-based matching with javalang
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PatternMatch:
    """Represents a pattern match in code."""

    def __init__(self, rule_id: str, file_path: str, line_number: int,
                 matched_text: str, severity: str):
        self.rule_id = rule_id
        self.file_path = file_path
        self.line_number = line_number
        self.matched_text = matched_text
        self.severity = severity


class PatternMatcher:
    """Pattern matching engine for code analysis."""

    def __init__(self):
        self.matches: List[PatternMatch] = []

    def match_regex(self, content: str, pattern: str, file_path: str,
                    rule_id: str, severity: str = 'medium') -> List[PatternMatch]:
        """Match a regex pattern in code content.

        Args:
            content: Code content to search
            pattern: Regex pattern to match
            file_path: Path to the file being analyzed
            rule_id: Rule identifier
            severity: Severity level (critical, high, medium, low)

        Returns:
            List of PatternMatch objects
        """
        matches = []
        lines = content.split('\n')

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            # Invalid regex pattern
            return matches

        for line_num, line in enumerate(lines, start=1):
            for match in regex.finditer(line):
                matches.append(PatternMatch(
                    rule_id=rule_id,
                    file_path=file_path,
                    line_number=line_num,
                    matched_text=match.group(0),
                    severity=severity
                ))

        return matches

    def match_presence(self, content: str, pattern: str, file_path: str,
                      rule_id: str, severity: str = 'medium') -> bool:
        """Check if a pattern is present in code (simple text search).

        Args:
            content: Code content to search
            pattern: Text pattern to find
            file_path: Path to the file being analyzed
            rule_id: Rule identifier
            severity: Severity level

        Returns:
            True if pattern found, False otherwise
        """
        return pattern in content

    def match_absence(self, content: str, pattern: str) -> bool:
        """Check if a pattern is absent (for required patterns).

        Args:
            content: Code content to search
            pattern: Text pattern that should be present

        Returns:
            True if pattern is missing, False if found
        """
        return pattern not in content

    def count_occurrences(self, content: str, pattern: str) -> int:
        """Count how many times a pattern occurs.

        Args:
            content: Code content to search
            pattern: Regex pattern to count

        Returns:
            Number of matches found
        """
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            return len(regex.findall(content))
        except re.error:
            return 0

    def scan_file(self, file_path: Path, rules: List[Dict]) -> List[PatternMatch]:
        """Scan a single file against multiple rules.

        Args:
            file_path: Path to file to scan
            rules: List of rule dictionaries

        Returns:
            List of pattern matches
        """
        if not file_path.exists() or not file_path.is_file():
            return []

        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, IOError):
            return []

        matches = []
        for rule in rules:
            rule_matches = self.apply_rule(content, str(file_path), rule)
            matches.extend(rule_matches)

        return matches

    def apply_rule(self, content: str, file_path: str, rule: Dict) -> List[PatternMatch]:
        """Apply a single rule to code content.

        Args:
            content: Code content
            file_path: File path being analyzed
            rule: Rule dictionary with pattern_type and pattern

        Returns:
            List of matches
        """
        pattern_type = rule.get('pattern_type', 'regex')
        pattern = rule.get('pattern', '')
        rule_id = rule.get('id', 'unknown')
        severity = rule.get('severity', 'medium')

        if pattern_type == 'regex':
            return self.match_regex(content, pattern, file_path, rule_id, severity)
        elif pattern_type == 'presence':
            # For presence checks, return a match if found
            if self.match_presence(content, pattern, file_path, rule_id, severity):
                return [PatternMatch(rule_id, file_path, 0, pattern, severity)]
        elif pattern_type == 'absence':
            # For absence checks, return a match if pattern is missing
            if self.match_absence(content, pattern):
                return [PatternMatch(rule_id, file_path, 0, f"Missing: {pattern}", severity)]

        return []

    def scan_directory(self, dir_path: Path, rules: List[Dict],
                      extensions: List[str] = None) -> List[PatternMatch]:
        """Scan all files in a directory.

        Args:
            dir_path: Directory to scan
            rules: List of rules to apply
            extensions: File extensions to include (e.g., ['.java'])

        Returns:
            List of all pattern matches
        """
        if extensions is None:
            extensions = ['.java']

        if not dir_path.exists() or not dir_path.is_dir():
            return []

        all_matches = []
        for ext in extensions:
            for file_path in dir_path.rglob(f'*{ext}'):
                matches = self.scan_file(file_path, rules)
                all_matches.extend(matches)

        return all_matches


def extract_line_context(file_path: str, line_number: int,
                        context_lines: int = 2) -> Tuple[str, str, str]:
    """Extract code context around a specific line.

    Args:
        file_path: Path to file
        line_number: Target line number
        context_lines: Number of lines before/after to include

    Returns:
        Tuple of (before_context, target_line, after_context)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if line_number < 1 or line_number > len(lines):
            return ("", "", "")

        idx = line_number - 1
        start = max(0, idx - context_lines)
        end = min(len(lines), idx + context_lines + 1)

        before = ''.join(lines[start:idx])
        target = lines[idx]
        after = ''.join(lines[idx + 1:end])

        return (before, target, after)
    except (IOError, UnicodeDecodeError):
        return ("", "", "")
