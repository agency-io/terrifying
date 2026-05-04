import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-default-encryption-kms.yml"


def test_compliant():
    tf = tf_resource(
        "aws_s3_bucket_server_side_encryption_configuration", "sse",
        '  bucket = "my-bucket"\n  rule {\n    apply_server_side_encryption_by_default {\n      sse_algorithm = "aws:kms"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_aes256():
    tf = tf_resource(
        "aws_s3_bucket_server_side_encryption_configuration", "sse",
        '  bucket = "my-bucket"\n  rule {\n    apply_server_side_encryption_by_default {\n      sse_algorithm = "AES256"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
