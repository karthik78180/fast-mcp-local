"""Metadata management module for verticle templates."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class VerticleMetadata:
    """Load and manage verticle metadata from schemas folder."""

    def __init__(self, schemas_path: Path):
        """Initialize metadata loader.

        Args:
            schemas_path: Path to schemas directory containing JSON metadata files
        """
        self.schemas_path = schemas_path
        self._cache: Dict[str, dict] = {}

    def load_metadata(self, verticle_type: str) -> Optional[dict]:
        """Load metadata for a specific verticle type.

        Args:
            verticle_type: Type of verticle (e.g., 'postgres', 'http')

        Returns:
            Metadata dictionary or None if not found
        """
        # Check cache first
        if verticle_type in self._cache:
            return self._cache[verticle_type]

        # Load from file
        schema_file = self.schemas_path / f"{verticle_type}.json"
        if not schema_file.exists():
            return None

        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                self._cache[verticle_type] = metadata
                return metadata
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading metadata for {verticle_type}: {e}")
            return None

    def list_all_types(self) -> List[dict]:
        """List all available verticle types.

        Returns:
            List of dictionaries containing type information:
            [
                {
                    "type": "postgres",
                    "name": "PostgreSQL Verticle",
                    "description": "Database client...",
                    "gradle_deps": ["io.vertx:vertx-pg-client:4.5.0"]
                }
            ]
        """
        types = []

        # Ensure schemas directory exists
        if not self.schemas_path.exists():
            return types

        # Scan all JSON files in schemas directory
        for schema_file in sorted(self.schemas_path.glob("*.json")):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    types.append({
                        "type": metadata.get("type", ""),
                        "name": metadata.get("name", ""),
                        "description": metadata.get("description", ""),
                        "gradle_deps": metadata.get("gradle_dependencies", [])
                    })
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading schema file {schema_file}: {e}")
                continue

        return types

    def clear_cache(self):
        """Clear the metadata cache."""
        self._cache.clear()
