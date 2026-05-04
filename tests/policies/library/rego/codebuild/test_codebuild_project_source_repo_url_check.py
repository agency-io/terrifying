import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/codebuild/codebuild-project-source-repo-url-check.rego"


def test_compliant():
    attrs = {"source": [{"type": "GITHUB", "location": "https://github.com/myorg/myrepo.git"}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_embedded_credentials():
    attrs = {"source": [{"type": "GITHUB", "location": "https://user:pass@github.com/myorg/myrepo.git"}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) != []
