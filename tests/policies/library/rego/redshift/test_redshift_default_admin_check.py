import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/redshift/redshift-default-admin-check.rego"
)


def test_compliant():
    inp = rego_input(
        [resource("aws_redshift_cluster", "cluster", {"master_username": "mydbadmin"})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_admin():
    inp = rego_input(
        [resource("aws_redshift_cluster", "cluster", {"master_username": "admin"})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_awsuser():
    inp = rego_input(
        [resource("aws_redshift_cluster", "cluster", {"master_username": "awsuser"})]
    )
    assert eval_rego_policy(POLICY, inp) != []
