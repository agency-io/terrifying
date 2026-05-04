import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/codebuild/codebuild-project-envvar-awscred-check.rego"


def test_compliant():
    attrs = {"environment": [{"environment_variable": [{"name": "MY_VAR", "value": "foo", "type": "PLAINTEXT"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_access_key():
    attrs = {"environment": [{"environment_variable": [{"name": "AWS_ACCESS_KEY_ID", "value": "AKIA...", "type": "PLAINTEXT"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_compliant_secrets_manager():
    attrs = {"environment": [{"environment_variable": [{"name": "AWS_ACCESS_KEY_ID", "value": "arn:...", "type": "SECRETS_MANAGER"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []
