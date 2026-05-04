import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-bucket-logging-enabled.yml"


def test_compliant():
    # Policy checks for existence of aws_s3_bucket_logging resource (empty filters).
    tf = tf_resource(
        "aws_s3_bucket_logging", "logs",
        '  bucket        = "my-bucket"\n  target_bucket = "my-log-bucket"\n  target_prefix = "logs/"\n',
    )
    assert c7n_violations(POLICY, tf) != []


def test_violation():
    # aws_s3_bucket without logging resource — policy does not flag aws_s3_bucket itself
    tf = tf_resource("aws_s3_bucket", "bucket", '  bucket = "my-bucket"\n')
    assert c7n_violations(POLICY, tf) == []
