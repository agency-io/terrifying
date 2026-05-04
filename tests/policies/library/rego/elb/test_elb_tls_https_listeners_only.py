import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/elb-tls-https-listeners-only.rego"


def test_compliant_https():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "HTTPS", "instance_protocol": "HTTPS", "lb_port": 443, "instance_port": 443}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_ssl():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "SSL", "instance_protocol": "SSL", "lb_port": 443, "instance_port": 443}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_http():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "HTTP", "instance_protocol": "HTTP", "lb_port": 80, "instance_port": 80}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_tcp():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "TCP", "instance_protocol": "TCP", "lb_port": 8080, "instance_port": 8080}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_classic_elb_ignored():
    inp = rego_input([resource("aws_lb", "my_alb", {
        "listener": [{"lb_protocol": "HTTP"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []
