import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/alb-http-to-https-redirection-check.rego"


def test_compliant_https_redirect():
    inp = rego_input([resource("aws_lb_listener", "my_listener", {
        "protocol": "HTTP",
        "default_action": [{"type": "redirect", "redirect": [{"protocol": "HTTPS"}]}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_https_listener():
    inp = rego_input([resource("aws_lb_listener", "my_listener", {
        "protocol": "HTTPS",
        "default_action": [{"type": "forward"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_http_no_redirect():
    inp = rego_input([resource("aws_lb_listener", "my_listener", {
        "protocol": "HTTP",
        "default_action": [{"type": "forward"}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_listener_ignored():
    inp = rego_input([resource("aws_lb", "my_alb", {"protocol": "HTTP"})])
    assert eval_rego_policy(POLICY, inp) == []
