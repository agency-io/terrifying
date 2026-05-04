import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/elb-tls-https-listeners-only.yml"


def test_compliant():
    tf = tf_resource(
        "aws_lb_listener", "my_listener",
        '  protocol = "HTTPS"\n  load_balancer_arn = "arn:aws:elasticloadbalancing:::loadbalancer/app/test/abc"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_lb_listener", "my_listener",
        '  protocol = "HTTP"\n  load_balancer_arn = "arn:aws:elasticloadbalancing:::loadbalancer/app/test/abc"\n',
    )
    assert c7n_violations(POLICY, tf) != []
