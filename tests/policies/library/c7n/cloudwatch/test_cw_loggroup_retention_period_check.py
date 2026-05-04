import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudwatch/cw-loggroup-retention-period-check.yml"


def test_compliant():
    tf = tf_resource("aws_cloudwatch_log_group", "lg", '  retention_in_days = 90\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_cloudwatch_log_group", "lg", '  name = "my-log-group"\n')
    assert c7n_violations(POLICY, tf) != []
