import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/codebuild/codebuild-project-source-repo-url-check.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_codebuild_project",
        "proj",
        '  source {\n    type     = "GITHUB"\n    location = "https://github.com/org/repo.git"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_codebuild_project",
        "proj",
        '  source {\n    type     = "GITHUB"\n    location = "https://user:token@github.com/org/repo.git"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
