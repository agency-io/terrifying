import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-access-point-public-access-blocks.rego"


def test_compliant():
    inp = rego_input([resource("aws_s3_access_point", "ap", {
        "public_access_block_configuration": [{
            "block_public_acls": True,
            "block_public_policy": True,
            "ignore_public_acls": True,
            "restrict_public_buckets": True,
        }],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_s3_access_point", "ap", {
        "public_access_block_configuration": [{
            "block_public_acls": False,
            "block_public_policy": True,
            "ignore_public_acls": True,
            "restrict_public_buckets": True,
        }],
    })])
    assert eval_rego_policy(POLICY, inp) != []
