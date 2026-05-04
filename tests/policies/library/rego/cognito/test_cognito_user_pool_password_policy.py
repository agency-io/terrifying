import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cognito/cognito-user-pool-password-policy.rego"
)

STRONG_POLICY = [
    {
        "minimum_length": 14,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_symbols": True,
    }
]
WEAK_POLICY = [
    {
        "minimum_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_symbols": True,
    }
]


def test_compliant():
    inp = rego_input(
        [resource("aws_cognito_user_pool", "pool", {"password_policy": STRONG_POLICY})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_short_length():
    inp = rego_input(
        [resource("aws_cognito_user_pool", "pool", {"password_policy": WEAK_POLICY})]
    )
    assert eval_rego_policy(POLICY, inp) != []
