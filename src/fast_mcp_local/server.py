"""Minimal FastMCP server implementation."""

from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("fast-mcp-local")


def greet(name: str) -> str:
    """Greet a person by name.

    Args:
        name: The name of the person to greet

    Returns:
        A greeting message
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    return a + b


# Register tools with MCP
mcp.tool()(greet)
mcp.tool()(add)


if __name__ == "__main__":
    mcp.run()
