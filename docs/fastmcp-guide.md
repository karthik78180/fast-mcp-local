# FastMCP Guide

## Introduction

FastMCP is a Python framework that makes it incredibly easy to build Model Context Protocol (MCP) servers. It's designed with simplicity and developer experience in mind.

## Why FastMCP?

### Simplicity
FastMCP reduces boilerplate code and allows you to focus on building functionality rather than protocol implementation.

### Type Safety
Built with modern Python type hints, FastMCP provides excellent IDE support and catches errors early.

### Async First
FastMCP is built on asyncio, making it efficient for I/O-bound operations like database queries and API calls.

## Getting Started

### Installation

```bash
pip install fastmcp
```

### Basic Server

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"
```

## Core Concepts

### Tools

Tools are functions that the LLM can call. They're defined using the `@mcp.tool()` decorator:

```python
@mcp.tool()
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b
```

### Resources

Resources provide read-only access to data:

```python
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read a file from the filesystem"""
    with open(path, 'r') as f:
        return f.read()
```

### Prompts

Prompts are reusable templates:

```python
@mcp.prompt()
def code_review_prompt(language: str) -> str:
    """Generate a code review prompt"""
    return f"Review this {language} code for best practices..."
```

## Best Practices

1. **Clear Documentation**: Always include descriptive docstrings
2. **Type Hints**: Use proper type annotations for better tooling
3. **Error Handling**: Handle exceptions gracefully
4. **Validation**: Validate inputs before processing
5. **Testing**: Write tests for your tools and resources

## Advanced Features

### Async Tools

```python
@mcp.tool()
async def fetch_data(url: str) -> dict:
    """Fetch data from an API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Context Management

FastMCP provides context objects for accessing server state and metadata.

### Lifecycle Hooks

Define startup and shutdown handlers for resource initialization and cleanup.
