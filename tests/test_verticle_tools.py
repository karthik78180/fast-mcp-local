"""Unit tests for verticle generation tools."""

import json
import pytest
from pathlib import Path
from fast_mcp_local.server import generate_verticle, list_verticle_types
from fast_mcp_local.metadata import VerticleMetadata
from fast_mcp_local.template_extractor import TemplateExtractor


def test_list_verticle_types_structure():
    """Test that list_verticle_types returns proper structure."""
    result = list_verticle_types()
    data = json.loads(result)

    # Should be a list
    assert isinstance(data, list)

    # Check structure of each entry
    if len(data) > 0:
        for verticle_type in data:
            assert "type" in verticle_type
            assert "name" in verticle_type
            assert "description" in verticle_type
            assert "gradle_deps" in verticle_type
            assert isinstance(verticle_type["gradle_deps"], list)


def test_generate_verticle_postgres():
    """Test generating PostgreSQL verticle."""
    result = generate_verticle("postgres")
    data = json.loads(result)

    # Check no error
    assert "error" not in data

    # Check structure
    assert data["type"] == "postgres"
    assert data["name"] == "PostgreSQL Verticle"
    assert "description" in data
    assert "verticle_code" in data
    assert "gradle_dependencies" in data
    assert "config_example" in data
    assert "deployment_example" in data

    # Check content
    assert "PostgresVerticle" in data["verticle_code"]
    assert "AbstractVerticle" in data["verticle_code"]
    assert len(data["gradle_dependencies"]) > 0
    assert "vertx-pg-client" in str(data["gradle_dependencies"])


def test_generate_verticle_http():
    """Test generating HTTP verticle."""
    result = generate_verticle("http")
    data = json.loads(result)

    # Check no error
    assert "error" not in data

    # Check structure
    assert data["type"] == "http"
    assert data["name"] == "HTTP Server Verticle"

    # Check content
    assert "HttpVerticle" in data["verticle_code"]
    assert "Router" in data["verticle_code"]
    assert "vertx-web" in str(data["gradle_dependencies"])


def test_generate_verticle_invalid_type():
    """Test generating with invalid verticle type."""
    result = generate_verticle("nonexistent")
    data = json.loads(result)

    # Should return error
    assert "error" in data
    assert "Unknown verticle type" in data["error"]
    assert "available_types" in data


def test_generate_verticle_config_example():
    """Test that config example is properly parsed."""
    result = generate_verticle("postgres")
    data = json.loads(result)

    config = data["config_example"]
    assert isinstance(config, dict)
    assert "postgres" in config


def test_generate_verticle_deployment_example():
    """Test that deployment example is extracted."""
    result = generate_verticle("postgres")
    data = json.loads(result)

    deployment = data["deployment_example"]
    assert isinstance(deployment, str)
    assert len(deployment) > 0
    assert "DeploymentOptions" in deployment or deployment == ""


def test_tools_are_callable():
    """Test that tools can be imported and called."""
    assert callable(generate_verticle)
    assert callable(list_verticle_types)
