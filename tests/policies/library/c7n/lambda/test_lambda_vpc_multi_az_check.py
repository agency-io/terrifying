import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/lambda/lambda-vpc-multi-az-check.yml"


def test_compliant_multi_az():
    tf = tf_resource(
        "aws_lambda_function", "my_fn",
        '  function_name = "my-function"\n  runtime       = "python3.11"\n  role          = "arn:aws:iam::123456789012:role/my-role"\n  handler       = "index.handler"\n  vpc_config {\n    subnet_ids         = ["subnet-aaa", "subnet-bbb"]\n    security_group_ids = ["sg-abc"]\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_compliant_no_vpc():
    # Functions with no VPC config at all are not flagged (they are caught by lambda-inside-vpc)
    tf = tf_resource(
        "aws_lambda_function", "my_fn",
        '  function_name = "my-function"\n  runtime       = "python3.11"\n  role          = "arn:aws:iam::123456789012:role/my-role"\n  handler       = "index.handler"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_single_az():
    tf = tf_resource(
        "aws_lambda_function", "my_fn",
        '  function_name = "my-function"\n  runtime       = "python3.11"\n  role          = "arn:aws:iam::123456789012:role/my-role"\n  handler       = "index.handler"\n  vpc_config {\n    subnet_ids         = ["subnet-aaa"]\n    security_group_ids = ["sg-abc"]\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
