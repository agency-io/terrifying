import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/iam/iam-user-group-membership-check.rego"
)


def test_compliant_with_group():
    inp = rego_input([resource("aws_iam_user", "my_user", {"groups": ["admins"]})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_groups():
    inp = rego_input([resource("aws_iam_user", "my_user", {"groups": []})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_missing_groups():
    inp = rego_input([resource("aws_iam_user", "my_user", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_iam_user_ignored():
    inp = rego_input([resource("aws_iam_role", "my_role", {})])
    assert eval_rego_policy(POLICY, inp) == []
