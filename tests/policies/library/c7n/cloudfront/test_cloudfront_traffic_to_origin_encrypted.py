import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cloudfront/cloudfront-traffic-to-origin-encrypted.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_cloudfront_distribution",
        "dist",
        '  origin {\n    custom_origin_config {\n      origin_protocol_policy = "https-only"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_cloudfront_distribution",
        "dist",
        '  origin {\n    custom_origin_config {\n      origin_protocol_policy = "http-only"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
