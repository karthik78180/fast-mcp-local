"""Unit tests for migration module."""

import json
import pytest
from fast_mcp_local.migration import (
    list_migrations,
    get_migration_metadata,
    get_migration_guide,
    get_migration_step,
    extract_step_from_markdown,
    list_migration_ids,
    clear_cache
)


def test_list_migrations():
    """Test listing all available migrations."""
    result = list_migrations()
    data = json.loads(result)

    assert isinstance(data, list)
    # Should have at least v1-to-v2 migration
    assert len(data) >= 1

    # Check structure of first migration
    if len(data) > 0:
        migration = data[0]
        assert 'migration_id' in migration
        assert 'name' in migration
        assert 'description' in migration
        assert 'source_version' in migration
        assert 'target_version' in migration


def test_get_migration_metadata_v1_to_v2():
    """Test getting metadata for v1-to-v2 migration."""
    result = get_migration_metadata('v1-to-v2')
    data = json.loads(result)

    assert 'error' not in data
    assert data['migration_id'] == 'v1-to-v2'
    assert data['name'] == 'V1 to V2 Migration'
    assert data['source_version'] == '1.x'
    assert data['target_version'] == '2.x'
    assert 'openrewrite_dependency' in data
    assert 'prerequisites' in data
    assert 'total_steps' in data
    assert data['total_steps'] == 5


def test_get_migration_metadata_nonexistent():
    """Test getting metadata for nonexistent migration."""
    result = get_migration_metadata('nonexistent')
    data = json.loads(result)

    assert 'error' in data
    assert 'nonexistent' in data['error'].lower()
    assert 'available_migrations' in data


def test_get_migration_guide():
    """Test getting full migration guide."""
    result = get_migration_guide('v1-to-v2')
    data = json.loads(result)

    assert 'error' not in data
    assert data['migration_id'] == 'v1-to-v2'
    assert 'metadata' in data
    assert 'guide' in data or 'steps' in data

    # Check guide content
    if 'guide' in data:
        assert 'V1 to V2 Migration Guide' in data['guide']
        assert 'Overview' in data['guide']

    # Check steps content
    if 'steps' in data:
        assert 'Step 1:' in data['steps']
        assert 'OpenRewrite' in data['steps']


def test_get_migration_guide_nonexistent():
    """Test getting guide for nonexistent migration."""
    result = get_migration_guide('nonexistent')
    data = json.loads(result)

    assert 'error' in data
    assert 'available_migrations' in data


def test_get_migration_step_1():
    """Test getting step 1 from migration."""
    result = get_migration_step('v1-to-v2', 1)
    data = json.loads(result)

    assert 'error' not in data
    assert data['migration_id'] == 'v1-to-v2'
    assert data['step_number'] == 1
    assert data['total_steps'] == 5
    assert 'content' in data

    # Check step 1 content
    content = data['content']
    assert 'Step 1:' in content
    assert 'OpenRewrite' in content
    assert 'build.gradle' in content


def test_get_migration_step_all_steps():
    """Test getting all 5 steps from migration."""
    for step_num in range(1, 6):
        result = get_migration_step('v1-to-v2', step_num)
        data = json.loads(result)

        assert 'error' not in data
        assert data['step_number'] == step_num
        assert 'content' in data
        assert f'Step {step_num}:' in data['content']


def test_get_migration_step_out_of_range():
    """Test getting step with invalid number."""
    # Step 0 (too low)
    result = get_migration_step('v1-to-v2', 0)
    data = json.loads(result)
    assert 'error' in data
    assert 'out of range' in data['error'].lower()

    # Step 99 (too high)
    result = get_migration_step('v1-to-v2', 99)
    data = json.loads(result)
    assert 'error' in data
    assert 'out of range' in data['error'].lower()


def test_get_migration_step_nonexistent_migration():
    """Test getting step for nonexistent migration."""
    result = get_migration_step('nonexistent', 1)
    data = json.loads(result)

    assert 'error' in data
    assert 'available_migrations' in data


