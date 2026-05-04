import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/vpc-default-security-group-closed.rego"


def test_compliant():
    inp = rego_input([resource("aws_default_security_group", "default", {"ingress": [], "egress": []})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_ingress():
    inp = rego_input([resource("aws_default_security_group", "default", {"ingress": [{"from_port": 0, "to_port": 0, "protocol": "-1", "cidr_blocks": ["0.0.0.0/0"]}], "egress": []})])
    assert eval_rego_policy(POLICY, inp) != []
