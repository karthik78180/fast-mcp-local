"""Minimal CLI for hackathon demo.

Simple command-line interface for document search and code generation.
"""

import sys
import click
from .server import (
    search_documents,
    get_document,
    list_documents,
    generate_verticle,
    list_verticle_types
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

    4. Get specific doc:
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
