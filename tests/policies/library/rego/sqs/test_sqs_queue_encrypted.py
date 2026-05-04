import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/sqs/sqs-queue-encrypted.rego"
)


def test_compliant_with_kms():
    inp = rego_input(
        [
            resource(
                "aws_sqs_queue",
                "queue",
                {
                    "kms_master_key_id": "arn:aws:kms:us-east-1:123:key/my-key",
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_with_sse():
    inp = rego_input(
        [
            resource(
                "aws_sqs_queue",
                "queue",
                {
                    "sqs_managed_sse_enabled": True,
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_sqs_queue", "queue", {})])
    assert eval_rego_policy(POLICY, inp) != []
