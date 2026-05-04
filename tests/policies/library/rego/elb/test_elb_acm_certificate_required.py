import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/elb-acm-certificate-required.rego"


def test_compliant_acm_cert():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "HTTPS", "ssl_certificate_id": "arn:aws:acm:us-east-1:123456789012:certificate/abc"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_http_listener():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "HTTP", "lb_port": 80, "instance_protocol": "HTTP", "instance_port": 80}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_non_acm_cert():
    inp = rego_input([resource("aws_elb", "classic_lb", {
        "listener": [{"lb_protocol": "HTTPS", "ssl_certificate_id": "arn:aws:iam::123456789012:server-certificate/my-cert"}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_classic_elb_ignored():
    inp = rego_input([resource("aws_lb", "my_alb", {
        "listener": [{"lb_protocol": "HTTPS", "ssl_certificate_id": "arn:aws:iam::123456789012:server-certificate/my-cert"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []
