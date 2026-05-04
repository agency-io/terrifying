import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cloudwatch/cloudwatch-alarm-action-check.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_cloudwatch_metric_alarm",
        "alarm",
        '  alarm_actions = ["arn:aws:sns:us-east-1:123:my-topic"]\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_cloudwatch_metric_alarm", "alarm", '  alarm_name = "my-alarm"\n'
    )
    assert c7n_violations(POLICY, tf) != []
