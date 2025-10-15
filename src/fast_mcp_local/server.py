"""Minimal FastMCP server implementation."""

import os
import json
from pathlib import Path
from fastmcp import FastMCP
from .database import DocumentDatabase
from .loader import initialize_documents
from .template_extractor import TemplateExtractor
from .metadata import VerticleMetadata
from . import migration
from . import scorer

# Initialize FastMCP server
mcp = FastMCP("fast-mcp-local")

# Database instance (initialized on module load)
db: DocumentDatabase | None = None

# Verticle template components (initialized on module load)
metadata_loader: VerticleMetadata | None = None
template_extractor: TemplateExtractor | None = None


def _initialize_database():
    """Initialize database and load documents."""
    global db, metadata_loader, template_extractor

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

    # Initialize verticle template components
    vertx_schemas_path = base_path / "docs" / "vertx" / "schemas"
    if vertx_schemas_path.exists():
        metadata_loader = VerticleMetadata(vertx_schemas_path)
        template_extractor = TemplateExtractor()
        print(f"Initialized verticle template system")


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


def generate_verticle(verticle_type: str) -> str:
    """Generate a verticle from template.

    Args:
        verticle_type: Type of verticle (e.g., 'postgres', 'http', 'redis')

    Returns:
        JSON string with verticle code, gradle dependencies, config, and deployment example
    """
    if not metadata_loader or not template_extractor:
        return json.dumps({"error": "Verticle template system not initialized"})

    # Load metadata
    metadata = metadata_loader.load_metadata(verticle_type)
    if not metadata:
        available_types = metadata_loader.list_all_types()
        return json.dumps({
            "error": f"Unknown verticle type: {verticle_type}",
            "available_types": [t["type"] for t in available_types]
        }, indent=2)

    # Read template file
    base_path = Path(__file__).parent.parent.parent
    template_file = base_path / "docs" / "vertx" / metadata["template_file"]

    if not template_file.exists():
        return json.dumps({"error": f"Template file not found: {template_file}"}, indent=2)

    try:
        template_content = template_file.read_text(encoding='utf-8')
    except IOError as e:
        return json.dumps({"error": f"Failed to read template: {e}"}, indent=2)

    # Extract code blocks
    code_blocks = template_extractor.extract_code_blocks(template_content)

    # Parse JSON config if available
    config_example = {}
    if 'json' in code_blocks:
        try:
            config_example = json.loads(code_blocks['json'])
        except json.JSONDecodeError:
            config_example = {"raw": code_blocks['json']}

    # Build response
    result = {
        "type": metadata["type"],
        "name": metadata["name"],
        "description": metadata["description"],
        "verticle_code": code_blocks.get("java", ""),
        "gradle_dependencies": metadata["gradle_dependencies"],
        "config_example": config_example,
        "deployment_example": code_blocks.get("deployment", ""),
        "use_cases": metadata.get("use_cases", [])
    }

    return json.dumps(result, indent=2)


def list_verticle_types() -> str:
    """List all available verticle types.

    Returns:
        JSON array of verticle types with metadata
    """
    if not metadata_loader:
        return json.dumps({"error": "Verticle template system not initialized"})

    types = metadata_loader.list_all_types()
    return json.dumps(types, indent=2)


def list_migrations() -> str:
    """List all available migration guides.

    Returns:
        JSON array of migration metadata
    """
    return migration.list_migrations()


def get_migration_metadata(migration_id: str) -> str:
    """Get migration metadata (versions, dependencies, steps count).

    Args:
        migration_id: The migration identifier (e.g., 'v1-to-v2')

    Returns:
        JSON string with migration metadata or error
    """
    return migration.get_migration_metadata(migration_id)


def get_migration_guide(migration_id: str) -> str:
    """Get full migration guide with all documentation.

    Args:
        migration_id: The migration identifier (e.g., 'v1-to-v2')

    Returns:
        JSON string with complete migration guide or error
    """
    return migration.get_migration_guide(migration_id)


def get_migration_step(migration_id: str, step_number: int) -> str:
    """Get specific step instructions from migration guide.

    Args:
        migration_id: The migration identifier (e.g., 'v1-to-v2')
        step_number: The step number (1-based)

    Returns:
        JSON string with step content or error
    """
    return migration.get_migration_step(migration_id, step_number)


def list_patterns() -> str:
    """List all available scoring patterns.

    Returns:
        JSON array of available patterns with metadata
    """
    return scorer.list_patterns()


def get_pattern_metadata(pattern_id: str) -> str:
    """Get pattern metadata and scoring criteria.

    Args:
        pattern_id: Pattern identifier (e.g., 'vertx-best-practices')

    Returns:
        JSON string with pattern metadata or error
    """
    return scorer.get_pattern_metadata(pattern_id)


def score_codebase(codebase_path: str, pattern_id: str) -> str:
    """Score a codebase against a pattern.

    Args:
        codebase_path: Path to codebase directory or file
        pattern_id: Pattern identifier (e.g., 'vertx-best-practices')

    Returns:
        JSON string with scoring results including violations and recommendations
    """
    return scorer.score_codebase(codebase_path, pattern_id)


def get_compliance_report(pattern_id: str, codebase_path: str) -> str:
    """Get detailed compliance report in markdown format.

    Args:
        pattern_id: Pattern identifier (e.g., 'vertx-best-practices')
        codebase_path: Path to codebase directory or file

    Returns:
        Markdown formatted compliance report
    """
    return scorer.get_compliance_report(pattern_id, codebase_path)


# Register tools with MCP
mcp.tool()(search_documents)
mcp.tool()(get_all_documents)
mcp.tool()(get_document)
mcp.tool()(generate_verticle)
mcp.tool()(list_verticle_types)
mcp.tool()(list_migrations)
mcp.tool()(get_migration_metadata)
mcp.tool()(get_migration_guide)
mcp.tool()(get_migration_step)
mcp.tool()(list_patterns)
mcp.tool()(get_pattern_metadata)
mcp.tool()(score_codebase)
mcp.tool()(get_compliance_report)


if __name__ == "__main__":
    mcp.run()
