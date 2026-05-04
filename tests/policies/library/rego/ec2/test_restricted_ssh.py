import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/restricted-ssh.rego"


def test_compliant():
    inp = rego_input([resource("aws_security_group", "sg", {"ingress": [{"from_port": 22, "to_port": 22, "cidr_blocks": ["10.0.0.0/8"], "ipv6_cidr_blocks": []}]})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_security_group", "sg", {"ingress": [{"from_port": 0, "to_port": 65535, "cidr_blocks": ["0.0.0.0/0"], "ipv6_cidr_blocks": []}]})])
    assert eval_rego_policy(POLICY, inp) != []
