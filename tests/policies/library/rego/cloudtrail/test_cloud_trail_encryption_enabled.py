import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudtrail/cloud-trail-encryption-enabled.rego"


def test_compliant():
    attrs = {"kms_key_id": "arn:aws:kms:us-east-1:123:key/abc"}
    inp = rego_input([resource("aws_cloudtrail", "my_trail", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_cloudtrail", "my_trail", {})])
    assert eval_rego_policy(POLICY, inp) != []
