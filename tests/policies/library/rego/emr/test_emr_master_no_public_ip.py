import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/emr/emr-master-no-public-ip.rego"


def test_compliant_with_subnet():
    inp = rego_input([resource("aws_emr_cluster", "my_cluster", {
        "ec2_attributes": [{"subnet_id": "subnet-abc123"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_ec2_attributes():
    inp = rego_input([resource("aws_emr_cluster", "my_cluster", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_subnet():
    inp = rego_input([resource("aws_emr_cluster", "my_cluster", {
        "ec2_attributes": [{"availability_zone": "us-east-1a"}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_emr_ignored():
    inp = rego_input([resource("aws_instance", "my_ec2", {})])
    assert eval_rego_policy(POLICY, inp) == []
