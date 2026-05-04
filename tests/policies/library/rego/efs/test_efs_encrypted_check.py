import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/efs/efs-encrypted-check.rego"
)


def test_compliant():
    inp = rego_input([resource("aws_efs_file_system", "data", {"encrypted": True})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_efs_file_system", "data", {"encrypted": False})])
    assert eval_rego_policy(POLICY, inp) != []
