import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/elb-acm-certificate-required.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_elb",
        "my_elb",
        '  listener {\n    instance_port = 443\n    instance_protocol = "HTTPS"\n    lb_port = 443\n    lb_protocol = "HTTPS"\n    ssl_certificate_id = "arn:aws:acm:us-east-1:123456789012:certificate/abc"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_elb",
        "my_elb",
        '  listener {\n    instance_port = 443\n    instance_protocol = "HTTPS"\n    lb_port = 443\n    lb_protocol = "HTTPS"\n    ssl_certificate_id = "arn:aws:iam::123456789012:server-certificate/my-cert"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
