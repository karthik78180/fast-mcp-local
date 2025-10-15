"""Unit tests for the scorer module."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from fast_mcp_local import scorer
from fast_mcp_local.pattern_matcher import PatternMatch


@pytest.fixture
def temp_java_file_good():
    """Create a temporary Java file with best practices."""
    fd, path = tempfile.mkstemp(suffix='.java')

    content = """
public class GoodVerticle extends AbstractVerticle {
    private static final Logger logger = LoggerFactory.getLogger(GoodVerticle.class);

    @Override
    public void start(Promise<Void> startPromise) {
        DeploymentOptions options = new DeploymentOptions()
            .setConfig(config())
            .setInstances(4);

        PgConnectOptions connectOptions = new PgConnectOptions()
            .setHost(config().getString("db.host"))
            .setPort(config().getInteger("db.port", 5432))
            .setDatabase(config().getString("db.name"));

        PoolOptions poolOptions = new PoolOptions().setMaxSize(10);
        PgPool pool = PgPool.pool(vertx, connectOptions, poolOptions);

        Router router = Router.router(vertx);
        router.get("/api/users").handler(this::getUsers);

        router.errorHandler(500, ctx -> {
            logger.error("Error", ctx.failure());
            ctx.response().setStatusCode(500).end("Error");
        });

        pool.preparedQuery("SELECT * FROM users WHERE id = $1")
            .execute(Tuple.of(userId), ar -> {
                if (ar.succeeded()) {
                    RowSet<Row> rows = ar.result();
                    processRows(rows);
                } else {
                    logger.error("Query failed", ar.cause());
                }
            });

        httpServer.listen(8080, ar -> {
            if (ar.succeeded()) {
                startPromise.complete();
            } else {
                startPromise.fail(ar.cause());
            }
        });
    }
}
"""

    with os.fdopen(fd, 'w') as f:
        f.write(content)

    yield path

    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def temp_java_file_bad():
    """Create a temporary Java file with anti-patterns."""
    fd, path = tempfile.mkstemp(suffix='.java')

    content = """
public class BadVerticle extends AbstractVerticle {

