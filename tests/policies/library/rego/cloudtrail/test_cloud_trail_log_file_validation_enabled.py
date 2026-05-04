import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudtrail/cloud-trail-log-file-validation-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_cloudtrail", "my_trail", {"enable_log_file_validation": True})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_cloudtrail", "my_trail", {"enable_log_file_validation": False})])
    assert eval_rego_policy(POLICY, inp) != []
