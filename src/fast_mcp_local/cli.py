"""CLI for PRB SRE Assistant.

Command-line interface for PRB management, drafting, and analysis.
"""

import sys
import click
from .server import (
    search_prbs,
    get_prb,
    list_prbs,
    draft_prb,
    create_prb_template,
    suggest_prb_sections,
    analyze_prb,
    validate_prb,
    extract_action_items,
    parse_prb
)


@click.group()
@click.version_option()
def cli():
    """PRB SRE Assistant - Problem Record Management Tool

    Tools for SRE teams to manage incident PRBs (Problem Records).
    """
    pass


# =============================================================================
# Search Commands
# =============================================================================

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Maximum results')
def search(query, limit):
    """Search past PRB documentation.

    Examples:
        prb search "database timeout"
        prb search "memory leak" --limit 5
    """
    result = search_prbs(query, limit)
    click.echo(result)


@cli.command()
def list():
    """List all available PRBs.

    Example:
        prb list
    """
    result = list_prbs()
    click.echo(result)


@cli.command()
@click.argument('filename')
def get(filename):
    """Get specific PRB content.

    Examples:
        prb get "prb-2024-001-database-outage.md"
    """
    result = get_prb(filename)
    click.echo(result)


# =============================================================================
# Drafting Commands
# =============================================================================

@cli.command()
@click.argument('description')
@click.option('--severity', '-s', default='High',
              help='Severity (Critical/High/Medium/Low)')
@click.option('--systems', default='',
              help='Affected systems (comma-separated)')
def draft(description, severity, systems):
    """Generate a PRB draft from incident description.

    Examples:
        prb draft "API gateway returned 503 errors"
        prb draft "Database timeout" --severity Critical --systems "api,db"
    """
    result = draft_prb(description, severity, systems)
    click.echo(result)


@cli.command()
@click.option('--type', '-t', default='standard',
              help='Template type (standard/critical/postmortem)')
def template(type):
    """Create a blank PRB template.

    Examples:
        prb template
        prb template --type critical
        prb template --type postmortem
    """
    result = create_prb_template(type)
    click.echo(result)


@cli.command()
@click.argument('prb_file', type=click.Path(exists=True))
def suggest(prb_file):
    """Suggest missing sections for a partial PRB.

    Examples:
        prb suggest my-draft.md
    """
    with open(prb_file, 'r') as f:
        content = f.read()

    result = suggest_prb_sections(content)
    click.echo(result)


# =============================================================================
# Analysis Commands
# =============================================================================

@cli.command()
@click.argument('prb_file', type=click.Path(exists=True))
def analyze(prb_file):
    """Analyze PRB completeness and quality.

    Examples:
        prb analyze prb-2024-001.md
    """
    with open(prb_file, 'r') as f:
        content = f.read()

    result = analyze_prb(content)
    click.echo(result)


@cli.command()
@click.argument('prb_file', type=click.Path(exists=True))
def validate(prb_file):
    """Validate PRB structure and completeness.

    Examples:
        prb validate prb-2024-001.md
    """
    with open(prb_file, 'r') as f:
        content = f.read()

    result = validate_prb(content)
    click.echo(result)


@cli.command()
@click.argument('prb_file', type=click.Path(exists=True))
def actions(prb_file):
    """Extract action items from a PRB.

    Examples:
        prb actions prb-2024-001.md
    """
    with open(prb_file, 'r') as f:
        content = f.read()

    result = extract_action_items(content)
    click.echo(result)


@cli.command()
@click.argument('prb_file', type=click.Path(exists=True))
def parse(prb_file):
    """Parse PRB and extract structured data.

    Examples:
        prb parse prb-2024-001.md
    """
    with open(prb_file, 'r') as f:
        content = f.read()

    result = parse_prb(content)
    click.echo(result)


# =============================================================================
# Help Command
# =============================================================================

@cli.command()
def help_commands():
    """Show common command examples.

    Common workflows:

    1. Search past PRBs:
       prb search "database timeout"
       prb list

    2. Draft a new PRB:
       prb draft "API returned 503 errors" --severity Critical
       prb template --type critical

    3. Analyze existing PRB:
       prb analyze my-prb.md
       prb validate my-prb.md
       prb actions my-prb.md

    4. Get specific PRB:
       prb get "prb-2024-001.md"
    """
    click.echo(__doc__)


def main():
    """Entry point for CLI."""
    try:
        cli()
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
