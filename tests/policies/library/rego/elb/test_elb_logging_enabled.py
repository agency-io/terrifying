import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/elb-logging-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_lb", "my_lb", {
        "access_logs": [{"bucket": "my-bucket", "enabled": True}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_access_logs():
    inp = rego_input([resource("aws_lb", "my_lb", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_access_logs_disabled():
    inp = rego_input([resource("aws_lb", "my_lb", {
        "access_logs": [{"bucket": "my-bucket", "enabled": False}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_alb_ignored():
    inp = rego_input([resource("aws_elb", "classic_lb", {})])
    assert eval_rego_policy(POLICY, inp) == []
