import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/kinesis/kinesis-stream-encrypted.rego"
)


def test_compliant_kms():
    inp = rego_input(
        [resource("aws_kinesis_stream", "my_stream", {"encryption_type": "KMS"})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_none():
    inp = rego_input(
        [resource("aws_kinesis_stream", "my_stream", {"encryption_type": "NONE"})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_missing():
    inp = rego_input([resource("aws_kinesis_stream", "my_stream", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_kinesis_ignored():
    inp = rego_input(
        [resource("aws_sqs_queue", "my_queue", {"encryption_type": "NONE"})]
    )
    assert eval_rego_policy(POLICY, inp) == []
