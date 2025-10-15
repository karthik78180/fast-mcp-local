"""FastMCP server for PRB (Problem Record) management.

SRE-focused tools for:
1. Drafting PRBs from incident descriptions
2. Analyzing PRB completeness and quality
3. Searching past PRB documentation
4. Validating PRB structure
5. Extracting action items
6. Finding similar incidents

Designed for SRE teams handling incident response and postmortems.
"""

import os
import json
from pathlib import Path
from fastmcp import FastMCP
from .database import DocumentDatabase
from .loader import initialize_documents
from .prb_analyzer import PRBAnalyzer
from .prb_drafter import PRBDrafter

# Initialize FastMCP server
mcp = FastMCP("prb-sre-assistant")

# Global instances
db: DocumentDatabase | None = None
prb_analyzer: PRBAnalyzer | None = None
prb_drafter: PRBDrafter | None = None


def _initialize():
    """Initialize database and PRB tools."""
    global db, prb_analyzer, prb_drafter

    base_path = Path(__file__).parent.parent.parent
    docs_path = base_path / "docs"
    db_path = base_path / "prb_documents.db"

    # Initialize database
    db = DocumentDatabase(str(db_path))
    db.connect()

    # Load PRB documentation
    if docs_path.exists():
        print(f"📚 Loading PRB documentation from {docs_path}...")
        stats = initialize_documents(str(docs_path), str(db_path))
        print(f"✅ Loaded: {stats['loaded']} docs, {stats['total_tokens']} tokens")
    else:
        print(f"⚠️  Docs directory not found: {docs_path}")

    # Initialize PRB tools
    prb_analyzer = PRBAnalyzer()
    prb_drafter = PRBDrafter()
    print(f"✅ PRB tools initialized")


# Initialize on module load (skip during tests)
if not os.environ.get("PYTEST_CURRENT_TEST"):
    _initialize()


# =============================================================================
# MCP TOOLS - PRB Documentation Search
# =============================================================================

def search_prbs(query: str, limit: int = 10) -> str:
    """Search past PRB documentation and examples.

    Args:
        query: Search query (e.g., "database timeout", "memory leak")
        limit: Maximum results to return (default: 10)

    Returns:
        JSON array of matching PRB documents with snippets

    Example:
        search_prbs("database connection pool exhausted", limit=5)
    """
    if not db:
        return json.dumps([])

    results = db.search_documents(query, limit)
    return json.dumps(results, indent=2)


def get_prb(filename: str) -> str:
    """Get full content of a specific PRB document.

    Args:
        filename: PRB filename (e.g., 'prb-2024-001-database-outage.md')

    Returns:
        JSON with PRB content and metadata

    Example:
        get_prb("prb-2024-001-database-outage.md")
    """
    if not db:
        return json.dumps({"error": "Database not initialized"})

    doc = db.get_document_by_filename(filename)

    if not doc:
        all_docs = db.get_all_documents()
        available = [d["filename"] for d in all_docs]
        return json.dumps({
            "error": f"PRB '{filename}' not found",
            "available_prbs": available[:10]  # Show first 10
        }, indent=2)

    return json.dumps(doc, indent=2)


def list_prbs() -> str:
    """List all available PRB documentation.

    Returns:
        JSON array of all PRBs with metadata

    Example:
        list_prbs()
    """
    if not db:
        return json.dumps([])

    documents = db.get_all_documents()
    return json.dumps(documents, indent=2)


# =============================================================================
# MCP TOOLS - PRB Drafting
# =============================================================================

def draft_prb(incident_description: str,
              severity: str = "High",
              affected_systems: str = "") -> str:
    """Generate a PRB draft from incident description.

    Args:
        incident_description: Description of the incident
        severity: Severity level (Critical/High/Medium/Low)
        affected_systems: Comma-separated list of affected systems

    Returns:
        PRB draft in markdown format

    Example:
        draft_prb(
            incident_description="API gateway returned 503 errors...",
            severity="Critical",
            affected_systems="api-gateway, backend-service"
        )
    """
    if not prb_drafter:
        return json.dumps({"error": "PRB drafter not initialized"})

    # Parse affected systems
    systems = [s.strip() for s in affected_systems.split(",")] if affected_systems else None

    # Generate draft
    draft = prb_drafter.draft_prb(
        incident_description=incident_description,
        severity=severity,
        affected_systems=systems
    )

    return json.dumps({
        "prb_draft": draft,
        "instructions": "Copy this draft and fill in the placeholders as the incident progresses"
    }, indent=2)


