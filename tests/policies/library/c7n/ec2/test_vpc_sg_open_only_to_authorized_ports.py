import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ec2/vpc-sg-open-only-to-authorized-ports.yml"
)

SAFE = '  ingress {\n    from_port = 443\n    to_port = 443\n    protocol = "tcp"\n    cidr_blocks = ["0.0.0.0/0"]\n  }\n'
OPEN = '  ingress {\n    from_port = 8080\n    to_port = 8080\n    protocol = "tcp"\n    cidr_blocks = ["0.0.0.0/0"]\n  }\n'


def test_compliant():
    assert c7n_violations(POLICY, tf_resource("aws_security_group", "sg", SAFE)) == []


def test_violation():
    assert c7n_violations(POLICY, tf_resource("aws_security_group", "sg", OPEN)) != []
