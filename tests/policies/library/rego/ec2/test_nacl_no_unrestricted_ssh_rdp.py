import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ec2/nacl-no-unrestricted-ssh-rdp.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_network_acl_rule",
                "rule",
                {
                    "rule_action": "allow",
                    "egress": False,
                    "from_port": 22,
                    "to_port": 22,
                    "cidr_block": "10.0.0.0/8",
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_ssh():
    inp = rego_input(
        [
            resource(
                "aws_network_acl_rule",
                "rule",
                {
                    "rule_action": "allow",
                    "egress": False,
                    "from_port": 22,
                    "to_port": 22,
                    "cidr_block": "0.0.0.0/0",
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []
