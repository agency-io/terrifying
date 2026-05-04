import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/ec2-transit-gateway-auto-vpc-attach-disabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_ec2_transit_gateway", "tgw", {"auto_accept_shared_attachments": "disable"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_ec2_transit_gateway", "tgw", {"auto_accept_shared_attachments": "enable"})])
    assert eval_rego_policy(POLICY, inp) != []
