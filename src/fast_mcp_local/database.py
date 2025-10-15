"""Database module for storing and querying documents."""

import sqlite3
from pathlib import Path
from typing import Optional


class DocumentDatabase:
    """SQLite database for document storage and retrieval."""

    def __init__(self, db_path: str = "documents.db"):
        """
        Initialize the database connection.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Connect to the database and create tables if needed."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the documents table if it doesn't exist."""
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                tokens INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_document(
        self,
        filename: str,
        content: str,
        tokens: int
    ) -> int:
        """
        Insert a document into the database.

        Args:
            filename: Relative path of the document from docs directory (e.g., 'guide.md' or 'api/overview.md')
            content: Full content of the document
            tokens: Token count calculated with tiktoken

        Returns:
            The ID of the inserted document

        Raises:
            RuntimeError: If database is not connected
            sqlite3.IntegrityError: If document with same path exists
        """
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO documents (filename, content, tokens)
            VALUES (?, ?, ?)
            """,
            (filename, content, tokens)
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_document(
        self,
        filename: str,
        content: str,
        tokens: int
    ) -> None:
        """
        Update an existing document or insert if it doesn't exist.

        Args:
            filename: Relative path of the document from docs directory (e.g., 'guide.md' or 'api/overview.md')
            content: Full content of the document
            tokens: Token count calculated with tiktoken
        """
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO documents (filename, content, tokens)
            VALUES (?, ?, ?)
            ON CONFLICT(filename) DO UPDATE SET
                content = excluded.content,
                tokens = excluded.tokens,
                created_at = CURRENT_TIMESTAMP
            """,
            (filename, content, tokens)
        )
        self.conn.commit()

    def search_documents(
        self,
        query: str,
        limit: int = 10
    ) -> list[dict]:
        """
        Search documents by content.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of matching documents with filename, content snippet, and tokens
        """
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()

        # Simple case-insensitive search
        cursor.execute(
            """
            SELECT id, filename, content, tokens, created_at
            FROM documents
            WHERE content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (f"%{query}%", limit)
        )

        results = []
        for row in cursor.fetchall():
            # Create a snippet around the match
            content = row["content"]
            query_lower = query.lower()
            content_lower = content.lower()

            if query_lower in content_lower:
                pos = content_lower.find(query_lower)
                start = max(0, pos - 100)
                end = min(len(content), pos + len(query) + 100)
                snippet = content[start:end]
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
            else:
                snippet = content[:200] + "..." if len(content) > 200 else content

            results.append({
                "id": row["id"],
                "filename": row["filename"],
                "snippet": snippet,
                "tokens": row["tokens"],
                "created_at": row["created_at"]
            })

        return results

    def get_all_documents(self) -> list[dict]:
        """
        Get all documents from the database.

        Returns:
            List of all documents
        """
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, filename, tokens, created_at
            FROM documents
            ORDER BY created_at DESC
            """
        )

        return [
            {
                "id": row["id"],
                "filename": row["filename"],
                "tokens": row["tokens"],
                "created_at": row["created_at"]
            }
            for row in cursor.fetchall()
        ]

    def get_document_by_filename(self, filename: str) -> Optional[dict]:
        """
        Get a specific document by its relative path.

        Args:
            filename: Relative path of the document from docs directory (e.g., 'guide.md' or 'api/overview.md')

        Returns:
            Document data or None if not found
        """
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, filename, content, tokens, created_at
            FROM documents
            WHERE filename = ?
            """,
            (filename,)
        )

        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "filename": row["filename"],
                "content": row["content"],
                "tokens": row["tokens"],
                "created_at": row["created_at"]
            }
        return None

    def get_total_tokens(self) -> int:
        """
        Get the total number of tokens across all documents.

        Returns:
            Total token count
        """
        if not self.conn:
            raise RuntimeError("Database not connected")

        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(tokens) as total FROM documents")
        result = cursor.fetchone()
        return result["total"] if result["total"] is not None else 0

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
