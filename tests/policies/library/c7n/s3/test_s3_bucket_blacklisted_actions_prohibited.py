import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/s3/s3-bucket-blacklisted-actions-prohibited.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_s3_bucket_policy",
        "policy",
        '  policy = jsonencode({"Statement":[{"Effect":"Deny","Principal":"*","Action":"s3:*"}]})\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_s3_bucket_policy",
        "policy",
        '  policy = jsonencode({"Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject"}]})\n',
    )
    assert c7n_violations(POLICY, tf) != []
