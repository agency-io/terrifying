import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/codebuild/codebuild-project-s3-logs-encrypted.rego"
)


def test_compliant_s3_encrypted():
    attrs = {
        "logs_config": [
            {"s3_logs": [{"status": "ENABLED", "encryption_disabled": False}]}
        ]
    }
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_s3_disabled():
    attrs = {"logs_config": [{"s3_logs": [{"status": "DISABLED"}]}]}
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    attrs = {
        "logs_config": [
            {"s3_logs": [{"status": "ENABLED", "encryption_disabled": True}]}
        ]
    }
    inp = rego_input([resource("aws_codebuild_project", "my_project", attrs)])
    assert eval_rego_policy(POLICY, inp) != []
