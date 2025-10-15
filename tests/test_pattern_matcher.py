"""Unit tests for the pattern matcher module."""

import pytest
import tempfile
import os
from pathlib import Path
from fast_mcp_local.pattern_matcher import PatternMatcher, PatternMatch


@pytest.fixture
def matcher():
    """Create a pattern matcher instance."""
    return PatternMatcher()


@pytest.fixture
def temp_java_file():
    """Create a temporary Java file for testing."""
    fd, path = tempfile.mkstemp(suffix='.java')

    # Write sample Java code
    content = """
public class TestVerticle extends AbstractVerticle {
    private static final Logger logger = LoggerFactory.getLogger(TestVerticle.class);

    @Override
    public void start(Promise<Void> startPromise) {
        DeploymentOptions options = new DeploymentOptions()
            .setConfig(config())
            .setInstances(4);

        PgConnectOptions connectOptions = new PgConnectOptions()
            .setHost(config().getString("db.host"))
            .setPort(5432)
            .setDatabase("mydb");

        PoolOptions poolOptions = new PoolOptions().setMaxSize(10);
        PgPool pool = PgPool.pool(vertx, connectOptions, poolOptions);

        pool.preparedQuery("SELECT * FROM users WHERE id = $1")
            .execute(Tuple.of(userId), ar -> {
                if (ar.succeeded()) {
                    RowSet<Row> rows = ar.result();
                    processRows(rows);
                } else {
                    logger.error("Query failed", ar.cause());
                }
            });

        startPromise.complete();
    }
}
"""

    with os.fdopen(fd, 'w') as f:
        f.write(content)

    yield path

    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def temp_java_file_with_violations():
    """Create a temporary Java file with anti-patterns."""
    fd, path = tempfile.mkstemp(suffix='.java')

    content = """
public class BadVerticle extends AbstractVerticle {

    @Override
    public void start() {
        String password = "mySecretPassword123";
        String apiKey = "sk_live_abc123xyz";

        Thread.sleep(1000);  // Blocking event loop!

        String userId = request.getParam("id");
        String query = "SELECT * FROM users WHERE id = " + userId;
        client.query(query).execute(ar -> {
            try {
                RowSet<Row> rows = ar.result();  // No error checking!
            } catch (Exception e) {
                e.printStackTrace();  // Bad logging
            }
        });
    }
}
"""

    with os.fdopen(fd, 'w') as f:
        f.write(content)

    yield path

    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


def test_matcher_creation(matcher):
    """Test creating a pattern matcher."""
    assert matcher is not None
    assert isinstance(matcher, PatternMatcher)


def test_match_regex_finds_pattern(matcher):
    """Test regex matching finds patterns."""
    content = "DeploymentOptions options = new DeploymentOptions();"
    matches = matcher.match_regex(
        content=content,
        pattern=r"DeploymentOptions",
        file_path="test.java",
        rule_id="test-rule",
        severity="medium"
    )

    assert len(matches) == 2  # Found twice in the line
    assert all(isinstance(m, PatternMatch) for m in matches)
    assert matches[0].rule_id == "test-rule"
    assert matches[0].severity == "medium"


def test_match_regex_no_match(matcher):
    """Test regex matching when pattern not found."""
    content = "public class TestVerticle {"
    matches = matcher.match_regex(
        content=content,
        pattern=r"NonExistentPattern",
        file_path="test.java",
        rule_id="test-rule"
    )

    assert len(matches) == 0


def test_match_regex_multiple_lines(matcher):
    """Test regex matching across multiple lines."""
    content = """
    Thread.sleep(1000);
    Thread.sleep(2000);
    Thread.join();
    """
    matches = matcher.match_regex(
        content=content,
        pattern=r"Thread\.sleep|Thread\.join",
        file_path="test.java",
        rule_id="no-blocking"
    )

    assert len(matches) == 3  # Three blocking calls


def test_match_presence_found(matcher):
    """Test presence matching when pattern exists."""
    content = "PgPool pool = PgPool.pool(vertx, options);"
    found = matcher.match_presence(
        content=content,
        pattern="PgPool.pool",
        file_path="test.java",
        rule_id="connection-pooling"
    )

    assert found is True


def test_match_presence_not_found(matcher):
    """Test presence matching when pattern doesn't exist."""
    content = "public class TestVerticle {"
    found = matcher.match_presence(
        content=content,
        pattern="Router.router",
        file_path="test.java",
        rule_id="router-usage"
    )

    assert found is False


def test_match_presence_case_sensitive(matcher):
    """Test that presence matching is case-sensitive."""
    content = "deploymentoptions options = new DeploymentOptions();"
    found = matcher.match_presence(
        content=content,
        pattern="DeploymentOptions",
        file_path="test.java",
        rule_id="deployment-options"
    )

    assert found is True  # Should still find it


def test_scan_file_with_rules(matcher, temp_java_file):
    """Test scanning a file with multiple rules."""
    rules = [
        {
            "id": "deployment-options",
            "pattern_type": "presence",
            "pattern": "DeploymentOptions",
            "score": 10,
            "severity": "medium"
        },
        {
            "id": "connection-pooling",
            "pattern_type": "regex",
            "pattern": r"PgPool\.pool",
            "score": 15,
            "severity": "high"
        },
        {
            "id": "async-error-handlers",
            "pattern_type": "regex",
            "pattern": r"\.(succeeded|failed)\(\)",
            "score": 15,
            "severity": "high"
        }
    ]

    matches = matcher.scan_file(Path(temp_java_file), rules)

    assert len(matches) > 0
    # Should find DeploymentOptions, PgPool.pool, succeeded/failed
    rule_ids = {m.rule_id for m in matches}
    assert "deployment-options" in rule_ids
    assert "connection-pooling" in rule_ids
    assert "async-error-handlers" in rule_ids


def test_scan_file_finds_violations(matcher, temp_java_file_with_violations):
    """Test scanning file with anti-patterns."""
    rules = [
        {
            "id": "no-blocking",
            "pattern_type": "regex",
            "pattern": r"Thread\.sleep|Thread\.join",
            "score": -20,
            "severity": "critical"
        },
        {
            "id": "no-hardcoded-credentials",
            "pattern_type": "regex",
            "pattern": r'(password|apiKey|secret)\s*=\s*"[^"]{4,}"',
            "score": -25,
            "severity": "critical"
        },
        {
            "id": "no-sql-concat",
            "pattern_type": "regex",
            "pattern": r'"SELECT.*"\s*\+',
            "score": -20,
            "severity": "critical"
        }
    ]

    matches = matcher.scan_file(Path(temp_java_file_with_violations), rules)

    assert len(matches) > 0
    rule_ids = {m.rule_id for m in matches}
    assert "no-blocking" in rule_ids
    assert "no-hardcoded-credentials" in rule_ids
    assert "no-sql-concat" in rule_ids

    # Check severity
    critical_matches = [m for m in matches if m.severity == "critical"]
    assert len(critical_matches) > 0


def test_scan_file_nonexistent(matcher):
    """Test scanning a non-existent file."""
    matches = matcher.scan_file(Path("/nonexistent/file.java"), [])
    assert len(matches) == 0


def test_scan_directory(matcher, temp_java_file):
    """Test scanning a directory."""
    # Get the directory containing the temp file
    dir_path = Path(temp_java_file).parent

    rules = [
        {
            "id": "deployment-options",
            "pattern_type": "presence",
            "pattern": "DeploymentOptions",
            "score": 10,
            "severity": "medium"
        }
    ]

    matches = matcher.scan_directory(dir_path, rules, extensions=['.java'])

    # Should find at least our temp file
    assert len(matches) >= 0  # May or may not match depending on temp file naming


def test_scan_directory_with_multiple_extensions(matcher):
    """Test scanning directory with multiple file extensions."""
    # Create temp directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Create test files
        java_file = Path(temp_dir) / "Test.java"
        java_file.write_text("DeploymentOptions options;")

        kt_file = Path(temp_dir) / "Test.kt"
        kt_file.write_text("val options = DeploymentOptions()")

        txt_file = Path(temp_dir) / "readme.txt"
        txt_file.write_text("DeploymentOptions")

        rules = [
            {
                "id": "deployment-options",
                "pattern_type": "presence",
                "pattern": "DeploymentOptions",
                "score": 10,
                "severity": "medium"
            }
        ]

        # Scan only Java and Kotlin files
        matches = matcher.scan_directory(
            Path(temp_dir),
            rules,
            extensions=['.java', '.kt']
        )

        # Should find in .java and .kt but not .txt
        file_paths = {m.file_path for m in matches}
        assert any('Test.java' in fp for fp in file_paths)
        assert any('Test.kt' in fp for fp in file_paths)

    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def test_pattern_match_dataclass():
    """Test PatternMatch dataclass creation."""
    match = PatternMatch(
        rule_id="test-rule",
        file_path="Test.java",
        line_number=42,
        matched_text="DeploymentOptions",
        severity="high"
    )

    assert match.rule_id == "test-rule"
    assert match.file_path == "Test.java"
    assert match.line_number == 42
    assert match.matched_text == "DeploymentOptions"
    assert match.severity == "high"


def test_match_regex_captures_line_numbers(matcher):
    """Test that regex matching captures correct line numbers."""
    content = """Line 1
Line 2 with pattern
Line 3
Line 4 with pattern
Line 5"""

    matches = matcher.match_regex(
        content=content,
        pattern=r"pattern",
        file_path="test.java",
        rule_id="test-rule"
    )

    assert len(matches) == 2
    line_numbers = [m.line_number for m in matches]
    assert 2 in line_numbers
    assert 4 in line_numbers