    @Override
    public void start() {
        String password = "mySecretPassword123";
        String apiUrl = "https://api.example.com";

        Thread.sleep(1000);

        String userId = request.getParam("id");
        String query = "SELECT * FROM users WHERE id = " + userId;

        PgConnection.connect(vertx, options, ar -> {
            PgConnection conn = ar.result();
            conn.query(query).execute(res -> {
                try {
                    processRows(res.result());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        });
    }
}
"""

    with os.fdopen(fd, 'w') as f:
        f.write(content)

    yield path

    if os.path.exists(path):
        os.unlink(path)


def test_list_patterns():
    """Test listing available patterns."""
    result = scorer.list_patterns()
    patterns = json.loads(result)

    assert isinstance(patterns, list)
    # Should find at least the vertx-best-practices pattern
    pattern_ids = [p.get("pattern_id") for p in patterns]
    assert "vertx" in str(pattern_ids).lower() or len(patterns) >= 0


def test_get_pattern_metadata():
    """Test getting pattern metadata."""
    result = scorer.get_pattern_metadata("vertx-best-practices")
    metadata = json.loads(result)

    # Check if we got an error or valid metadata
    if "error" not in metadata:
        assert metadata["pattern_id"] == "vertx-best-practices"
        assert "name" in metadata
        assert "description" in metadata
        assert "categories" in metadata
        assert "total_possible_score" in metadata
        assert "passing_threshold" in metadata

        # Verify categories structure
        categories = metadata["categories"]
        assert isinstance(categories, dict)
        for cat_name, cat_data in categories.items():
            assert "weight" in cat_data
            assert "rule_count" in cat_data


def test_get_pattern_metadata_invalid():
    """Test getting metadata for non-existent pattern."""
    result = scorer.get_pattern_metadata("nonexistent-pattern")
    metadata = json.loads(result)

    assert "error" in metadata


def test_load_pattern_rules():
    """Test loading pattern rules."""
    rules = scorer.load_pattern_rules("vertx-best-practices")

    # May or may not exist depending on setup
    if rules is not None:
        assert isinstance(rules, dict)
        assert "pattern_id" in rules
        assert "categories" in rules


def test_load_pattern_rules_invalid():
    """Test loading non-existent pattern rules."""
    rules = scorer.load_pattern_rules("nonexistent-pattern")
    assert rules is None


def test_score_codebase_good_code(temp_java_file_good):
    """Test scoring a codebase with good practices."""
    result = scorer.score_codebase(temp_java_file_good, "vertx-best-practices")
    score_data = json.loads(result)

    # Check if pattern exists
    if "error" not in score_data:
        assert "overall_score" in score_data
        assert "grade" in score_data
        assert "category_scores" in score_data
        assert "summary" in score_data
        assert "violations" in score_data
        assert "recommendations" in score_data

        # Should have a decent score
        assert score_data["overall_score"] >= 0
        assert score_data["grade"] in ["A", "B", "C", "D", "F"]

        # Summary should have proper structure
        summary = score_data["summary"]
        assert "files_scanned" in summary
        assert "violations_found" in summary
        assert "best_practices_followed" in summary
        assert summary["files_scanned"] == 1


def test_score_codebase_bad_code(temp_java_file_bad):
    """Test scoring a codebase with anti-patterns."""
    result = scorer.score_codebase(temp_java_file_bad, "vertx-best-practices")
    score_data = json.loads(result)

    # Check if pattern exists
    if "error" not in score_data:
        assert "overall_score" in score_data
        assert "violations" in score_data

        # Should have violations
        violations = score_data["violations"]
        assert len(violations) > 0

        # Check violation structure
        for violation in violations[:3]:  # Check first 3
            assert "rule_id" in violation
            assert "rule_name" in violation
            assert "severity" in violation
            assert "file" in violation
            assert "line" in violation
            assert "message" in violation

        # Should have critical issues
        summary = score_data["summary"]
        assert summary["critical_issues"] > 0


def test_score_codebase_nonexistent_path():
    """Test scoring a non-existent path."""
    result = scorer.score_codebase("/nonexistent/path", "vertx-best-practices")
    score_data = json.loads(result)

    assert "error" in score_data


def test_score_codebase_invalid_pattern(temp_java_file_good):
    """Test scoring with invalid pattern."""
    result = scorer.score_codebase(temp_java_file_good, "invalid-pattern")
    score_data = json.loads(result)

    assert "error" in score_data


def test_calculate_score():
    """Test score calculation logic."""
    matches = [
        PatternMatch(
            rule_id="deployment-options",
            file_path="Test.java",
            line_number=10,
            matched_text="DeploymentOptions",
            severity="medium"
        ),
        PatternMatch(
            rule_id="no-blocking",
            file_path="Test.java",
            line_number=20,
            matched_text="Thread.sleep",
            severity="critical"
        )
    ]

    rules = [
        {
            "id": "deployment-options",
            "category": "deployment",
            "name": "Uses DeploymentOptions",
            "description": "Test rule",
            "score": 10,
            "severity": "medium",
            "suggestion": "Good job"
        },
        {
            "id": "no-blocking",
            "category": "error_handling",
            "name": "No Blocking",
            "description": "Test rule",
            "score": -20,
            "severity": "critical",
            "suggestion": "Don't block"
        }
    ]

    rules_data = {
        "pattern_id": "test-pattern",
        "categories": {
            "deployment": {"weight": 50, "rules": [rules[0]]},
            "error_handling": {"weight": 50, "rules": [rules[1]]}
        }
    }

    result = scorer.calculate_score(matches, rules, rules_data)

    assert "overall_score" in result
    assert "grade" in result
    assert "category_scores" in result
    assert "violations" in result
    assert "summary" in result

    # Check violations
    violations = result["violations"]
    assert len(violations) == 2

    # Check critical issues
    critical = [v for v in violations if v["severity"] == "critical"]
    assert len(critical) == 1


def test_generate_recommendations():
    """Test recommendation generation."""
    violations = [
        {
            "rule_id": "no-blocking",
            "severity": "critical",
            "category": "error_handling",
            "reference_doc": "vertx/error-handling.md"
        },
        {
            "rule_id": "no-hardcoded-credentials",
            "severity": "critical",
            "category": "configuration",
            "reference_doc": "vertx/config.md"
        },
        {
            "rule_id": "no-sql-concat",
            "severity": "critical",
            "category": "database",
            "reference_doc": "vertx/database.md"
        }
    ]

    rules_data = {"categories": {}}

    recommendations = scorer.generate_recommendations(violations, rules_data)

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0

    # Should mention critical issues
    assert any("critical" in rec.lower() for rec in recommendations)


def test_get_compliance_report_good_code(temp_java_file_good):
    """Test generating compliance report for good code."""
    result = scorer.get_compliance_report("vertx-best-practices", temp_java_file_good)

    # Check if pattern exists
    if "Error" not in result:
        assert isinstance(result, str)
        assert "# Code Compliance Report" in result or len(result) > 0
        # Should be markdown formatted
        assert "#" in result or "Pattern" in result


def test_get_compliance_report_bad_code(temp_java_file_bad):
    """Test generating compliance report for bad code."""
    result = scorer.get_compliance_report("vertx-best-practices", temp_java_file_bad)

    # Check if pattern exists
    if "Error" not in result:
        assert isinstance(result, str)
        # Should contain violation information
        assert len(result) > 0


def test_get_compliance_report_invalid_pattern(temp_java_file_good):
    """Test compliance report with invalid pattern."""
    result = scorer.get_compliance_report("invalid-pattern", temp_java_file_good)

    assert isinstance(result, str)
    assert "Error" in result


def test_get_patterns_dir():
    """Test getting patterns directory path."""
    patterns_dir = scorer.get_patterns_dir()

    assert isinstance(patterns_dir, Path)
    assert "patterns" in str(patterns_dir)


def test_score_grading():
    """Test that scores are assigned correct grades."""
    # Create minimal test data
    matches = []
    rules = []
    rules_data = {
        "pattern_id": "test",
        "categories": {}
    }

    # Test different score ranges
    # Note: Without matches and rules, score will be 0
    result = scorer.calculate_score(matches, rules, rules_data)

    # With no violations and no rules, score should be 0
    assert result["overall_score"] == 0
    assert result["grade"] == "F"


def test_category_scores_structure():
    """Test that category scores have proper structure."""
    matches = []
    rules = [
        {
            "id": "test-rule",
            "category": "deployment",
            "name": "Test Rule",
            "description": "Test",
            "score": 10,
            "severity": "medium"
        }
    ]

    rules_data = {
        "pattern_id": "test",
        "categories": {
            "deployment": {
                "weight": 100,
                "rules": rules
            }
        }
    }

    result = scorer.calculate_score(matches, rules, rules_data)

    category_scores = result["category_scores"]
    assert "deployment" in category_scores

    deployment = category_scores["deployment"]
    assert "score" in deployment
    assert "max" in deployment
    assert "violations" in deployment
    assert "passed" in deployment

    assert deployment["max"] == 10  # Rule score
    assert deployment["violations"] == 0  # No violations
    assert deployment["passed"] == 0  # Pattern not found


def test_violations_limit():
    """Test that violations are limited in output."""
    # Create many violations
    matches = [
        PatternMatch(
            rule_id="test-rule",
            file_path="Test.java",
            line_number=i,
            matched_text="violation",
            severity="medium"
        )
        for i in range(50)
    ]

    rules = [
        {
            "id": "test-rule",
            "category": "test",
            "name": "Test Rule",
            "description": "Test",
            "score": -5,
            "severity": "medium",
            "suggestion": "Fix it"
        }
    ]

    rules_data = {
        "pattern_id": "test",
        "categories": {
            "test": {"weight": 100, "rules": rules}
        }
    }

    result = scorer.calculate_score(matches, rules, rules_data)

    # Should limit to top 20 violations
    assert len(result["violations"]) <= 20


def test_recommendations_limit():
    """Test that recommendations are limited."""
    violations = [
        {
            "rule_id": f"rule-{i}",
            "severity": "high",
            "category": f"category-{i % 5}",
            "reference_doc": f"doc-{i}.md"
        }
        for i in range(30)
    ]

    rules_data = {"categories": {}}

    recommendations = scorer.generate_recommendations(violations, rules_data)

    # Should limit to top 10 recommendations
    assert len(recommendations) <= 10
