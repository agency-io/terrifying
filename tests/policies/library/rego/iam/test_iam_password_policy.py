import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/iam/iam-password-policy.rego"
)

COMPLIANT_ATTRS = {
    "minimum_password_length": 14,
    "require_uppercase_characters": True,
    "require_lowercase_characters": True,
    "require_symbols": True,
    "require_numbers": True,
}


def test_compliant():
    inp = rego_input(
        [resource("aws_iam_account_password_policy", "policy", COMPLIANT_ATTRS)]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_short_password():
    attrs = {**COMPLIANT_ATTRS, "minimum_password_length": 8}
    inp = rego_input([resource("aws_iam_account_password_policy", "policy", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_uppercase():
    attrs = {**COMPLIANT_ATTRS, "require_uppercase_characters": False}
    inp = rego_input([resource("aws_iam_account_password_policy", "policy", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_lowercase():
    attrs = {**COMPLIANT_ATTRS, "require_lowercase_characters": False}
    inp = rego_input([resource("aws_iam_account_password_policy", "policy", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_symbols():
    attrs = {**COMPLIANT_ATTRS, "require_symbols": False}
    inp = rego_input([resource("aws_iam_account_password_policy", "policy", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_numbers():
    attrs = {**COMPLIANT_ATTRS, "require_numbers": False}
    inp = rego_input([resource("aws_iam_account_password_policy", "policy", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_password_policy_ignored():
    inp = rego_input([resource("aws_iam_user", "my_user", {})])
    assert eval_rego_policy(POLICY, inp) == []
