import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elasticache/elasticache-redis-cluster-automatic-backup-check.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_elasticache_replication_group",
        "main",
        '  replication_group_id    = "my-redis"\n  snapshot_retention_limit = 7\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_elasticache_replication_group",
        "main",
        '  replication_group_id    = "my-redis"\n  snapshot_retention_limit = 0\n',
    )
    assert c7n_violations(POLICY, tf) != []
