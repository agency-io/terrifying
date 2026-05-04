import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/elbv2-predefined-security-policy-ssl-check.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_lb_listener",
        "my_listener",
        '  protocol = "HTTPS"\n  ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"\n  load_balancer_arn = "arn:aws:elasticloadbalancing:::loadbalancer/app/test/abc"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_lb_listener",
        "my_listener",
        '  protocol = "HTTPS"\n  ssl_policy = "ELBSecurityPolicy-2016-08"\n  load_balancer_arn = "arn:aws:elasticloadbalancing:::loadbalancer/app/test/abc"\n',
    )
    assert c7n_violations(POLICY, tf) != []
