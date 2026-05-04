import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ec2/nacl-no-unrestricted-ssh-rdp.yml"
)

SAFE = '  vpc_id = "vpc-123"\n  ingress {\n    protocol = "tcp"\n    rule_no = 100\n    action = "allow"\n    cidr_block = "10.0.0.0/8"\n    from_port = 22\n    to_port = 22\n  }\n'
OPEN_SSH = '  vpc_id = "vpc-123"\n  ingress {\n    protocol = "tcp"\n    rule_no = 100\n    action = "allow"\n    cidr_block = "0.0.0.0/0"\n    from_port = 22\n    to_port = 22\n  }\n'


def test_compliant():
    assert c7n_violations(POLICY, tf_resource("aws_network_acl", "nacl", SAFE)) == []


def test_violation():
    assert (
        c7n_violations(POLICY, tf_resource("aws_network_acl", "nacl", OPEN_SSH)) != []
    )
