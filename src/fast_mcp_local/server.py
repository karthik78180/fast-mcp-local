"""FastMCP server with document search, code generation, migrations, and scoring.

Core features:
1. Document search - Search company Vert.x documentation
2. Code generation - Generate verticle code from templates
3. Migrations - OpenRewrite migration guides
4. Code scoring - Analyze code against best practices

Designed for easy customization with company-specific context.
"""

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

# Global instances
db: DocumentDatabase | None = None
metadata_loader: VerticleMetadata | None = None
template_extractor: TemplateExtractor | None = None


def _initialize():
    """Initialize database and template system."""
    global db, metadata_loader, template_extractor

    base_path = Path(__file__).parent.parent.parent
    docs_path = base_path / "docs"
    db_path = base_path / "documents.db"

    # Initialize database
    db = DocumentDatabase(str(db_path))
    db.connect()

    # Load documents
    if docs_path.exists():
        print(f"📚 Loading documents from {docs_path}...")
        stats = initialize_documents(str(docs_path), str(db_path))
        print(f"✅ Loaded: {stats['loaded']} docs, {stats['total_tokens']} tokens")
    else:
        print(f"⚠️  Docs directory not found: {docs_path}")

    # Initialize template system
    vertx_schemas_path = base_path / "docs" / "vertx" / "schemas"
    if vertx_schemas_path.exists():
        metadata_loader = VerticleMetadata(vertx_schemas_path)
        template_extractor = TemplateExtractor()
        types = metadata_loader.list_all_types()
        print(f"✅ Loaded {len(types)} verticle templates")


# Initialize on module load (skip during tests)
if not os.environ.get("PYTEST_CURRENT_TEST"):
    _initialize()


# =============================================================================
# MCP TOOLS - Document Search
# =============================================================================

def search_documents(query: str, limit: int = 10) -> str:
    """Search company Vert.x documentation.

    Args:
        query: Search query (e.g., "async handler", "configuration")
        limit: Maximum results to return (default: 10)

    Returns:
        JSON with matching documents and snippets
    """
    if not db:
        return json.dumps({"error": "Database not initialized"})

    results = db.search_documents(query, limit)

    if not results:
        return json.dumps({
            "message": f"No documents found matching '{query}'",
            "suggestion": "Try broader search terms or check docs/ directory"
        })

    return json.dumps({
        "query": query,
        "count": len(results),
        "results": results
    }, indent=2)


def get_document(filename: str) -> str:
    """Get full content of a specific document.

    Args:
        filename: Document filename (e.g., 'platform-async-handler.md')

    Returns:
        JSON with document content and metadata
    """
    if not db:
        return json.dumps({"error": "Database not initialized"})

    doc = db.get_document_by_filename(filename)

    if not doc:
        all_docs = db.get_all_documents()
        available = [d["filename"] for d in all_docs]
        return json.dumps({
            "error": f"Document '{filename}' not found",
            "available_documents": available[:10]  # Show first 10
        }, indent=2)

    return json.dumps(doc, indent=2)


def list_documents() -> str:
    """List all available documentation.

    Returns:
        JSON array of all documents with metadata
    """
    if not db:
        return json.dumps({"error": "Database not initialized"})

    documents = db.get_all_documents()

    if not documents:
        return json.dumps({
            "message": "No documents found",
            "suggestion": "Add markdown files to docs/ directory"
        })

    # Group by directory for better organization
    grouped = {}
    for doc in documents:
        parts = doc["filename"].split("/")
        category = parts[0] if len(parts) > 1 else "root"
        if category not in grouped:
            grouped[category] = []
        grouped[category].append({
            "filename": doc["filename"],
            "title": doc["title"],
            "tokens": doc["tokens"]
        })

    return json.dumps({
        "total": len(documents),
        "categories": grouped
    }, indent=2)


# =============================================================================
# MCP TOOLS - Verticle Code Generation
# =============================================================================

