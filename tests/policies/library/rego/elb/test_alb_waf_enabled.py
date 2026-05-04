import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/alb-waf-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_lb", "my_alb", {"web_acl_arn": "arn:aws:wafv2:us-east-1:123456789012:regional/webacl/example/abc123"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_waf():
    inp = rego_input([resource("aws_lb", "my_alb", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_alb_ignored():
    inp = rego_input([resource("aws_elb", "classic_lb", {})])
    assert eval_rego_policy(POLICY, inp) == []
