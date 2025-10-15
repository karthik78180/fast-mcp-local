"""CLI for Fast MCP Local.

Command-line interface for document search, code generation, migrations, and scoring.
"""

import sys
import click
from .server import (
    search_documents,
    get_document,
    list_documents,
    generate_verticle,
    list_verticle_types,
    list_migrations,
    get_migration_metadata,
    get_migration_guide,
    get_migration_step,
    list_patterns,
    get_pattern_metadata,
    score_codebase,
    get_compliance_report
)


@click.group()
@click.version_option()
def cli():
    """Fast MCP Local - Vert.x Development Assistant

    Search documentation and generate verticle code.
    """
    pass


# =============================================================================
# Document Commands
# =============================================================================

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Maximum results')
def search(query, limit):
    """Search company documentation.

    Examples:
        mcp search "async handler"
        mcp search "postgres" --limit 5
    """
    result = search_documents(query, limit)
    click.echo(result)


@cli.command()
def list_docs():
    """List all indexed documents.

    Example:
        mcp list-docs
    """
    result = list_documents()
    click.echo(result)


@cli.command()
@click.argument('filename')
def get(filename):
    """Get specific document content.

    Examples:
        mcp get "vertx/templates/platform-async-handler.md"
        mcp get "company/best-practices.md"
    """
    result = get_document(filename)
    click.echo(result)


# =============================================================================
# Code Generation Commands
# =============================================================================

@cli.command()
@click.argument('verticle_type')
def generate(verticle_type):
    """Generate verticle code from template.

    Examples:
        mcp generate platform-async
        mcp generate platform-sync
        mcp generate platform-multipart
    """
    result = generate_verticle(verticle_type)
    click.echo(result)


@cli.command()
def list_types():
    """List all available verticle templates.

    Example:
        mcp list-types
    """
    result = list_verticle_types()
    click.echo(result)


@cli.command(name='list-verticles')
def list_verticles():
    """List all available verticle templates (alias for list-types).

    Example:
        mcp list-verticles
    """
    result = list_verticle_types()
    click.echo(result)


# =============================================================================
# Convenience Aliases
# =============================================================================

@cli.command()
@click.argument('query')
def ask(query):
    """Quick documentation search (alias for search).

    Example:
        mcp ask "how to configure platform"
    """
    result = search_documents(query, limit=5)
    click.echo(result)


# =============================================================================
# Migration Commands
# =============================================================================

@cli.command(name='list-migrations')
def list_migrations_cmd():
    """List all available migration guides.

    Example:
        mcp list-migrations
    """
    result = list_migrations()
    click.echo(result)


@cli.command()
@click.argument('migration_id')
def migration_info(migration_id):
    """Get migration metadata (versions, dependencies, steps).

    Example:
        mcp migration-info v1-to-v2
    """
    result = get_migration_metadata(migration_id)
    click.echo(result)


@cli.command()
@click.argument('migration_id')
def migration_guide(migration_id):
    """Get full migration guide with all documentation.

    Example:
        mcp migration-guide v1-to-v2
    """
    result = get_migration_guide(migration_id)
    click.echo(result)


@cli.command()
@click.argument('migration_id')
@click.argument('step_number', type=int)
def migration_step(migration_id, step_number):
    """Get specific step instructions from migration guide.

    Examples:
        mcp migration-step v1-to-v2 1
        mcp migration-step v1-to-v2 3
    """
    result = get_migration_step(migration_id, step_number)
    click.echo(result)


# =============================================================================
# Code Scoring Commands
# =============================================================================

@cli.command(name='list-patterns')
def list_patterns_cmd():
    """List all available code scoring patterns.

    Example:
        mcp list-patterns
    """
    result = list_patterns()
    click.echo(result)


@cli.command()
@click.argument('pattern_id')
def pattern_info(pattern_id):
    """Get pattern metadata and scoring criteria.

    Example:
        mcp pattern-info vertx-best-practices
    """
    result = get_pattern_metadata(pattern_id)
    click.echo(result)


@cli.command()
@click.argument('codebase_path')
@click.option('--pattern', '-p', required=True, help='Pattern ID to score against')
def score(codebase_path, pattern):
    """Score a codebase against a pattern.

    Examples:
        mcp score ./src/MyVerticle.java --pattern vertx-best-practices
        mcp score ./verticles/ -p vertx-best-practices
    """
    result = score_codebase(codebase_path, pattern)
    click.echo(result)


@cli.command()
@click.argument('codebase_path')
@click.option('--pattern', '-p', required=True, help='Pattern ID to score against')
def compliance(codebase_path, pattern):
    """Get detailed compliance report in markdown format.

    Examples:
        mcp compliance ./src/MyVerticle.java --pattern vertx-best-practices
        mcp compliance ./verticles/ -p vertx-best-practices
    """
    result = get_compliance_report(pattern, codebase_path)
    click.echo(result)


# =============================================================================
# Help Command
# =============================================================================

@cli.command()
def help_commands():
    """Show common command examples.

    Common workflows:

    1. Search documentation:
       mcp search "async handler"
       mcp ask "configuration guide"

    2. List available docs:
       mcp list-docs

    3. Generate code:
       mcp list-types              # See all templates
       mcp generate platform-async  # Generate code

    4. Migrations:
       mcp list-migrations         # See all migrations
       mcp migration-guide v1-to-v2  # Get full guide

    5. Code scoring:
       mcp list-patterns           # See all patterns
       mcp score ./MyVerticle.java --pattern vertx-best-practices

    6. Get specific doc:
       mcp get "company/best-practices.md"
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
