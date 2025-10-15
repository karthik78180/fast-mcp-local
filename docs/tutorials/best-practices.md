# Best Practices for MCP Servers

This guide covers best practices for building production-ready MCP servers.

## Code Organization

### Separate Concerns

Keep your tools, resources, and prompts in separate modules:

```
my_mcp_server/
├── __init__.py
├── server.py       # Main server setup
├── tools/          # Tool implementations
├── resources/      # Resource handlers
└── prompts/        # Prompt templates
```

### Use Type Hints

Always use type hints for better IDE support and error catching:

```python
@mcp.tool()
def process_data(input_data: dict[str, Any]) -> list[str]:
    """Process input data and return results"""
    ...
```

## Error Handling

### Validate Input

Always validate input parameters:

```python
@mcp.tool()
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Provide Clear Error Messages

Make errors actionable:

```python
if not user_id:
    raise ValueError("user_id is required and must be a non-empty string")
```

## Performance

### Use Caching

Cache expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_user_data(user_id: str) -> dict:
    # Expensive database query
    ...
```

### Async Operations

Use async for I/O-bound operations:

```python
@mcp.tool()
async def fetch_api_data(url: str) -> dict:
    """Fetch data from an external API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## Security

### Input Sanitization

Never trust user input:

```python
import re

@mcp.tool()
def get_file(filename: str) -> str:
    """Read a file safely"""
    # Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        raise ValueError("Invalid filename")

    # Only allow alphanumeric, dash, underscore, and dot
    if not re.match(r'^[\w\-\.]+$', filename):
        raise ValueError("Filename contains invalid characters")

    # Read from safe directory only
    safe_path = Path('/safe/directory') / filename
    return safe_path.read_text()
```

## Documentation

### Write Clear Docstrings

Your docstrings become the tool's description:

```python
@mcp.tool()
def search_products(
    query: str,
    category: str | None = None,
    max_results: int = 10
) -> list[dict]:
    """
    Search for products in the catalog.

    Args:
        query: Search terms to match against product names and descriptions
        category: Optional category filter (e.g., 'electronics', 'books')
        max_results: Maximum number of results to return (1-100)

    Returns:
        List of matching products with id, name, price, and description

    Raises:
        ValueError: If max_results is out of range or category is invalid
    """
    ...
```

## Testing

### Write Unit Tests

Test each tool independently:

```python
def test_divide_numbers():
    result = divide_numbers(10, 2)
    assert result == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide_numbers(10, 0)
```

## Monitoring

### Add Logging

Log important events:

```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def delete_user(user_id: str) -> bool:
    """Delete a user account"""
    logger.warning(f"Deleting user account: {user_id}")
    # Delete user
    return True
```
