"""Document loader module for scraping and loading markdown files."""

import tiktoken
from pathlib import Path
from typing import Optional
from .database import DocumentDatabase


class DocumentLoader:
    """Loader for reading and processing markdown documents."""

    def __init__(
        self,
        docs_path: str = "docs",
        db_path: str = "documents.db",
        encoding_name: str = "cl100k_base"
    ):
        """
        Initialize the document loader.

        Args:
            docs_path: Path to the directory containing markdown files
            db_path: Path to the SQLite database file
            encoding_name: Tiktoken encoding to use (default: cl100k_base for GPT-4)
        """
        self.docs_path = Path(docs_path)
        self.db_path = db_path
        self.encoding = tiktoken.get_encoding(encoding_name)

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def load_file(self, file_path: Path) -> tuple[str, int]:
        """
        Load a single markdown file and count its tokens.

        Args:
            file_path: Path to the markdown file

        Returns:
            Tuple of (content, token_count)

        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file encoding is invalid
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tokens = self.count_tokens(content)
        return content, tokens

    def load_all_documents(self, force_reload: bool = False) -> dict:
        """
        Load all markdown files from the docs directory into the database.

        Recursively searches for .md files in all subdirectories.

        Args:
            force_reload: If True, update existing documents. If False, skip existing ones.

        Returns:
            Dictionary with statistics about the load operation

        Raises:
            FileNotFoundError: If docs directory doesn't exist
        """
        if not self.docs_path.exists():
            raise FileNotFoundError(f"Docs directory not found: {self.docs_path}")

        stats = {
            "loaded": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
            "total_tokens": 0,
            "files": []
        }

        # Find all markdown files recursively
        md_files = list(self.docs_path.glob("**/*.md"))

        if not md_files:
            return stats

        # Connect to database
        with DocumentDatabase(self.db_path) as db:
            for file_path in md_files:
                try:
                    # Store relative path from docs directory
                    relative_path = str(file_path.relative_to(self.docs_path))

                    # Check if document already exists
                    existing = db.get_document_by_filename(relative_path)

                    if existing and not force_reload:
                        stats["skipped"] += 1
                        stats["files"].append({
                            "filename": relative_path,
                            "status": "skipped",
                            "tokens": existing["tokens"]
                        })
                        stats["total_tokens"] += existing["tokens"]
                        continue

                    # Load and process the file
                    content, tokens = self.load_file(file_path)

                    # Insert or update in database
                    if force_reload:
                        db.update_document(relative_path, content, tokens)
                        status = "updated"
                        stats["updated"] += 1
                    else:
                        db.insert_document(relative_path, content, tokens)
                        status = "loaded"
                        stats["loaded"] += 1

                    stats["total_tokens"] += tokens
                    stats["files"].append({
                        "filename": relative_path,
                        "status": status,
                        "tokens": tokens
                    })

                except Exception as e:
                    stats["errors"] += 1
                    # Get relative path safely
                    try:
                        rel_path = str(file_path.relative_to(self.docs_path))
                    except ValueError:
                        rel_path = file_path.name
                    stats["files"].append({
                        "filename": rel_path,
                        "status": "error",
                        "error": str(e)
                    })

        return stats

    def load_directory(
        self,
        custom_path: Optional[str] = None,
        force_reload: bool = False
    ) -> dict:
        """
        Load documents from a custom directory.

        Args:
            custom_path: Custom directory path (uses default if None)
            force_reload: If True, update existing documents

        Returns:
            Dictionary with load statistics
        """
        if custom_path:
            original_path = self.docs_path
            self.docs_path = Path(custom_path)

        try:
            return self.load_all_documents(force_reload)
        finally:
            if custom_path:
                self.docs_path = original_path


def initialize_documents(
    docs_path: str = "docs",
    db_path: str = "documents.db",
    force_reload: bool = False
) -> dict:
    """
    Convenience function to initialize documents from the docs directory.

    Args:
        docs_path: Path to the directory containing markdown files
        db_path: Path to the SQLite database file
        force_reload: If True, update existing documents

    Returns:
        Dictionary with load statistics
    """
    loader = DocumentLoader(docs_path, db_path)
    return loader.load_all_documents(force_reload)
