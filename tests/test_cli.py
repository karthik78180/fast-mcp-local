"""Unit tests for CLI wrapper."""

import json
import pytest
from click.testing import CliRunner
from fast_mcp_local.cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Fast MCP Local' in result.output
    assert 'Commands:' in result.output


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0


def test_search_command(runner):
    """Test search command."""
    result = runner.invoke(cli, ['search', 'postgres'])
    assert result.exit_code == 0
    # Should return JSON
    try:
        data = json.loads(result.output)
        assert isinstance(data, list)
    except json.JSONDecodeError:
        pytest.fail("Search command did not return valid JSON")


def test_search_command_with_limit(runner):
    """Test search command with limit option."""
    result = runner.invoke(cli, ['search', 'verticle', '--limit', '2'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) <= 2
    except json.JSONDecodeError:
        pytest.fail("Search command did not return valid JSON")


def test_list_docs_command(runner):
    """Test list-docs command."""
    result = runner.invoke(cli, ['list-docs'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, list)
    except json.JSONDecodeError:
        pytest.fail("List-docs command did not return valid JSON")


def test_get_command(runner):
    """Test get command with valid document."""
    result = runner.invoke(cli, ['get', 'vertx/README.md'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, dict)
        assert 'content' in data or 'error' not in data
    except json.JSONDecodeError:
        pytest.fail("Get command did not return valid JSON")


def test_get_command_nonexistent(runner):
    """Test get command with nonexistent document."""
    result = runner.invoke(cli, ['get', 'nonexistent.md'])
    assert result.exit_code == 0
    # Should return error message
    assert 'not found' in result.output.lower()


def test_list_verticles_command(runner):
    """Test list-verticles command."""
    result = runner.invoke(cli, ['list-verticles'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, list)
        # Should have at least postgres and http
        types = [item['type'] for item in data]
        assert 'postgres' in types or 'http' in types
    except json.JSONDecodeError:
        pytest.fail("List-verticles command did not return valid JSON")


def test_generate_postgres(runner):
    """Test generate command for postgres verticle."""
    result = runner.invoke(cli, ['generate', 'postgres'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, dict)
        assert data['type'] == 'postgres'
        assert 'verticle_code' in data
        assert 'gradle_dependencies' in data
        assert 'config_example' in data
        assert 'PostgresVerticle' in data['verticle_code']
    except json.JSONDecodeError:
        pytest.fail("Generate command did not return valid JSON")


def test_generate_http(runner):
    """Test generate command for http verticle."""
    result = runner.invoke(cli, ['generate', 'http'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, dict)
        assert data['type'] == 'http'
        assert 'verticle_code' in data
        assert 'HttpVerticle' in data['verticle_code']
    except json.JSONDecodeError:
        pytest.fail("Generate command did not return valid JSON")


def test_generate_invalid_type(runner):
    """Test generate command with invalid verticle type."""
    result = runner.invoke(cli, ['generate', 'nonexistent'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert 'error' in data
        assert 'Unknown verticle type' in data['error']
    except json.JSONDecodeError:
        pytest.fail("Generate command did not return valid JSON")


def test_ask_command(runner):
    """Test ask command (alias for search)."""
    result = runner.invoke(cli, ['ask', 'postgres'])
    assert result.exit_code == 0
    try:
        data = json.loads(result.output)
        assert isinstance(data, list)
        # Ask uses limit=5 by default
        assert len(data) <= 5
    except json.JSONDecodeError:
        pytest.fail("Ask command did not return valid JSON")


def test_command_with_missing_argument(runner):
    """Test command with missing required argument."""
    result = runner.invoke(cli, ['search'])
    assert result.exit_code != 0
    assert 'Error' in result.output or 'Missing argument' in result.output


def test_all_commands_available(runner):
    """Test that all expected commands are registered."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0

    expected_commands = [
        'search',
        'list-docs',
        'get',
        'generate',
        'list-verticles',
        'ask'
    ]

    for command in expected_commands:
        assert command in result.output, f"Command '{command}' not found in help output"


def test_json_output_format(runner):
    """Test that all commands return valid JSON."""
    commands = [
        (['search', 'test'], list),
        (['list-docs'], list),
        (['list-verticles'], list),
        (['generate', 'postgres'], dict),
    ]

    for cmd_args, expected_type in commands:
        result = runner.invoke(cli, cmd_args)
        assert result.exit_code == 0, f"Command {cmd_args} failed"
        try:
            data = json.loads(result.output)
            assert isinstance(data, expected_type), \
                f"Command {cmd_args} returned wrong type: {type(data)}"
        except json.JSONDecodeError:
            pytest.fail(f"Command {cmd_args} did not return valid JSON")
