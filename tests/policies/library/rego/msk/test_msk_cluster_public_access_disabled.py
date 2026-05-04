import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/msk/msk-cluster-public-access-disabled.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_msk_cluster",
                "cluster",
                {
                    "broker_node_group_info": [
                        {
                            "connectivity_info": [
                                {"public_access": [{"type": "DISABLED"}]}
                            ]
                        }
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
                    "broker_node_group_info": [
                        {
                            "connectivity_info": [
                                {"public_access": [{"type": "SERVICE_PROVIDED_EIPS"}]}
                            ]
                        }
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []
