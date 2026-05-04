import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/kms/cmk-backing-key-rotation-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_kms_key", "my_key", {"enable_key_rotation": True})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_rotation_disabled():
    inp = rego_input([resource("aws_kms_key", "my_key", {"enable_key_rotation": False})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_rotation_missing():
    inp = rego_input([resource("aws_kms_key", "my_key", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_kms_ignored():
    inp = rego_input([resource("aws_s3_bucket", "my_bucket", {})])
    assert eval_rego_policy(POLICY, inp) == []
