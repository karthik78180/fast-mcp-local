"""Unit tests for the document loader module."""

import pytest
import tempfile
import os
from pathlib import Path
from fast_mcp_local.loader import DocumentLoader, initialize_documents


@pytest.fixture
def temp_docs_dir():
    """Create a temporary docs directory with test files in nested folders."""
    temp_dir = tempfile.mkdtemp()
    docs_path = Path(temp_dir) / "docs"
    docs_path.mkdir()

    # Create test markdown files in root
    (docs_path / "test1.md").write_text("# Test 1\n\nThis is test document one.")
    (docs_path / "test2.md").write_text("# Test 2\n\nThis is test document two.")

    # Create nested folders with markdown files
    tutorials_path = docs_path / "tutorials"
    tutorials_path.mkdir()
    (tutorials_path / "intro.md").write_text("# Tutorial Intro\n\nGetting started.")

    api_path = docs_path / "api" / "reference"
    api_path.mkdir(parents=True)
    (api_path / "guide.md").write_text("# API Guide\n\nAPI documentation.")

    yield docs_path

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    os.unlink(path)  # Remove the file, we just want the path

    yield path

    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


def test_count_tokens():
    """Test token counting."""
    loader = DocumentLoader()
    text = "Hello, world! This is a test."
    tokens = loader.count_tokens(text)
    assert tokens > 0
    assert isinstance(tokens, int)


def test_count_tokens_empty_string():
    """Test token counting with empty string."""
    loader = DocumentLoader()
    tokens = loader.count_tokens("")
    assert tokens == 0


def test_load_file(temp_docs_dir):
    """Test loading a single file."""
    loader = DocumentLoader()
    file_path = temp_docs_dir / "test1.md"

    content, tokens = loader.load_file(file_path)

    assert content == "# Test 1\n\nThis is test document one."
    assert tokens > 0


def test_load_nonexistent_file():
    """Test loading a non-existent file."""
    loader = DocumentLoader()

    with pytest.raises(FileNotFoundError):
        loader.load_file(Path("/nonexistent/file.md"))


def test_load_all_documents(temp_docs_dir, temp_db_path):
    """Test loading all documents from a directory recursively."""
    loader = DocumentLoader(str(temp_docs_dir), temp_db_path)
    stats = loader.load_all_documents()

    assert stats["loaded"] == 4  # 2 root + 1 tutorials + 1 api/reference
    assert stats["updated"] == 0
    assert stats["skipped"] == 0
    assert stats["errors"] == 0
    assert stats["total_tokens"] > 0
    assert len(stats["files"]) == 4

    # Verify nested paths are stored correctly
    filenames = [f["filename"] for f in stats["files"]]
    assert "test1.md" in filenames
    assert "test2.md" in filenames
    assert "tutorials/intro.md" in filenames
    assert "api/reference/guide.md" in filenames


def test_load_all_documents_skip_existing(temp_docs_dir, temp_db_path):
    """Test that existing documents are skipped by default."""
    loader = DocumentLoader(str(temp_docs_dir), temp_db_path)

    # First load
    stats1 = loader.load_all_documents()
    assert stats1["loaded"] == 4

    # Second load should skip all
    stats2 = loader.load_all_documents()
    assert stats2["loaded"] == 0
    assert stats2["skipped"] == 4


def test_load_all_documents_force_reload(temp_docs_dir, temp_db_path):
    """Test force reloading documents."""
    loader = DocumentLoader(str(temp_docs_dir), temp_db_path)

    # First load
    stats1 = loader.load_all_documents()
    assert stats1["loaded"] == 4

    # Force reload
    stats2 = loader.load_all_documents(force_reload=True)
    assert stats2["updated"] == 4
    assert stats2["loaded"] == 0


def test_load_all_documents_empty_directory(temp_db_path):
    """Test loading from an empty directory."""
    temp_dir = tempfile.mkdtemp()
    docs_path = Path(temp_dir) / "docs"
    docs_path.mkdir()

    try:
        loader = DocumentLoader(str(docs_path), temp_db_path)
        stats = loader.load_all_documents()

        assert stats["loaded"] == 0
        assert stats["total_tokens"] == 0
        assert len(stats["files"]) == 0

    finally:
        import shutil
        shutil.rmtree(temp_dir)


def test_load_directory_custom_path(temp_docs_dir, temp_db_path):
    """Test loading from a custom directory."""
    # Create loader with default path
    loader = DocumentLoader("docs", temp_db_path)

    # Load from custom path
    stats = loader.load_directory(str(temp_docs_dir))

    assert stats["loaded"] == 4
    assert loader.docs_path == Path("docs")  # Should restore original path


def test_initialize_documents(temp_docs_dir, temp_db_path):
    """Test the convenience function."""
    stats = initialize_documents(str(temp_docs_dir), temp_db_path)

    assert stats["loaded"] == 4
    assert stats["total_tokens"] > 0


def test_load_invalid_utf8_file(temp_docs_dir):
    """Test loading a file with invalid UTF-8."""
    # Create a file with invalid UTF-8
    invalid_file = temp_docs_dir / "invalid.md"
    with open(invalid_file, 'wb') as f:
        f.write(b'\x80\x81\x82')

    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    os.unlink(db_path)

    try:
        loader = DocumentLoader(str(temp_docs_dir), db_path)
        stats = loader.load_all_documents()

        # Should have 4 successful and 1 error (4 valid files + 1 invalid)
        assert stats["loaded"] == 4
        assert stats["errors"] == 1

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_different_encodings():
    """Test that different encodings are supported."""
    loader = DocumentLoader()

    # Test with cl100k_base (GPT-4)
    text = "Hello, world!"
    tokens_cl100k = loader.count_tokens(text)

    # Test with different encoding
    loader2 = DocumentLoader(encoding_name="p50k_base")  # GPT-3
    tokens_p50k = loader2.count_tokens(text)

    # Both should work (counts may differ)
    assert tokens_cl100k > 0
    assert tokens_p50k > 0
