# Resources Reference

Resources provide read-only access to data in your MCP server. They're designed for retrieving information that the LLM might need.

## Basic Resource Definition

```python
@mcp.resource("config://settings/{key}")
def get_setting(key: str) -> str:
    """Get a configuration setting"""
    return settings.get(key, "")
```

## Resource URIs

Resources use URI templates to define their paths:

```python
# Static resource
@mcp.resource("data://users")
def list_users() -> list[dict]:
    """List all users"""
    return get_all_users()

# Dynamic resource with parameters
@mcp.resource("data://users/{user_id}")
def get_user(user_id: str) -> dict:
    """Get a specific user"""
    return get_user_by_id(user_id)

# Multiple parameters
@mcp.resource("files://{category}/{filename}")
def get_file(category: str, filename: str) -> str:
    """Get file content"""
    return read_file(category, filename)
```

## Resource Types

### Text Resources

Return plain text or markdown:

```python
@mcp.resource("docs://readme")
def get_readme() -> str:
    """Get README content"""
    return """
    # My Application

    This is the documentation...
    """
```

### JSON Resources

Return structured data:

```python
@mcp.resource("api://stats")
def get_statistics() -> dict:
    """Get application statistics"""
    return {
        "users": 1000,
        "requests": 50000,
        "uptime": "99.9%"
    }
```

### File Resources

Provide access to files:

```python
from pathlib import Path

@mcp.resource("files://{path}")
def read_file(path: str) -> str:
    """Read a file from the safe directory"""
    # Security: validate path
    safe_path = Path("/safe/directory") / path
    if not safe_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    return safe_path.read_text()
```

## Async Resources

For I/O-bound operations:

```python
@mcp.resource("external://data/{id}")
async def fetch_external_data(id: str) -> dict:
    """Fetch data from external API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/{id}") as resp:
            return await resp.json()
```

## Resource Metadata

Provide additional context about resources:

```python
@mcp.resource(
    "docs://guide/{page}",
    name="Documentation Page",
    description="Access documentation pages by name"
)
def get_doc_page(page: str) -> str:
    """Get a documentation page"""
    return load_documentation(page)
```

## Security Considerations

### Path Validation

Always validate paths to prevent traversal attacks:

```python
@mcp.resource("files://{path}")
def safe_read_file(path: str) -> str:
    """Safely read a file"""
    # Prevent directory traversal
    if '..' in path or path.startswith('/'):
        raise ValueError("Invalid path")

    # Use a whitelist of allowed directories
    allowed_dirs = ['/var/data', '/var/public']
    full_path = Path(allowed_dirs[0]) / path

    # Check if resolved path is within allowed directory
    if not any(str(full_path.resolve()).startswith(d) for d in allowed_dirs):
        raise ValueError("Access denied")

    return full_path.read_text()
```

### Access Control

Implement access control when needed:

```python
@mcp.resource("private://data/{resource_id}")
def get_private_data(resource_id: str, context: Context) -> dict:
    """Get private data with access control"""
    # Check permissions
    if not has_permission(context.user, resource_id):
        raise PermissionError("Access denied")

    return load_private_data(resource_id)
```

## Caching

Cache expensive resource operations:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
@mcp.resource("cached://data/{key}")
def get_cached_data(key: str) -> dict:
    """Get data with caching"""
    # Expensive operation
    return expensive_database_query(key)
```

## Examples

### Configuration Resource

```python
@mcp.resource("config://app")
def get_app_config() -> dict:
    """Get application configuration"""
    return {
        "version": "1.0.0",
        "environment": "production",
        "features": {
            "auth": True,
            "analytics": True
        }
    }
```

### Database Resource

```python
@mcp.resource("db://tables/{table_name}")
async def get_table_schema(table_name: str) -> dict:
    """Get database table schema"""
    schema = await db.get_schema(table_name)
    return {
        "table": table_name,
        "columns": schema.columns,
        "indexes": schema.indexes
    }
```

### Log Resource

```python
@mcp.resource("logs://recent")
def get_recent_logs(limit: int = 100) -> list[str]:
    """Get recent log entries"""
    return read_logs(limit=limit)
```
