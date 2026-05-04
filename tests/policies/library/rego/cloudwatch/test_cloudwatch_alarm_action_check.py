import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudwatch/cloudwatch-alarm-action-check.rego"


def test_compliant_alarm_action():
    attrs = {"alarm_actions": ["arn:aws:sns:us-east-1:123:my-topic"], "ok_actions": [], "insufficient_data_actions": []}
    inp = rego_input([resource("aws_cloudwatch_metric_alarm", "my_alarm", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_actions():
    attrs = {"alarm_actions": [], "ok_actions": [], "insufficient_data_actions": []}
    inp = rego_input([resource("aws_cloudwatch_metric_alarm", "my_alarm", attrs)])
    assert eval_rego_policy(POLICY, inp) != []
