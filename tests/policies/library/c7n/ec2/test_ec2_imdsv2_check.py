import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ec2/ec2-imdsv2-check.yml"


def test_compliant():
    tf = tf_resource("aws_instance", "inst", '  ami = "ami-123"\n  instance_type = "t3.micro"\n  metadata_options {\n    http_tokens = "required"\n  }\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_instance", "inst", '  ami = "ami-123"\n  instance_type = "t3.micro"\n  metadata_options {\n    http_tokens = "optional"\n  }\n')
    assert c7n_violations(POLICY, tf) != []
