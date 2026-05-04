import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/dynamodb/dynamodb-autoscaling-enabled.rego"
)


def test_compliant_pay_per_request():
    inp = rego_input(
        [resource("aws_dynamodb_table", "tbl", {"billing_mode": "PAY_PER_REQUEST"})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_provisioned_no_autoscaling():
    inp = rego_input(
        [resource("aws_dynamodb_table", "tbl", {"billing_mode": "PROVISIONED"})]
    )
    assert eval_rego_policy(POLICY, inp) != []
