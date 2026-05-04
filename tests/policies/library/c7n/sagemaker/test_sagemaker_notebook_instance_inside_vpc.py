import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/sagemaker/sagemaker-notebook-instance-inside-vpc.yml"


def test_compliant():
    tf = tf_resource(
        "aws_sagemaker_notebook_instance", "nb",
        '  name      = "my-notebook"\n  subnet_id = "subnet-12345"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_sagemaker_notebook_instance", "nb",
        '  name = "my-notebook"\n',
    )
    assert c7n_violations(POLICY, tf) != []
