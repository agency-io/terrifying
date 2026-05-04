import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/no-unrestricted-route-to-igw.yml"

SAFE = '  vpc_id = "vpc-123"\n  route {\n    cidr_block = "10.0.0.0/8"\n    transit_gateway_id = "tgw-abc"\n  }\n'
OPEN = '  vpc_id = "vpc-123"\n  route {\n    cidr_block = "0.0.0.0/0"\n    gateway_id = "igw-abc"\n  }\n'


def test_compliant():
    assert c7n_violations(POLICY, tf_resource("aws_route_table", "rt", SAFE)) == []


def test_violation():
    assert c7n_violations(POLICY, tf_resource("aws_route_table", "rt", OPEN)) != []
