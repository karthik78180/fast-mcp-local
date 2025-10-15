# Building MCP Tools

## Introduction

Tools are the core functionality of MCP servers. They allow LLMs to perform actions, retrieve data, and interact with external systems. This guide covers best practices for building effective MCP tools.

## Tool Design Principles

### 1. Single Responsibility

Each tool should do one thing well. Don't create monolithic tools that try to do everything.

**Good:**
```python
@mcp.tool()
def get_user(user_id: int) -> dict:
    """Get user information by ID"""
    return database.get_user(user_id)
```

**Bad:**
```python
@mcp.tool()
def manage_users(action: str, user_id: int = None, data: dict = None):
    """Do anything with users"""
    # Too many responsibilities!
```

### 2. Clear Interfaces

Use descriptive names and type hints. Your tool's signature should be self-documenting.

```python
@mcp.tool()
def search_documents(
    query: str,
    limit: int = 10,
    include_archived: bool = False
) -> list[dict]:
    """
    Search documents by query string.

    Args:
        query: Search terms
        limit: Maximum number of results
        include_archived: Whether to include archived documents

    Returns:
        List of matching documents
    """
    pass
```

### 3. Error Handling

Always handle errors gracefully and provide helpful error messages.

```python
@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Input Validation

Validate inputs before processing to catch errors early:

```python
@mcp.tool()
def create_user(username: str, email: str, age: int) -> dict:
    """Create a new user"""
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")

    if not email or '@' not in email:
        raise ValueError("Invalid email address")

    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")

    return database.create_user(username, email, age)
```

## Performance Considerations

### Use Async for I/O Operations

```python
@mcp.tool()
async def fetch_weather(city: str) -> dict:
    """Get weather information for a city"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.weather.com/{city}") as resp:
            return await resp.json()
```

### Implement Caching

For expensive operations, consider caching results:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Get exchange rate (cached)"""
    # Expensive API call
    pass
```

### Limit Result Sizes

Always limit the amount of data returned:

```python
@mcp.tool()
def list_files(directory: str, limit: int = 100) -> list[str]:
    """List files in directory (limited to 100)"""
    files = os.listdir(directory)
    return files[:min(limit, 100)]
```

## Security

### Input Sanitization

Never trust user input. Sanitize and validate everything:

```python
import os.path

@mcp.tool()
def read_file(path: str) -> str:
    """Read a file safely"""
    # Prevent directory traversal
    clean_path = os.path.normpath(path)
    if '..' in clean_path:
        raise ValueError("Invalid path")

    # Only allow reading from specific directory
    allowed_dir = "/safe/directory"
    full_path = os.path.join(allowed_dir, clean_path)

    if not full_path.startswith(allowed_dir):
        raise ValueError("Access denied")

    with open(full_path, 'r') as f:
        return f.read()
```

### Rate Limiting

Implement rate limiting for expensive operations to prevent abuse.

### Audit Logging

Log tool invocations for security and debugging:

```python
import logging

@mcp.tool()
def delete_file(path: str) -> bool:
    """Delete a file"""
    logging.info(f"File deletion requested: {path}")
    # Perform deletion
    return True
```

## Testing Tools

Always write tests for your tools:

```python
def test_add_tool():
    result = add(5, 3)
    assert result == 8

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

## Documentation

Good documentation is essential. Include:
- Purpose of the tool
- Parameter descriptions
- Return value description
- Example usage
- Potential errors

```python
@mcp.tool()
def analyze_text(text: str, language: str = "en") -> dict:
    """
    Analyze text for sentiment and key phrases.

    This tool uses natural language processing to extract insights
    from the provided text.

    Args:
        text: The text to analyze (max 10,000 characters)
        language: Language code (default: "en")

    Returns:
        Dictionary containing:
        - sentiment: Positive/Negative/Neutral
        - score: Confidence score (0-1)
        - key_phrases: List of important phrases

    Raises:
        ValueError: If text is empty or too long
        UnsupportedLanguageError: If language is not supported

    Example:
        >>> analyze_text("I love this product!")
        {'sentiment': 'Positive', 'score': 0.95, 'key_phrases': ['love', 'product']}
    """
    pass
```
