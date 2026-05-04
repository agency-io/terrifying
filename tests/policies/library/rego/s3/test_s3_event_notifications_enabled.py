import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/s3/s3-event-notifications-enabled.rego"
)


def test_compliant_with_topic():
    inp = rego_input(
        [
            resource(
                "aws_s3_bucket",
                "bucket",
                {
                    "topic": [
                        {
                            "topic_arn": "arn:aws:sns:us-east-1:123:topic",
                            "events": ["s3:ObjectCreated:*"],
                        }
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_s3_bucket", "bucket", {})])
    assert eval_rego_policy(POLICY, inp) != []
