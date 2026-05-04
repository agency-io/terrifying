import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/rds/rds-aurora-mysql-audit-logging-enabled.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_rds_cluster",
                "cluster",
                {
                    "engine": "aurora-mysql",
                    "enabled_cloudwatch_logs_exports": ["audit", "error"],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input(
        [
            resource(
                "aws_rds_cluster",
                "cluster",
                {
                    "engine": "aurora-mysql",
                    "enabled_cloudwatch_logs_exports": ["error"],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_non_aurora_not_flagged():
    inp = rego_input(
        [
            resource(
                "aws_rds_cluster",
                "cluster",
                {
                    "engine": "aurora-postgresql",
                    "enabled_cloudwatch_logs_exports": [],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []
