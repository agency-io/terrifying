import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/lambda/lambda-function-public-access-prohibited.yml"


def test_compliant():
    # A permission granted to a specific account principal is not a violation
    tf = tf_resource(
        "aws_lambda_permission", "my_permission",
        '  statement_id  = "AllowSpecificAccount"\n  action        = "lambda:InvokeFunction"\n  function_name = "my-function"\n  principal     = "123456789012"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    # A permission granted to wildcard principal (*) is a violation
    tf = tf_resource(
        "aws_lambda_permission", "my_permission",
        '  statement_id  = "AllowPublic"\n  action        = "lambda:InvokeFunction"\n  function_name = "my-function"\n  principal     = "*"\n',
    )
    assert c7n_violations(POLICY, tf) != []
