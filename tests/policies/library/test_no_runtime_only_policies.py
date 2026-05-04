from terrifying.policies.library import load_manifest

RUNTIME_ONLY = {
    "ec2-stopped-instance",
    "ec2-volume-inuse-check",
    "eip-attached",
    "ebs-snapshot-public-restorable-check",
    "dynamodb-in-backup-plan",
    "efs-in-backup-plan",
    "vpc-network-acl-unused-check",
    "access-keys-rotated",
    "iam-user-mfa-enabled",
    "iam-user-unused-credentials-check",
    "mfa-enabled-for-iam-console-access",
    "kms-cmk-not-scheduled-for-deletion-2",
    "secretsmanager-scheduled-rotation-success-check",
    "secretsmanager-secret-periodic-rotation",
    "secretsmanager-secret-unused",
    "cloudwatch-alarm-action-enabled-check",
}


def test_no_runtime_only_in_manifest():
    entries = load_manifest()
    bundled_ids = {e.id for e in entries}
    overlap = bundled_ids & RUNTIME_ONLY
    assert overlap == set(), f"Runtime-only policies found in manifest: {overlap}"
