"""Unit tests for TemplateExtractor."""

import pytest
from fast_mcp_local.template_extractor import TemplateExtractor


@pytest.fixture
def extractor():
    """Create a TemplateExtractor instance."""
    return TemplateExtractor()


def test_extract_java_code(extractor):
    """Test extracting Java code from markdown."""
    markdown = """
# Test Template

## Verticle Code
```java
public class TestVerticle extends AbstractVerticle {
    @Override
    public void start() {
        System.out.println("Started");
    }
}
```
"""
    blocks = extractor.extract_code_blocks(markdown)
    assert "java" in blocks
    assert "TestVerticle" in blocks["java"]
    assert "AbstractVerticle" in blocks["java"]


def test_extract_gradle_dependencies(extractor):
    """Test extracting Gradle dependencies."""
    markdown = """
## Gradle Dependencies
```gradle
dependencies {
    implementation 'io.vertx:vertx-core:4.5.0'
    implementation 'io.vertx:vertx-web:4.5.0'
}
```
"""
    blocks = extractor.extract_code_blocks(markdown)
    assert "gradle" in blocks
    assert "vertx-core" in blocks["gradle"]
    assert "vertx-web" in blocks["gradle"]


def test_extract_json_config(extractor):
    """Test extracting JSON configuration."""
    markdown = """
## Configuration Example
```json
{
  "http": {
    "port": 8080,
    "host": "localhost"
  }
}
```
"""
    blocks = extractor.extract_code_blocks(markdown)
    assert "json" in blocks
    assert "http" in blocks["json"]
    assert "8080" in blocks["json"]


def test_extract_deployment_example(extractor):
    """Test extracting deployment example."""
    markdown = """
## Deployment Example
```java
DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setInstances(1);
vertx.deployVerticle(new MyVerticle(), options);
```
"""
    blocks = extractor.extract_code_blocks(markdown)
    assert "deployment" in blocks
    assert "DeploymentOptions" in blocks["deployment"]
    assert "deployVerticle" in blocks["deployment"]


def test_extract_multiple_code_blocks(extractor):
    """Test extracting multiple code blocks of different types."""
    markdown = """
# Template

## Gradle Dependencies
```gradle
dependencies {
    implementation 'io.vertx:vertx-core:4.5.0'
}
```

## Verticle Code
```java
public class TestVerticle {}
```

## Configuration Example
```json
{"test": "value"}
```

## Deployment Example
```java
vertx.deployVerticle(new TestVerticle());
```
"""
    blocks = extractor.extract_code_blocks(markdown)
    assert "gradle" in blocks
    assert "java" in blocks
    assert "json" in blocks
    assert "deployment" in blocks


def test_extract_description(extractor):
    """Test extracting description section."""
    markdown = """
# Test Template

## Description
This is a test verticle for demonstration purposes.

## Verticle Code
```java
public class Test {}
```
"""
    description = extractor.extract_description(markdown)
    assert "test verticle" in description
    assert "demonstration" in description


def test_extract_description_not_found(extractor):
    """Test extracting description when section doesn't exist."""
    markdown = """
# Test Template

## Verticle Code
```java
public class Test {}
```
"""
    description = extractor.extract_description(markdown)
    assert description == ""


def test_extract_section(extractor):
    """Test extracting arbitrary section."""
    markdown = """
# Template

## Use Cases
- Use case 1
- Use case 2
- Use case 3

## Other Section
Content
"""
    section = extractor.extract_section(markdown, "Use Cases")
    assert "Use case 1" in section
    assert "Use case 2" in section
    assert "Use case 3" in section


def test_extract_section_not_found(extractor):
    """Test extracting non-existent section."""
    markdown = """
# Template

## Existing Section
Content
"""
    section = extractor.extract_section(markdown, "Non-Existent")
    assert section == ""


def test_empty_markdown(extractor):
    """Test handling empty markdown."""
    blocks = extractor.extract_code_blocks("")
    assert blocks == {}
    assert extractor.extract_description("") == ""


def test_no_code_blocks(extractor):
    """Test markdown with no code blocks."""
    markdown = """
# Template

This is just text with no code blocks.
"""
    blocks = extractor.extract_code_blocks(markdown)
    assert blocks == {}
