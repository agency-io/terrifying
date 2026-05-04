import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/msk/msk-in-cluster-node-require-tls.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_msk_cluster",
                "cluster",
                {
                    "encryption_info": [
                        {"encryption_in_transit": [{"client_broker": "TLS"}]}
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input(
        [
            resource(
                "aws_msk_cluster",
                "cluster",
                {
                    "encryption_info": [
                        {"encryption_in_transit": [{"client_broker": "TLS_PLAINTEXT"}]}
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []
