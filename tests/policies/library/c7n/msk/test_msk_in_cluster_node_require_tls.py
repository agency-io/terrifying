import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/msk/msk-in-cluster-node-require-tls.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_msk_cluster",
        "cluster",
        '  encryption_info {\n    encryption_in_transit {\n      client_broker = "TLS"\n      in_cluster    = true\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_client_broker():
    tf = tf_resource(
        "aws_msk_cluster",
        "cluster",
        '  encryption_info {\n    encryption_in_transit {\n      client_broker = "PLAINTEXT"\n      in_cluster    = true\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []


def test_violation_in_cluster():
    tf = tf_resource(
        "aws_msk_cluster",
        "cluster",
        '  encryption_info {\n    encryption_in_transit {\n      client_broker = "TLS"\n      in_cluster    = false\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []
