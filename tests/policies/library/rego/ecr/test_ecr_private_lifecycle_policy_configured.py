import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ecr/ecr-private-lifecycle-policy-configured.rego"


def test_compliant():
    repo = resource("aws_ecr_repository", "repo", {"name": "my-repo"})
    lp = resource("aws_ecr_lifecycle_policy", "lp", {"repository": "my-repo"})
    inp = rego_input([repo, lp])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_ecr_repository", "repo", {"name": "my-repo"})])
    assert eval_rego_policy(POLICY, inp) != []
