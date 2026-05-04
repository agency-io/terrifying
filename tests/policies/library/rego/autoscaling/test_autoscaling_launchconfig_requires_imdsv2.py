import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/autoscaling/autoscaling-launchconfig-requires-imdsv2.rego"


def test_compliant():
    attrs = {"metadata_options": [{"http_tokens": "required"}]}
    inp = rego_input([resource("aws_launch_configuration", "my_lc", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_optional():
    attrs = {"metadata_options": [{"http_tokens": "optional"}]}
    inp = rego_input([resource("aws_launch_configuration", "my_lc", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_metadata_options():
    inp = rego_input([resource("aws_launch_configuration", "my_lc", {})])
    assert eval_rego_policy(POLICY, inp) != []
