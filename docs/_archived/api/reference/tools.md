# Tools Reference

Tools are callable functions exposed through the MCP protocol that LLMs can invoke.

## Basic Tool Definition

```python
@mcp.tool()
def tool_name(param1: str, param2: int) -> str:
    """Tool description that the LLM sees"""
    return f"Result: {param1} {param2}"
```

## Parameters

### Required Parameters

Parameters without defaults are required:

```python
@mcp.tool()
def greet(name: str) -> str:
    """Greet someone"""
    return f"Hello, {name}!"
```

### Optional Parameters

Use default values for optional parameters:

```python
@mcp.tool()
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet someone with a custom greeting"""
    return f"{greeting}, {name}!"
```

### Type Annotations

Supported types:
- `str`: String values
- `int`: Integer numbers
- `float`: Floating-point numbers
- `bool`: Boolean values
- `list[T]`: Lists of a specific type
- `dict[K, V]`: Dictionaries with specific key/value types
- `Optional[T]`: Optional values (can be None)
- `Union[T1, T2]`: Multiple possible types

## Return Values

Tools can return:
- Simple types: `str`, `int`, `float`, `bool`
- Complex types: `dict`, `list`
- JSON-serializable objects

```python
@mcp.tool()
def get_user(user_id: int) -> dict:
    """Get user information"""
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com"
    }
```

## Async Tools

For I/O-bound operations, use async tools:

```python
@mcp.tool()
async def fetch_data(url: str) -> dict:
    """Fetch data from a URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## Error Handling

Raise exceptions for error conditions:

```python
@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Documentation

### Docstring Format

Use clear, descriptive docstrings:

```python
@mcp.tool()
def search_database(
    query: str,
    limit: int = 10
) -> list[dict]:
    """
    Search the database for matching records.

    Args:
        query: Search terms to match
        limit: Maximum number of results (default: 10)

    Returns:
        List of matching database records

    Raises:
        ValueError: If limit is negative or exceeds 1000
    """
    ...
```

## Examples

### Simple Calculation Tool

```python
@mcp.tool()
def calculate_area(width: float, height: float) -> float:
    """Calculate the area of a rectangle"""
    return width * height
```

### Data Transformation Tool

```python
@mcp.tool()
def format_address(
    street: str,
    city: str,
    state: str,
    zip_code: str
) -> str:
    """Format an address string"""
    return f"{street}\n{city}, {state} {zip_code}"
```

### Database Query Tool

```python
@mcp.tool()
async def query_users(
    role: str | None = None,
    active: bool = True
) -> list[dict]:
    """
    Query users from the database.

    Args:
        role: Filter by user role (e.g., 'admin', 'user')
        active: Only return active users (default: True)

    Returns:
        List of user records matching the criteria
    """
    # Database query implementation
    ...
```
