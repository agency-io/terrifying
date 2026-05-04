import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/kms/kms-key-policy-no-public-access.yml"


def test_compliant():
    tf = tf_resource(
        "aws_kms_key", "my_key",
        '  policy = "{\\\"Version\\\":\\\"2012-10-17\\\",\\\"Statement\\\":[{\\\"Effect\\\":\\\"Allow\\\",\\\"Principal\\\":{\\\"AWS\\\":\\\"arn:aws:iam::123456789012:root\\\"},\\\"Action\\\":\\\"kms:*\\\",\\\"Resource\\\":\\\"*\\\"}]}"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_kms_key", "my_key",
        '  policy = "{\\\"Version\\\":\\\"2012-10-17\\\",\\\"Statement\\\":[{\\\"Effect\\\":\\\"Allow\\\",\\\"Principal\\\": \\\"*\\\",\\\"Action\\\":\\\"kms:*\\\",\\\"Resource\\\":\\\"*\\\"}]}"\n',
    )
    assert c7n_violations(POLICY, tf) != []
