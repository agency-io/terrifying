import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudwatch/cw-loggroup-retention-period-check.rego"


def test_compliant():
    inp = rego_input([resource("aws_cloudwatch_log_group", "my_log_group", {"retention_in_days": 90})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_cloudwatch_log_group", "my_log_group", {})])
    assert eval_rego_policy(POLICY, inp) != []
