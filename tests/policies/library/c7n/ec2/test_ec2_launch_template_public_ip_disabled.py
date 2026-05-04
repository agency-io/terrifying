import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ec2/ec2-launch-template-public-ip-disabled.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_launch_template",
        "lt",
        "  network_interfaces {\n    associate_public_ip_address = false\n  }\n",
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_launch_template",
        "lt",
        "  network_interfaces {\n    associate_public_ip_address = true\n  }\n",
    )
    assert c7n_violations(POLICY, tf) != []
