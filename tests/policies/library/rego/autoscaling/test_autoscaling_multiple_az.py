import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/autoscaling/autoscaling-multiple-az.rego"
)


def test_compliant():
    attrs = {"availability_zones": ["us-east-1a", "us-east-1b"]}
    inp = rego_input([resource("aws_autoscaling_group", "my_asg", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_single_az():
    attrs = {"availability_zones": ["us-east-1a"]}
    inp = rego_input([resource("aws_autoscaling_group", "my_asg", attrs)])
    assert eval_rego_policy(POLICY, inp) != []
