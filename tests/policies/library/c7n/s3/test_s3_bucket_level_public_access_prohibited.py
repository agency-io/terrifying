import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/s3/s3-bucket-level-public-access-prohibited.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_s3_bucket_public_access_block",
        "block",
        "  block_public_acls       = true\n  block_public_policy     = true\n  ignore_public_acls      = true\n  restrict_public_buckets = true\n",
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_s3_bucket_public_access_block",
        "block",
        "  block_public_acls = false\n",
    )
    assert c7n_violations(POLICY, tf) != []
