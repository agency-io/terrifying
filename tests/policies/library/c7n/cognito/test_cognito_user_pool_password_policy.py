import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cognito/cognito-user-pool-password-policy.yml"

STRONG = '  password_policy {\n    minimum_length = 14\n    require_uppercase = true\n    require_lowercase = true\n    require_numbers = true\n    require_symbols = true\n  }\n'
WEAK = '  password_policy {\n    minimum_length = 8\n    require_uppercase = false\n    require_lowercase = true\n    require_numbers = true\n    require_symbols = true\n  }\n'


def test_compliant():
    tf = tf_resource("aws_cognito_user_pool", "pool", STRONG)
    assert c7n_violations(POLICY, tf) == []


def test_violation_short_length():
    tf = tf_resource("aws_cognito_user_pool", "pool", WEAK)
    assert c7n_violations(POLICY, tf) != []
