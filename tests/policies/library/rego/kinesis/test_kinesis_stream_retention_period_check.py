import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/kinesis/kinesis-stream-retention-period-check.rego"


def test_compliant_168_hours():
    inp = rego_input([resource("aws_kinesis_stream", "my_stream", {"retention_period": 168})])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_more_than_168():
    inp = rego_input([resource("aws_kinesis_stream", "my_stream", {"retention_period": 336})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_24_hours():
    inp = rego_input([resource("aws_kinesis_stream", "my_stream", {"retention_period": 24})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_167_hours():
    inp = rego_input([resource("aws_kinesis_stream", "my_stream", {"retention_period": 167})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_kinesis_ignored():
    inp = rego_input([resource("aws_sqs_queue", "my_queue", {"retention_period": 24})])
    assert eval_rego_policy(POLICY, inp) == []
