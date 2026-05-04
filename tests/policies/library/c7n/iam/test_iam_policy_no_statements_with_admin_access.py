import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/iam/iam-policy-no-statements-with-admin-access.yml"


def test_compliant():
    tf = tf_resource(
        "aws_iam_policy", "my_policy",
        '  name   = "my-policy"\n  policy = jsonencode({\n    Version = "2012-10-17"\n    Statement = [{\n      Effect   = "Allow"\n      Action   = ["s3:GetObject"]\n      Resource = "*"\n    }]\n  })\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_iam_policy", "my_policy",
        '  name   = "my-admin-policy"\n  policy = "{\\\"Version\\\":\\\"2012-10-17\\\",\\\"Statement\\\":[{\\\"Effect\\\":\\\"Allow\\\",\\\"Action\\\": \\\"*\\\",\\\"Resource\\\":\\\"*\\\"}]}"\n',
    )
    assert c7n_violations(POLICY, tf) != []
