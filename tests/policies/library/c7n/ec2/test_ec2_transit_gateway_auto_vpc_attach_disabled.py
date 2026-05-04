import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/ec2-transit-gateway-auto-vpc-attach-disabled.yml"


def test_compliant():
    tf = tf_resource("aws_ec2_transit_gateway", "tgw", '  auto_accept_shared_attachments = "disable"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_ec2_transit_gateway", "tgw", '  auto_accept_shared_attachments = "enable"\n')
    assert c7n_violations(POLICY, tf) != []
