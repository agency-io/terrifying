import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/lambda/lambda-inside-vpc.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_lambda_function",
        "my_fn",
        '  function_name = "my-function"\n  runtime       = "python3.11"\n  role          = "arn:aws:iam::123456789012:role/my-role"\n  handler       = "index.handler"\n  vpc_config {\n    subnet_ids         = ["subnet-abc"]\n    security_group_ids = ["sg-abc"]\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_lambda_function",
        "my_fn",
        '  function_name = "my-function"\n  runtime       = "python3.11"\n  role          = "arn:aws:iam::123456789012:role/my-role"\n  handler       = "index.handler"\n',
    )
    assert c7n_violations(POLICY, tf) != []
