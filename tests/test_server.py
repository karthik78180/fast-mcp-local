"""Unit tests for the FastMCP server."""

import pytest
from fast_mcp_local.server import (
    search_documents,
    get_all_documents,
    get_document,
    generate_verticle,
    list_verticle_types
)


def test_server_imports():
    """Test that server module and tools can be imported."""
    assert callable(search_documents)
    assert callable(get_all_documents)
    assert callable(get_document)
    assert callable(generate_verticle)
    assert callable(list_verticle_types)
