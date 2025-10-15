"""Unit tests for VerticleMetadata."""

import json
import pytest
from pathlib import Path
from fast_mcp_local.metadata import VerticleMetadata


@pytest.fixture
def schemas_path(tmp_path):
    """Create a temporary schemas directory with test metadata files."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()

    # Create postgres.json
    postgres_metadata = {
        "type": "postgres",
        "name": "PostgreSQL Verticle",
        "description": "Database client verticle for PostgreSQL",
        "template_file": "templates/postgres-verticle.md",
        "gradle_dependencies": [
            "io.vertx:vertx-core:4.5.0",
            "io.vertx:vertx-pg-client:4.5.0"
        ],
        "config_keys": ["postgres.host", "postgres.port"],
        "use_cases": ["CRUD operations", "Connection pooling"]
    }

    with open(schemas_dir / "postgres.json", 'w') as f:
        json.dump(postgres_metadata, f)

    # Create http.json
    http_metadata = {
        "type": "http",
        "name": "HTTP Server Verticle",
        "description": "REST API server verticle",
        "template_file": "templates/http-verticle.md",
        "gradle_dependencies": [
            "io.vertx:vertx-core:4.5.0",
            "io.vertx:vertx-web:4.5.0"
        ],
        "config_keys": ["http.host", "http.port"],
        "use_cases": ["REST APIs", "Microservices"]
    }

    with open(schemas_dir / "http.json", 'w') as f:
        json.dump(http_metadata, f)

    return schemas_dir


@pytest.fixture
def metadata_loader(schemas_path):
    """Create a VerticleMetadata instance."""
    return VerticleMetadata(schemas_path)


def test_load_postgres_metadata(metadata_loader):
    """Test loading PostgreSQL metadata."""
    metadata = metadata_loader.load_metadata("postgres")
    assert metadata is not None
    assert metadata["type"] == "postgres"
    assert metadata["name"] == "PostgreSQL Verticle"
    assert "vertx-pg-client" in str(metadata["gradle_dependencies"])


def test_load_http_metadata(metadata_loader):
    """Test loading HTTP metadata."""
    metadata = metadata_loader.load_metadata("http")
    assert metadata is not None
    assert metadata["type"] == "http"
    assert metadata["name"] == "HTTP Server Verticle"
    assert "vertx-web" in str(metadata["gradle_dependencies"])


def test_load_nonexistent_metadata(metadata_loader):
    """Test loading non-existent verticle type."""
    metadata = metadata_loader.load_metadata("nonexistent")
    assert metadata is None


def test_metadata_caching(metadata_loader):
    """Test that metadata is cached after first load."""
    # First load
    metadata1 = metadata_loader.load_metadata("postgres")
    assert metadata1 is not None

    # Second load should return cached version
    metadata2 = metadata_loader.load_metadata("postgres")
    assert metadata2 is metadata1  # Same object


def test_list_all_types(metadata_loader):
    """Test listing all available verticle types."""
    types = metadata_loader.list_all_types()
    assert len(types) == 2

    # Check that both types are present
    type_names = [t["type"] for t in types]
    assert "postgres" in type_names
    assert "http" in type_names

    # Check structure
    for t in types:
        assert "type" in t
        assert "name" in t
        assert "description" in t
        assert "gradle_deps" in t


def test_list_all_types_structure(metadata_loader):
    """Test the structure of list_all_types output."""
    types = metadata_loader.list_all_types()

    postgres_type = next(t for t in types if t["type"] == "postgres")
    assert postgres_type["name"] == "PostgreSQL Verticle"
    assert "PostgreSQL" in postgres_type["description"]
    assert len(postgres_type["gradle_deps"]) == 2


def test_clear_cache(metadata_loader):
    """Test clearing the cache."""
    # Load metadata
    metadata1 = metadata_loader.load_metadata("postgres")
    assert metadata1 is not None

    # Clear cache
    metadata_loader.clear_cache()

    # Load again - should be a different object
    metadata2 = metadata_loader.load_metadata("postgres")
    assert metadata2 is not None
    assert metadata2 is not metadata1


def test_empty_schemas_directory(tmp_path):
    """Test with an empty schemas directory."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    metadata_loader = VerticleMetadata(empty_dir)
    types = metadata_loader.list_all_types()
    assert types == []


def test_nonexistent_schemas_directory(tmp_path):
    """Test with a non-existent schemas directory."""
    nonexistent_dir = tmp_path / "nonexistent"

    metadata_loader = VerticleMetadata(nonexistent_dir)
    types = metadata_loader.list_all_types()
    assert types == []


def test_invalid_json_file(tmp_path):
    """Test handling of invalid JSON file."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()

    # Create invalid JSON file
    with open(schemas_dir / "invalid.json", 'w') as f:
        f.write("{ invalid json content")

    metadata_loader = VerticleMetadata(schemas_dir)

    # Should handle gracefully
    metadata = metadata_loader.load_metadata("invalid")
    assert metadata is None

    # list_all_types should skip invalid file
    types = metadata_loader.list_all_types()
    assert types == []
