"""Unit tests for the database module."""

import pytest
import tempfile
import os
from pathlib import Path
from fast_mcp_local.database import DocumentDatabase


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create temp file
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)

    # Create and connect database
    db = DocumentDatabase(path)
    db.connect()

    yield db

    # Cleanup
    db.close()
    if os.path.exists(path):
        os.unlink(path)


def test_database_connect(temp_db):
    """Test database connection."""
    assert temp_db.conn is not None


def test_insert_document(temp_db):
    """Test inserting a document."""
    doc_id = temp_db.insert_document(
        filename="test.md",
        content="# Test Document\n\nThis is a test.",
        tokens=10
    )
    assert doc_id > 0


def test_insert_duplicate_document(temp_db):
    """Test inserting a duplicate document raises error."""
    temp_db.insert_document(
        filename="test.md",
        content="Content 1",
        tokens=5
    )

    with pytest.raises(Exception):  # sqlite3.IntegrityError
        temp_db.insert_document(
            filename="test.md",
            content="Content 2",
            tokens=10
        )


def test_update_document(temp_db):
    """Test updating a document."""
    # Insert initial document
    temp_db.insert_document(
        filename="test.md",
        content="Original content",
        tokens=5
    )

    # Update it
    temp_db.update_document(
        filename="test.md",
        content="Updated content",
        tokens=10
    )

    # Verify update
    doc = temp_db.get_document_by_filename("test.md")
    assert doc is not None
    assert doc["content"] == "Updated content"
    assert doc["tokens"] == 10


def test_search_documents(temp_db):
    """Test searching documents."""
    # Insert test documents
    temp_db.insert_document(
        filename="doc1.md",
        content="Python is a great programming language",
        tokens=10
    )
    temp_db.insert_document(
        filename="doc2.md",
        content="JavaScript is also popular",
        tokens=8
    )

    # Search for Python
    results = temp_db.search_documents("Python")
    assert len(results) == 1
    assert results[0]["filename"] == "doc1.md"

    # Search for programming
    results = temp_db.search_documents("programming")
    assert len(results) == 1


def test_search_documents_case_insensitive(temp_db):
    """Test case-insensitive search."""
    temp_db.insert_document(
        filename="doc1.md",
        content="FastMCP is awesome",
        tokens=5
    )

    results = temp_db.search_documents("fastmcp")
    assert len(results) == 1
    assert results[0]["filename"] == "doc1.md"


def test_search_documents_with_limit(temp_db):
    """Test search with result limit."""
    # Insert 5 documents
    for i in range(5):
        temp_db.insert_document(
            filename=f"doc{i}.md",
            content="test content",
            tokens=5
        )

    results = temp_db.search_documents("test", limit=3)
    assert len(results) == 3


def test_get_all_documents(temp_db):
    """Test retrieving all documents."""
    # Insert test documents
    temp_db.insert_document("doc1.md", "Content 1", 5)
    temp_db.insert_document("doc2.md", "Content 2", 10)

    docs = temp_db.get_all_documents()
    assert len(docs) == 2
    assert all("filename" in doc for doc in docs)
    assert all("tokens" in doc for doc in docs)


def test_get_document_by_filename(temp_db):
    """Test retrieving a specific document."""
    temp_db.insert_document(
        filename="test.md",
        content="Test content",
        tokens=5
    )

    doc = temp_db.get_document_by_filename("test.md")
    assert doc is not None
    assert doc["filename"] == "test.md"
    assert doc["content"] == "Test content"
    assert doc["tokens"] == 5


def test_get_nonexistent_document(temp_db):
    """Test retrieving a non-existent document."""
    doc = temp_db.get_document_by_filename("nonexistent.md")
    assert doc is None


def test_get_total_tokens(temp_db):
    """Test getting total token count."""
    temp_db.insert_document("doc1.md", "Content 1", 10)
    temp_db.insert_document("doc2.md", "Content 2", 20)
    temp_db.insert_document("doc3.md", "Content 3", 15)

    total = temp_db.get_total_tokens()
    assert total == 45


def test_get_total_tokens_empty_db(temp_db):
    """Test total tokens on empty database."""
    total = temp_db.get_total_tokens()
    assert total == 0


def test_context_manager():
    """Test database context manager."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)

    try:
        with DocumentDatabase(path) as db:
            assert db.conn is not None
            db.insert_document("test.md", "Content", 5)

        # Connection should be closed
        # (we can't directly test this without accessing internals)

    finally:
        if os.path.exists(path):
            os.unlink(path)
