"""Template extraction module for parsing markdown templates."""

import re
from typing import Dict


class TemplateExtractor:
    """Extract code blocks and content from markdown templates."""

    def extract_code_blocks(self, markdown: str) -> Dict[str, str]:
        """Extract all fenced code blocks by language.

        Args:
            markdown: Markdown content with fenced code blocks

        Returns:
            Dictionary mapping language to code content:
            {
                'java': 'class PostgresVerticle...',
                'gradle': 'dependencies {...}',
                'json': '{"postgres": {...}}',
                'deployment': 'DeploymentOptions...'
            }
        """
        blocks = {}

        # Pattern to match fenced code blocks: ```language\ncode\n```
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, markdown, re.DOTALL)

        for lang, code in matches:
            code = code.strip()

            if lang == 'java':
                # Check if this is deployment code (appears after ## Deployment section)
                if '## Deployment Example' in markdown:
                    # Find position of deployment section
                    deployment_pos = markdown.find('## Deployment Example')
                    code_pos = markdown.find(code, deployment_pos)

                    # If this code appears after deployment section, mark as deployment
                    if code_pos > deployment_pos and code_pos != -1:
                        if 'deployment' not in blocks:  # Take first deployment example
                            blocks['deployment'] = code
                        continue

                # Regular Java code (verticle implementation)
                if 'java' not in blocks:  # Take first Java block as main verticle
                    blocks['java'] = code

            elif lang == 'gradle':
                if 'gradle' not in blocks:  # Take first gradle block
                    blocks['gradle'] = code

            elif lang == 'json':
                # Take the first JSON block after "Configuration Example"
                if 'json' not in blocks and '## Configuration Example' in markdown:
                    config_pos = markdown.find('## Configuration Example')
                    code_pos = markdown.find(code)
                    if code_pos > config_pos:
                        blocks['json'] = code

        return blocks

    def extract_description(self, markdown: str) -> str:
        """Extract description from ## Description section.

        Args:
            markdown: Markdown content

        Returns:
            Description text or empty string if not found
        """
        match = re.search(r'## Description\s*\n(.*?)\n\n', markdown, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def extract_section(self, markdown: str, section_title: str) -> str:
        """Extract content from a specific markdown section.

        Args:
            markdown: Markdown content
            section_title: Section heading (e.g., "Use Cases")

        Returns:
            Section content or empty string if not found
        """
        pattern = rf'## {section_title}\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, markdown, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
