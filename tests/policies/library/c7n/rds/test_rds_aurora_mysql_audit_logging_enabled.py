import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/rds/rds-aurora-mysql-audit-logging-enabled.yml"


def test_compliant():
    tf = tf_resource(
        "aws_rds_cluster", "db",
        '  engine                          = "aurora-mysql"\n  enabled_cloudwatch_logs_exports = ["audit"]\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_no_logs():
    tf = tf_resource(
        "aws_rds_cluster", "db",
        '  engine                          = "aurora-mysql"\n  enabled_cloudwatch_logs_exports = []\n',
    )
    assert c7n_violations(POLICY, tf) != []


def test_not_aurora_not_flagged():
    # Non-aurora engine should not be flagged by this policy
    tf = tf_resource(
        "aws_rds_cluster", "db",
        '  engine                          = "postgres"\n  enabled_cloudwatch_logs_exports = []\n',
    )
    assert c7n_violations(POLICY, tf) == []
