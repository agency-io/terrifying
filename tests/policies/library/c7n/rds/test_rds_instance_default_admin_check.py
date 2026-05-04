import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/rds/rds-instance-default-admin-check.yml"


def test_compliant():
    tf = tf_resource("aws_db_instance", "db", '  username = "mydbadmin"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation_admin():
    tf = tf_resource("aws_db_instance", "db", '  username = "admin"\n')
    assert c7n_violations(POLICY, tf) != []


def test_violation_master():
    tf = tf_resource("aws_db_instance", "db", '  username = "master"\n')
    assert c7n_violations(POLICY, tf) != []
