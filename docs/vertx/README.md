# Vert.x Verticle Templates

## Overview
This directory contains templates and configurations for generating Vert.x verticles. Use the MCP tools to generate working verticle code with proper Gradle dependencies and deployment configurations.

## Available Templates

### PostgreSQL Verticle
- **Type**: `postgres`
- **Description**: Database client verticle for PostgreSQL operations with reactive connection pooling
- **Use Cases**: CRUD operations, connection pooling, reactive queries
- **Template**: [postgres-verticle.md](templates/postgres-verticle.md)

### HTTP Server Verticle
- **Type**: `http`
- **Description**: REST API server verticle using Vert.x Web router
- **Use Cases**: REST APIs, microservices endpoints, web backends
- **Template**: [http-verticle.md](templates/http-verticle.md)

## Usage

### List Available Verticle Types
```
Tool: list_verticle_types()
```

Returns all available verticle templates with their descriptions and dependencies.

### Generate a Verticle
```
Tool: generate_verticle("postgres")
Tool: generate_verticle("http")
```

Returns complete verticle code including:
- Java source code
- Gradle dependencies
- Configuration example
- Deployment example

### Search for Deployment Patterns
```
Tool: search_documents("deployment")
Tool: get_document("vertx/deployment-config.md")
```

Use existing document search tools to find deployment configurations and patterns.

## Directory Structure

```
vertx/
├── README.md                   # This file
├── deployment-config.md        # Deployment configurations and patterns
├── templates/                  # Verticle code templates
│   ├── postgres-verticle.md
│   └── http-verticle.md
└── schemas/                    # Metadata for each verticle type
    ├── postgres.json
    └── http.json
```

## Template Format

Each template contains:
- **Description**: What the verticle does
- **Gradle Dependencies**: Required dependencies in Gradle format
- **Verticle Code**: Complete Java implementation
- **Configuration Example**: JSON configuration structure
- **Deployment Example**: How to deploy the verticle
- **Use Cases**: When to use this verticle

## Adding New Templates

To add a new verticle type:

1. Create `templates/[type]-verticle.md` with the template content
2. Create `schemas/[type].json` with metadata
3. Reload the MCP server

The new template will automatically be available through the tools.

## Gradle Setup

All templates use Gradle for dependency management. Basic build.gradle:

```gradle
plugins {
    id 'java'
    id 'application'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'io.vertx:vertx-core:4.5.0'
    // Add specific verticle dependencies
}

application {
    mainClass = 'com.example.MainVerticle'
}
```

## Learn More

- [Vert.x Documentation](https://vertx.io/docs/)
- [Vert.x Examples](https://github.com/vert-x3/vertx-examples)
- [Deployment Config Guide](deployment-config.md)
