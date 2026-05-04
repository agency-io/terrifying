import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/elbv2-predefined-security-policy-ssl-check.rego"


def test_compliant_recommended_policy():
    inp = rego_input([resource("aws_lb_listener", "my_listener", {
        "protocol": "HTTPS",
        "ssl_policy": "ELBSecurityPolicy-TLS13-1-2-2021-06",
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_http_listener():
    inp = rego_input([resource("aws_lb_listener", "my_listener", {
        "protocol": "HTTP",
        "ssl_policy": "ELBSecurityPolicy-2016-08",
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_outdated_policy():
    inp = rego_input([resource("aws_lb_listener", "my_listener", {
        "protocol": "HTTPS",
        "ssl_policy": "ELBSecurityPolicy-2016-08",
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_listener_ignored():
    inp = rego_input([resource("aws_lb", "my_alb", {
        "protocol": "HTTPS",
        "ssl_policy": "ELBSecurityPolicy-2016-08",
    })])
    assert eval_rego_policy(POLICY, inp) == []
