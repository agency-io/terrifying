import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/no-unrestricted-route-to-igw.rego"


def test_compliant():
    inp = rego_input([resource("aws_route", "rt", {"destination_cidr_block": "0.0.0.0/0", "gateway_id": "nat-12345"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_route", "rt", {"destination_cidr_block": "0.0.0.0/0", "gateway_id": "igw-12345"})])
    assert eval_rego_policy(POLICY, inp) != []
