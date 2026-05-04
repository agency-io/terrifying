import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/restricted-common-ports.yml"

SAFE = '  ingress {\n    from_port = 3389\n    to_port = 3389\n    protocol = "tcp"\n    cidr_blocks = ["10.0.0.0/8"]\n  }\n'
OPEN = '  ingress {\n    from_port = 3306\n    to_port = 3306\n    protocol = "tcp"\n    cidr_blocks = ["0.0.0.0/0"]\n  }\n'


def test_compliant():
    assert c7n_violations(POLICY, tf_resource("aws_security_group", "sg", SAFE)) == []


def test_violation():
    assert c7n_violations(POLICY, tf_resource("aws_security_group", "sg", OPEN)) != []
