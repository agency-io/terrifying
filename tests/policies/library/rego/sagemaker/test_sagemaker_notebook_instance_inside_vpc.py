import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/sagemaker/sagemaker-notebook-instance-inside-vpc.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_sagemaker_notebook_instance",
                "nb",
                {
                    "subnet_id": "subnet-12345",
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_sagemaker_notebook_instance", "nb", {})])
    assert eval_rego_policy(POLICY, inp) != []
