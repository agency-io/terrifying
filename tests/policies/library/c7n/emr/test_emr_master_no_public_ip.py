import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/emr/emr-master-no-public-ip.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_emr_cluster",
        "my_cluster",
        '  ec2_attributes {\n    subnet_id = "subnet-abc123"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_emr_cluster",
        "my_cluster",
        '  name = "my-cluster"\n  release_label = "emr-6.4.0"\n',
    )
    assert c7n_violations(POLICY, tf) != []
