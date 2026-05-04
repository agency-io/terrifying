import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/codebuild/codebuild-project-logging-enabled.rego"


def test_compliant_cloudwatch():
    attrs = {"logs_config": [{"cloudwatch_logs": [{"status": "ENABLED"}], "s3_logs": [{"status": "DISABLED"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_s3():
    attrs = {"logs_config": [{"cloudwatch_logs": [{"status": "DISABLED"}], "s3_logs": [{"status": "ENABLED", "location": "my-bucket/logs"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    attrs = {"logs_config": [{"cloudwatch_logs": [{"status": "DISABLED"}], "s3_logs": [{"status": "DISABLED"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) != []
