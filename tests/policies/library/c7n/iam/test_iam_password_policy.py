import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/iam/iam-password-policy.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_iam_account_password_policy",
        "strict",
        "  minimum_password_length      = 14\n"
        "  require_symbols              = true\n"
        "  require_numbers              = true\n"
        "  require_uppercase_characters = true\n"
        "  require_lowercase_characters = true\n"
        "  max_password_age             = 90\n",
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_short_password():
    tf = tf_resource(
        "aws_iam_account_password_policy",
        "weak",
        "  minimum_password_length      = 8\n"
        "  require_symbols              = true\n"
        "  require_numbers              = true\n"
        "  require_uppercase_characters = true\n"
        "  require_lowercase_characters = true\n"
        "  max_password_age             = 90\n",
    )
    assert c7n_violations(POLICY, tf) != []


def test_violation_no_symbols():
    tf = tf_resource(
        "aws_iam_account_password_policy",
        "weak",
        "  minimum_password_length      = 14\n"
        "  require_symbols              = false\n"
        "  require_numbers              = true\n"
        "  require_uppercase_characters = true\n"
        "  require_lowercase_characters = true\n"
        "  max_password_age             = 90\n",
    )
    assert c7n_violations(POLICY, tf) != []
