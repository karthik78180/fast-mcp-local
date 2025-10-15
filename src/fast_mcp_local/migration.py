"""Migration guide management for OpenRewrite-based migrations."""

import json
from pathlib import Path
from typing import Dict, List, Optional


def get_migrations_dir() -> Path:
    """Get the migrations directory path."""
    current_dir = Path(__file__).parent
    migrations_dir = current_dir.parent.parent / "docs" / "migrations"
    return migrations_dir


def get_schemas_dir() -> Path:
    """Get the migration schemas directory path."""
    return get_migrations_dir() / "schemas"


def load_migration_metadata(migration_id: str) -> Optional[Dict]:
    """Load migration metadata from JSON schema file.

    Args:
        migration_id: The migration identifier (e.g., "v1-to-v2")

    Returns:
        Dictionary with migration metadata or None if not found
    """
    schemas_dir = get_schemas_dir()
    schema_file = schemas_dir / f"{migration_id}.json"

    if not schema_file.exists():
        return None

    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def list_migrations() -> str:
    """List all available migration guides.

    Returns:
        JSON string with array of migration metadata
    """
    schemas_dir = get_schemas_dir()

    if not schemas_dir.exists():
        return json.dumps([])

    migrations = []
    for schema_file in schemas_dir.glob("*.json"):
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                migrations.append(metadata)
        except (json.JSONDecodeError, IOError):
            continue

    # Sort by migration_id
    migrations.sort(key=lambda x: x.get("migration_id", ""))

    return json.dumps(migrations, indent=2)


def get_migration_metadata(migration_id: str) -> str:
    """Get migration metadata (versions, dependencies, steps count).

    Args:
        migration_id: The migration identifier (e.g., "v1-to-v2")

    Returns:
        JSON string with migration metadata or error
    """
    metadata = load_migration_metadata(migration_id)

    if metadata is None:
        available = list_migration_ids()
        return json.dumps({
            "error": f"Migration '{migration_id}' not found",
            "available_migrations": available
        })

    return json.dumps(metadata, indent=2)


def get_migration_guide(migration_id: str) -> str:
    """Get full migration guide with all documentation.

    Args:
        migration_id: The migration identifier (e.g., "v1-to-v2")

    Returns:
        JSON string with complete migration guide or error
    """
    metadata = load_migration_metadata(migration_id)

    if metadata is None:
        available = list_migration_ids()
        return json.dumps({
            "error": f"Migration '{migration_id}' not found",
            "available_migrations": available
        })

    migrations_dir = get_migrations_dir()
    migration_dir = migrations_dir / migration_id

    # Read all markdown files
    guide_content = {}
    guide_content["migration_id"] = migration_id
    guide_content["metadata"] = metadata

    # Read migration-guide.md
    guide_file = migration_dir / "migration-guide.md"
    if guide_file.exists():
        with open(guide_file, 'r', encoding='utf-8') as f:
            guide_content["guide"] = f.read()

    # Read steps.md
    steps_file = migration_dir / "steps.md"
    if steps_file.exists():
        with open(steps_file, 'r', encoding='utf-8') as f:
            guide_content["steps"] = f.read()

    # Read gradle-setup.md if exists
    gradle_file = migration_dir / "gradle-setup.md"
    if gradle_file.exists():
        with open(gradle_file, 'r', encoding='utf-8') as f:
            guide_content["gradle_setup"] = f.read()

    return json.dumps(guide_content, indent=2)


def get_migration_step(migration_id: str, step_number: int) -> str:
    """Get specific step instructions from migration guide.

    Args:
        migration_id: The migration identifier (e.g., "v1-to-v2")
        step_number: The step number (1-based)

    Returns:
        JSON string with step content or error
    """
    metadata = load_migration_metadata(migration_id)

    if metadata is None:
        available = list_migration_ids()
        return json.dumps({
            "error": f"Migration '{migration_id}' not found",
            "available_migrations": available
        })

    total_steps = metadata.get("total_steps", 0)
    if step_number < 1 or step_number > total_steps:
        return json.dumps({
            "error": f"Step {step_number} is out of range",
            "total_steps": total_steps,
            "valid_range": f"1-{total_steps}"
        })

    migrations_dir = get_migrations_dir()
    migration_dir = migrations_dir / migration_id
    steps_file = migration_dir / "steps.md"

    if not steps_file.exists():
        return json.dumps({
            "error": f"Steps file not found for migration '{migration_id}'"
        })

    # Read and parse steps
    with open(steps_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract specific step
    step_content = extract_step_from_markdown(content, step_number)

    if step_content is None:
        return json.dumps({
            "error": f"Step {step_number} not found in steps file",
            "total_steps": total_steps
        })

    return json.dumps({
        "migration_id": migration_id,
        "step_number": step_number,
        "total_steps": total_steps,
        "content": step_content
    }, indent=2)


def extract_step_from_markdown(markdown: str, step_number: int) -> Optional[str]:
    """Extract a specific step section from markdown content.

    Args:
        markdown: The full markdown content
        step_number: The step number to extract (1-based)

    Returns:
        The step content or None if not found
    """
    lines = markdown.split('\n')
    step_prefix = f"## Step {step_number}:"

    start_idx = None
    end_idx = None

    # Find start of this step
    for i, line in enumerate(lines):
        if line.startswith(step_prefix):
            start_idx = i
            break

    if start_idx is None:
        return None

    # Find start of next step or end of file
    for i in range(start_idx + 1, len(lines)):
        if lines[i].startswith("## Step "):
            end_idx = i
            break

    if end_idx is None:
        end_idx = len(lines)

    # Extract step content
    step_lines = lines[start_idx:end_idx]
    return '\n'.join(step_lines).strip()


def list_migration_ids() -> List[str]:
    """Get list of available migration IDs.

    Returns:
        List of migration IDs
    """
    schemas_dir = get_schemas_dir()

    if not schemas_dir.exists():
        return []

    migration_ids = []
    for schema_file in schemas_dir.glob("*.json"):
        migration_id = schema_file.stem
        migration_ids.append(migration_id)

    return sorted(migration_ids)


# Cache for migration metadata
_metadata_cache: Dict[str, Dict] = {}


def clear_cache():
    """Clear the metadata cache."""
    global _metadata_cache
    _metadata_cache.clear()