def create_prb_template(template_type: str = "standard") -> str:
    """Create a blank PRB from template.

    Args:
        template_type: Template type (standard/critical/postmortem)

    Returns:
        PRB template in markdown format

    Example:
        create_prb_template("critical")
    """
    if not prb_drafter:
        return json.dumps({"error": "PRB drafter not initialized"})

    template = prb_drafter.create_prb_from_template(template_type)

    return json.dumps({
        "template_type": template_type,
        "template": template,
        "instructions": f"Use this {template_type} PRB template as a starting point"
    }, indent=2)


def suggest_prb_sections(partial_prb: str) -> str:
    """Suggest missing sections for a partial PRB.

    Args:
        partial_prb: Partial PRB content

    Returns:
        JSON array of suggested sections with templates

    Example:
        suggest_prb_sections("# PRB-2024-001\\n\\n## Timeline\\n...")
    """
    if not prb_drafter:
        return json.dumps({"error": "PRB drafter not initialized"})

    suggestions = prb_drafter.suggest_sections(partial_prb)

    return json.dumps({
        "missing_sections": len(suggestions),
        "suggestions": suggestions
    }, indent=2)


# =============================================================================
# MCP TOOLS - PRB Analysis
# =============================================================================

def analyze_prb(prb_content: str) -> str:
    """Analyze PRB completeness and provide suggestions.

    Args:
        prb_content: PRB content in markdown format

    Returns:
        JSON with analysis, score, and improvement suggestions

    Example:
        analyze_prb(prb_content)
    """
    if not prb_analyzer:
        return json.dumps({"error": "PRB analyzer not initialized"})

    analysis = prb_analyzer.analyze_completeness(prb_content)

    return json.dumps(analysis, indent=2)


def validate_prb(prb_content: str) -> str:
    """Validate PRB structure and completeness.

    Args:
        prb_content: PRB content in markdown format

    Returns:
        JSON with validation results and missing sections

    Example:
        validate_prb(prb_content)
    """
    if not prb_analyzer:
        return json.dumps({"error": "PRB analyzer not initialized"})

    validation = prb_analyzer.validate_prb(prb_content)

    return json.dumps(validation, indent=2)


def extract_action_items(prb_content: str) -> str:
    """Extract all action items from a PRB.

    Args:
        prb_content: PRB content in markdown format

    Returns:
        JSON array of action items with owners and due dates

    Example:
        extract_action_items(prb_content)
    """
    if not prb_analyzer:
        return json.dumps({"error": "PRB analyzer not initialized"})

    action_items = prb_analyzer.extract_action_items(prb_content)

    return json.dumps({
        "total_action_items": len(action_items),
        "action_items": action_items,
        "summary": {
            "pending": len([a for a in action_items if a["status"] == "pending"]),
            "completed": len([a for a in action_items if a["status"] == "completed"]),
            "with_owner": len([a for a in action_items if a["owner"]]),
            "with_due_date": len([a for a in action_items if a["due_date"]])
        }
    }, indent=2)


def parse_prb(prb_content: str) -> str:
    """Parse PRB and extract all structured data.

    Args:
        prb_content: PRB content in markdown format

    Returns:
        JSON with parsed PRB data (metadata, sections, timeline, action items)

    Example:
        parse_prb(prb_content)
    """
    if not prb_analyzer:
        return json.dumps({"error": "PRB analyzer not initialized"})

    parsed = prb_analyzer.parse_prb(prb_content)

    return json.dumps(parsed, indent=2)


# =============================================================================
# Register MCP Tools
# =============================================================================

# Documentation search tools
mcp.tool()(search_prbs)
mcp.tool()(get_prb)
mcp.tool()(list_prbs)

# PRB drafting tools
mcp.tool()(draft_prb)
mcp.tool()(create_prb_template)
mcp.tool()(suggest_prb_sections)

# PRB analysis tools
mcp.tool()(analyze_prb)
mcp.tool()(validate_prb)
mcp.tool()(extract_action_items)
mcp.tool()(parse_prb)


if __name__ == "__main__":
    mcp.run()
