import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/s3/s3-bucket-server-side-encryption-enabled.rego"
)


def test_compliant():
    resources = [
        resource("aws_s3_bucket", "my_bucket", {}),
        resource(
            "aws_s3_bucket_server_side_encryption_configuration",
            "sse",
            {
                "bucket": "my_bucket",
                "rule": [
                    {
                        "apply_server_side_encryption_by_default": [
                            {"sse_algorithm": "AES256"}
                        ]
                    }
                ],
            },
        ),
    ]
    inp = rego_input(resources)
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_s3_bucket", "my_bucket", {})])
    assert eval_rego_policy(POLICY, inp) != []
