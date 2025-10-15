"""Minimal FastMCP server implementation."""

import os
from pathlib import Path
from fastmcp import FastMCP
from .database import DocumentDatabase
from .loader import initialize_documents

# Initialize FastMCP server
mcp = FastMCP("fast-mcp-local")

# Database instance (initialized on module load)
db: DocumentDatabase | None = None


def _initialize_database():
    """Initialize database and load documents."""
    global db

    # Determine paths relative to this file
    base_path = Path(__file__).parent.parent.parent
    docs_path = base_path / "docs"
    db_path = base_path / "documents.db"

    # Initialize database
    db = DocumentDatabase(str(db_path))
    db.connect()

    # Load documents from docs folder if they exist
    if docs_path.exists():
        print(f"Loading documents from {docs_path}...")
        stats = initialize_documents(str(docs_path), str(db_path))
        print(f"Loaded: {stats['loaded']}, Updated: {stats['updated']}, "
              f"Skipped: {stats['skipped']}, Errors: {stats['errors']}")
        print(f"Total tokens: {stats['total_tokens']}")
    else:
        print(f"Docs directory not found: {docs_path}")


# Initialize database when module is imported (unless in test mode)
if not os.environ.get("PYTEST_CURRENT_TEST"):
    _initialize_database()


def search_documents(query: str, limit: int = 10) -> str:
    """Search documents by content.

    Args:
        query: Search query string to find in documents
        limit: Maximum number of results to return (default: 10)

    Returns:
        JSON string containing matching documents with snippets
    """
    if not db:
        return "Database not initialized"

    results = db.search_documents(query, limit)

    if not results:
        return f"No documents found matching '{query}'"

    import json
    return json.dumps(results, indent=2)


def get_all_documents() -> str:
    """Get a list of all documents in the database.

    Returns:
        JSON string containing all documents with metadata
    """
    if not db:
        return "Database not initialized"

    documents = db.get_all_documents()

    if not documents:
        return "No documents found in database"

    import json
    return json.dumps(documents, indent=2)


def get_document(filename: str) -> str:
    """Get the full content of a specific document by filename.

    Args:
        filename: Name of the document file (e.g., 'mcp-overview.md')

    Returns:
        JSON string containing the document content and metadata
    """
    if not db:
        return "Database not initialized"

    doc = db.get_document_by_filename(filename)

    if not doc:
        return f"Document '{filename}' not found"

    import json
    return json.dumps(doc, indent=2)


# Register tools with MCP
mcp.tool()(search_documents)
mcp.tool()(get_all_documents)
mcp.tool()(get_document)


if __name__ == "__main__":
    mcp.run()
