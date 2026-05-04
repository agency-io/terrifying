import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/msk/msk-cluster-public-access-disabled.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_msk_cluster",
        "cluster",
        '  broker_node_group_info {\n    connectivity_info {\n      public_access {\n        type = "DISABLED"\n      }\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_msk_cluster",
        "cluster",
        '  broker_node_group_info {\n    connectivity_info {\n      public_access {\n        type = "SERVICE_PROVIDED_EIPS"\n      }\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
