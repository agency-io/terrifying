import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ec2/subnet-auto-assign-public-ip-disabled.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_subnet",
        "sub",
        '  vpc_id = "vpc-123"\n  cidr_block = "10.0.1.0/24"\n  map_public_ip_on_launch = false\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_subnet",
        "sub",
        '  vpc_id = "vpc-123"\n  cidr_block = "10.0.1.0/24"\n  map_public_ip_on_launch = true\n',
    )
    assert c7n_violations(POLICY, tf) != []
