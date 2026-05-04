import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elasticache/elasticache-redis-cluster-automatic-backup-check.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_elasticache_replication_group",
                "rg",
                {"snapshot_retention_limit": 7},
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input(
        [
            resource(
                "aws_elasticache_replication_group",
                "rg",
                {"snapshot_retention_limit": 0},
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []
