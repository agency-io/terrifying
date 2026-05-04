import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/vpc-default-security-group-closed.yml"

CLOSED = '  name = "default"\n'
OPEN = '  name = "default"\n  ingress {\n    from_port = 0\n    to_port = 0\n    protocol = "-1"\n    self = true\n  }\n'


def test_compliant():
    assert c7n_violations(POLICY, tf_resource("aws_security_group", "sg", CLOSED)) == []


def test_violation():
    assert c7n_violations(POLICY, tf_resource("aws_security_group", "sg", OPEN)) != []
