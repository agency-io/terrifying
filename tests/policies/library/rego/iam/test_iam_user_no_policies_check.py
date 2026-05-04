import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/iam/iam-user-no-policies-check.rego"


def test_compliant_no_inline_policy():
    inp = rego_input([resource("aws_iam_user", "my_user", {"name": "my_user"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_inline_policy():
    inp = rego_input([resource("aws_iam_user_policy", "my_inline", {
        "name": "my-policy",
        "user": "my_user",
        "policy": '{"Version":"2012-10-17","Statement":[]}',
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_iam_user_policy_ignored():
    inp = rego_input([resource("aws_iam_policy", "my_managed", {
        "policy": '{"Version":"2012-10-17","Statement":[]}',
    })])
    assert eval_rego_policy(POLICY, inp) == []
