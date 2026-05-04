import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/rds/rds-enhanced-monitoring-enabled.yml"


def test_compliant():
    tf = tf_resource("aws_db_instance", "db", '  monitoring_interval = 60\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation_zero():
    tf = tf_resource("aws_db_instance", "db", '  monitoring_interval = 0\n')
    assert c7n_violations(POLICY, tf) != []
