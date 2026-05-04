import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/redshift/redshift-default-admin-check.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_redshift_cluster", "cluster", '  master_username = "myclusteradmin"\n'
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_awsuser():
    tf = tf_resource(
        "aws_redshift_cluster", "cluster", '  master_username = "awsuser"\n'
    )
    assert c7n_violations(POLICY, tf) != []


def test_violation_admin():
    tf = tf_resource("aws_redshift_cluster", "cluster", '  master_username = "admin"\n')
    assert c7n_violations(POLICY, tf) != []
