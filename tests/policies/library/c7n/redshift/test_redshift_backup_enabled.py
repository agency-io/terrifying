import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/redshift/redshift-backup-enabled.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_redshift_cluster", "cluster", "  automated_snapshot_retention_period = 7\n"
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_redshift_cluster", "cluster", "  automated_snapshot_retention_period = 0\n"
    )
    assert c7n_violations(POLICY, tf) != []