def generate_verticle(verticle_type: str) -> str:
    """Generate verticle code from template.

    Args:
        verticle_type: Template type (e.g., 'platform-async', 'platform-sync')

    Returns:
        JSON with verticle code, dependencies, and configuration
    """
    if not metadata_loader or not template_extractor:
        return json.dumps({"error": "Template system not initialized"})

    # Load metadata
    metadata = metadata_loader.load_metadata(verticle_type)
    if not metadata:
        available_types = metadata_loader.list_all_types()
        return json.dumps({
            "error": f"Unknown verticle type: {verticle_type}",
            "available_types": [t["type"] for t in available_types],
            "suggestion": "Run list_verticle_types() to see all options"
        }, indent=2)

    # Read template file
    base_path = Path(__file__).parent.parent.parent
    template_file = base_path / "docs" / "vertx" / metadata["template_file"]

    if not template_file.exists():
        return json.dumps({
            "error": f"Template file not found: {template_file}"
        }, indent=2)

    template_content = template_file.read_text(encoding='utf-8')

    # Extract code blocks
    code_blocks = template_extractor.extract_code_blocks(template_content)

    # Parse JSON config
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
        "gradle_dependencies": metadata.get("gradle_dependencies", []),
        "config_example": config_example,
        "use_cases": metadata.get("use_cases", [])
    }

    return json.dumps(result, indent=2)


def list_verticle_types() -> str:
    """List all available verticle templates.

    Returns:
        JSON array of available templates
    """
    if not metadata_loader:
        return json.dumps({"error": "Template system not initialized"})

    types = metadata_loader.list_all_types()

    # Group by category (platform vs standard)
    platform_handlers = []
    standard_verticles = []

    for t in types:
        if t["type"].startswith("platform-"):
            platform_handlers.append(t)
        else:
            standard_verticles.append(t)

    return json.dumps({
        "total": len(types),
        "platform_handlers": platform_handlers,
        "standard_verticles": standard_verticles
    }, indent=2)


# =============================================================================
# MCP TOOLS - Migration Guides
# =============================================================================

def list_migrations() -> str:
    """List all available migration guides.

    Returns:
        JSON array of migration metadata
    """
    return migration.list_migrations()


def get_migration_metadata(migration_id: str) -> str:
    """Get migration metadata (versions, dependencies, steps count).

    Args:
        migration_id: Migration identifier (e.g., 'v1-to-v2')

    Returns:
        JSON with migration metadata
    """
    return migration.get_migration_metadata(migration_id)


def get_migration_guide(migration_id: str) -> str:
    """Get full migration guide with all documentation.

    Args:
        migration_id: Migration identifier (e.g., 'v1-to-v2')

    Returns:
        JSON with complete migration guide
    """
    return migration.get_migration_guide(migration_id)


def get_migration_step(migration_id: str, step_number: int) -> str:
    """Get specific step instructions from migration guide.

    Args:
        migration_id: Migration identifier (e.g., 'v1-to-v2')
        step_number: Step number (1-based)

    Returns:
        JSON with step content
    """
    return migration.get_migration_step(migration_id, step_number)


# =============================================================================
# MCP TOOLS - Code Scoring
# =============================================================================

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
        JSON with pattern metadata
    """
    return scorer.get_pattern_metadata(pattern_id)


def score_codebase(codebase_path: str, pattern_id: str) -> str:
    """Score a codebase against a pattern.

    Args:
        codebase_path: Path to codebase directory or file
        pattern_id: Pattern identifier (e.g., 'vertx-best-practices')

    Returns:
        JSON with scoring results, violations, and recommendations
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


# =============================================================================
# Register MCP Tools
# =============================================================================

# Document search tools
mcp.tool()(search_documents)
mcp.tool()(get_document)
mcp.tool()(list_documents)

# Code generation tools
mcp.tool()(generate_verticle)
mcp.tool()(list_verticle_types)

# Migration tools
mcp.tool()(list_migrations)
mcp.tool()(get_migration_metadata)
mcp.tool()(get_migration_guide)
mcp.tool()(get_migration_step)

# Code scoring tools
mcp.tool()(list_patterns)
mcp.tool()(get_pattern_metadata)
mcp.tool()(score_codebase)
mcp.tool()(get_compliance_report)


if __name__ == "__main__":
    mcp.run()
