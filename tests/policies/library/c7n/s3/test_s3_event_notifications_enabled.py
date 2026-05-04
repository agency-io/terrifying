import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-event-notifications-enabled.yml"


def test_compliant_no_notification_resource():
    # Policy targets aws_s3_bucket_notification. A plain bucket has no violations.
    tf = tf_resource("aws_s3_bucket", "bucket", '  bucket = "my-bucket"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation_notification_resource_exists():
    # The notification resource existing is matched by empty filters.
    tf = tf_resource(
        "aws_s3_bucket_notification", "notif",
        '  bucket = "my-bucket"\n',
    )
    assert c7n_violations(POLICY, tf) != []
