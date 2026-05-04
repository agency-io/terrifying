import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/codebuild/codebuild-project-envvar-awscred-check.yml"


def test_compliant():
    tf = tf_resource(
        "aws_codebuild_project", "proj",
        '  environment {\n    environment_variable {\n      name  = "MY_VAR"\n      value = "my-value"\n      type  = "PARAMETER_STORE"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_codebuild_project", "proj",
        '  environment {\n    environment_variable {\n      name  = "AWS_ACCESS_KEY_ID"\n      value = "AKIAIOSFODNN7EXAMPLE"\n      type  = "PLAINTEXT"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
