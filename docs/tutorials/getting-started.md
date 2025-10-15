# Getting Started with FastMCP

Welcome to the FastMCP getting started guide! This tutorial will walk you through creating your first MCP server.

## Prerequisites

Before you begin, make sure you have:
- Python 3.10 or higher installed
- Basic understanding of Python programming
- Familiarity with command-line tools

## Installation

First, install FastMCP using pip:

```bash
pip install fastmcp
```

## Creating Your First Server

Let's create a simple MCP server:

```python
from fastmcp import FastMCP

mcp = FastMCP("my-first-server")

@mcp.tool()
def hello_world(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

## Running the Server

Save the code above as `server.py` and run it:

```bash
python server.py
```

Your MCP server is now running and ready to accept connections!

## Next Steps

- Learn about [advanced tools](../api/reference/tools.md)
- Explore [resource management](../api/reference/resources.md)
- Check out [best practices](best-practices.md)
