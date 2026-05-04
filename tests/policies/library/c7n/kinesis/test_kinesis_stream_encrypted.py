import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/kinesis/kinesis-stream-encrypted.yml"


def test_compliant():
    tf = tf_resource(
        "aws_kinesis_stream", "my_stream",
        '  name            = "my-stream"\n  encryption_type = "KMS"\n  kms_key_id      = "arn:aws:kms:us-east-1:123456789012:key/abc"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_kinesis_stream", "my_stream",
        '  name            = "my-stream"\n  encryption_type = "NONE"\n',
    )
    assert c7n_violations(POLICY, tf) != []
