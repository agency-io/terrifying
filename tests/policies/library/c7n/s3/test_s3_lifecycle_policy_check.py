import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-lifecycle-policy-check.yml"


def test_compliant_no_lifecycle_resource():
    # Policy targets aws_s3_bucket_lifecycle_configuration. A plain bucket has no violations.
    tf = tf_resource("aws_s3_bucket", "bucket", '  bucket = "my-bucket"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation_lifecycle_resource_exists():
    # The lifecycle configuration resource existing is matched by empty filters.
    tf = tf_resource(
        "aws_s3_bucket_lifecycle_configuration", "lc",
        '  bucket = "my-bucket"\n',
    )
    assert c7n_violations(POLICY, tf) != []