def test_extract_step_from_markdown():
    """Test extracting specific step from markdown."""
    markdown = """# Migration Steps

## Step 1: First Step
This is the first step.
Some content here.

## Step 2: Second Step
This is the second step.

## Step 3: Third Step
Final step.
"""

    # Extract step 1
    step1 = extract_step_from_markdown(markdown, 1)
    assert step1 is not None
    assert 'Step 1: First Step' in step1
    assert 'This is the first step' in step1
    assert 'Step 2:' not in step1

    # Extract step 2
    step2 = extract_step_from_markdown(markdown, 2)
    assert step2 is not None
    assert 'Step 2: Second Step' in step2
    assert 'This is the second step' in step2
    assert 'Step 1:' not in step2
    assert 'Step 3:' not in step2

    # Extract step 3 (last)
    step3 = extract_step_from_markdown(markdown, 3)
    assert step3 is not None
    assert 'Step 3: Third Step' in step3
    assert 'Final step' in step3


def test_extract_step_from_markdown_not_found():
    """Test extracting nonexistent step."""
    markdown = """# Migration Steps

## Step 1: Only Step
Just one step.
"""

    result = extract_step_from_markdown(markdown, 2)
    assert result is None


def test_list_migration_ids():
    """Test listing migration IDs."""
    ids = list_migration_ids()

    assert isinstance(ids, list)
    assert 'v1-to-v2' in ids
    # Should be sorted
    assert ids == sorted(ids)


def test_clear_cache():
    """Test clearing metadata cache."""
    # Call some functions to populate cache
    get_migration_metadata('v1-to-v2')

    # Clear cache should not raise error
    clear_cache()


def test_migration_metadata_structure():
    """Test complete structure of migration metadata."""
    result = get_migration_metadata('v1-to-v2')
    data = json.loads(result)

    # Check openrewrite_dependency structure
    assert 'openrewrite_dependency' in data
    dep = data['openrewrite_dependency']
    assert 'group' in dep
    assert 'artifact' in dep
    assert 'version' in dep
    assert 'recipe_class' in dep

    # Check prerequisites structure
    assert 'prerequisites' in data
    prereqs = data['prerequisites']
    assert 'java_version' in prereqs
    assert 'gradle_version' in prereqs

    # Check other fields
    assert 'estimated_time' in data
    assert 'tags' in data
    assert isinstance(data['tags'], list)


def test_migration_guide_gradle_setup():
    """Test that gradle setup documentation exists."""
    result = get_migration_guide('v1-to-v2')
    data = json.loads(result)

    # Should have gradle_setup if file exists
    # (optional, so just check if present it's valid)
    if 'gradle_setup' in data:
        assert isinstance(data['gradle_setup'], str)
        assert len(data['gradle_setup']) > 0


def test_migration_steps_content():
    """Test that step content is comprehensive."""
    result = get_migration_step('v1-to-v2', 1)
    data = json.loads(result)

    content = data['content']

    # Step 1 should mention these key things
    assert 'gradle' in content.lower()
    assert 'plugin' in content.lower()
    assert 'dependency' in content.lower() or 'dependencies' in content.lower()

    # Should have code blocks (markdown)
    assert '```' in content


def test_migration_steps_order():
    """Test that steps are in logical order."""
    # Get all steps
    steps = []
    for i in range(1, 6):
        result = get_migration_step('v1-to-v2', i)
        data = json.loads(result)
        steps.append(data['content'])

    # Step 1 should be setup
    assert 'gradle' in steps[0].lower() or 'plugin' in steps[0].lower()

    # Step 2 should be prerequisites
    assert 'prereq' in steps[1].lower() or 'check' in steps[1].lower()

    # Step 3 should be dry run
    assert 'dry' in steps[2].lower() or 'preview' in steps[2].lower()

    # Step 4 should be apply
    assert 'apply' in steps[3].lower() or 'run' in steps[3].lower()

    # Step 5 should be verify
    assert 'verify' in steps[4].lower() or 'test' in steps[4].lower()


def test_json_output_format():
    """Test that all functions return valid JSON."""
    functions_to_test = [
        (list_migrations, ()),
        (get_migration_metadata, ('v1-to-v2',)),
        (get_migration_guide, ('v1-to-v2',)),
        (get_migration_step, ('v1-to-v2', 1)),
    ]

    for func, args in functions_to_test:
        result = func(*args)
        # Should be valid JSON
        try:
            data = json.loads(result)
            assert data is not None
        except json.JSONDecodeError:
            pytest.fail(f"{func.__name__} did not return valid JSON")
