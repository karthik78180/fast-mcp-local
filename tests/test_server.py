"""Unit tests for the FastMCP server."""

import pytest
from fast_mcp_local.server import greet, add


def test_greet():
    """Test the greet function."""
    result = greet("Alice")
    assert result == "Hello, Alice!"
    assert isinstance(result, str)


def test_greet_empty_name():
    """Test greet with empty string."""
    result = greet("")
    assert result == "Hello, !"


def test_add():
    """Test the add function."""
    result = add(2, 3)
    assert result == 5


def test_add_negative():
    """Test add with negative numbers."""
    result = add(-5, 3)
    assert result == -2


def test_add_zero():
    """Test add with zero."""
    result = add(0, 0)
    assert result == 0
