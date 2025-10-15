"""Command-line interface wrapper for MCP tools.

This CLI allows you to use MCP tools from the command line,
making them accessible to GitHub Copilot and other integrations.
"""

import sys
import click
from .server import (
    search_documents,
    get_all_documents,
    get_document,
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
    """Fast MCP Local - CLI wrapper for MCP tools.

    This CLI provides access to document search and Vert.x code generation tools.
    """
    pass


@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
def search(query, limit):
    """Search documents by content.

    Example:
        mcp search "postgres verticle"
        mcp search "deployment" --limit 5
    """
    result = search_documents(query, limit)
    click.echo(result)


@cli.command()
def list_docs():
    """List all indexed documents.

    Example:
        mcp list-docs
    """
    result = get_all_documents()
    click.echo(result)


@cli.command()
@click.argument('filename')
def get(filename):
    """Get full content of a specific document.

    Example:
        mcp get "vertx/templates/postgres-verticle.md"
        mcp get "mcp-overview.md"
    """
    result = get_document(filename)
    click.echo(result)


@cli.command()
@click.argument('verticle_type')
def generate(verticle_type):
    """Generate Vert.x verticle code from template.

    Available types: postgres, http

    Example:
        mcp generate postgres
        mcp generate http
    """
    result = generate_verticle(verticle_type)
    click.echo(result)


@cli.command()
def list_verticles():
    """List all available verticle templates.

    Example:
        mcp list-verticles
    """
    result = list_verticle_types()
    click.echo(result)


@cli.command()
@click.argument('query')
def ask(query):
    """Quick search for documentation (alias for search).

    Example:
        mcp ask "how to deploy verticles"
        mcp ask "postgres configuration"
    """
    result = search_documents(query, limit=5)
    click.echo(result)


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
    """Get migration metadata (versions, dependencies, steps count).

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

    Example:
        mcp migration-step v1-to-v2 1
        mcp migration-step v1-to-v2 3
    """
    result = get_migration_step(migration_id, step_number)
    click.echo(result)


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

    Example:
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

    Example:
        mcp compliance ./src/MyVerticle.java --pattern vertx-best-practices
        mcp compliance ./verticles/ -p vertx-best-practices
    """
    result = get_compliance_report(pattern, codebase_path)
    click.echo(result)


def main():
    """Entry point for CLI."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
