import shutil
import json
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/s3/s3-bucket-ssl-requests-only.rego"


def test_compliant():
    policy_doc = json.dumps({
        "Statement": [{
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Condition": {"Bool": {"aws:SecureTransport": "false"}},
        }]
    })
    inp = rego_input([resource("aws_s3_bucket", "bucket", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    policy_doc = json.dumps({
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
        }]
    })
    inp = rego_input([resource("aws_s3_bucket", "bucket", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []
