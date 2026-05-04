import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ec2/ec2-imdsv2-check.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_instance",
                "web",
                {"metadata_options": [{"http_tokens": "required"}]},
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_metadata_options():
    inp = rego_input([resource("aws_instance", "web", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_optional_tokens():
    inp = rego_input(
        [
            resource(
                "aws_instance",
                "web",
                {"metadata_options": [{"http_tokens": "optional"}]},
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []
