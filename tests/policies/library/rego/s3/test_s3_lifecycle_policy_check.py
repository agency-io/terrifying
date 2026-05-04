import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-lifecycle-policy-check.rego"


def test_compliant():
    inp = rego_input([resource("aws_s3_bucket", "bucket", {
        "lifecycle_rule": [{"enabled": True, "expiration": [{"days": 90}]}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_s3_bucket", "bucket", {"lifecycle_rule": []})])
    assert eval_rego_policy(POLICY, inp) != []
