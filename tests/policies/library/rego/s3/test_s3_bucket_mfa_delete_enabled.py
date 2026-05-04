import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/s3/s3-bucket-mfa-delete-enabled.rego"
)


def test_compliant():
    resources = [
        resource("aws_s3_bucket", "my_bucket", {}),
        resource(
            "aws_s3_bucket_versioning",
            "ver",
            {
                "bucket": "my_bucket",
                "versioning_configuration": [
                    {"status": "Enabled", "mfa_delete": "Enabled"}
                ],
            },
        ),
    ]
    inp = rego_input(resources)
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_s3_bucket", "my_bucket", {})])
    assert eval_rego_policy(POLICY, inp) != []
