#!/usr/bin/env python3
"""Generate terrifying/policies/library/manifest.yaml by scanning bundled policy files."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

LIBRARY = Path(__file__).parent.parent / "terrifying/policies/library"
MANIFEST = LIBRARY / "manifest.yaml"

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


def _parse_rego_meta(text: str) -> dict:
    meta = {}
    for line in text.splitlines():
        line = line.strip().lstrip("# ")
        for key in ("title", "description", "severity", "tags", "terraform_resources"):
            if line.startswith(f"{key}:"):
                val = line[len(key) + 1:].strip()
                if key in ("tags", "terraform_resources"):
                    meta[key] = [t.strip() for t in val.split(",") if t.strip()]
                else:
                    meta[key] = val
    return meta


def _parse_c7n_meta(text: str) -> dict:
    data = yaml.safe_load(text)
    policies = data.get("policies", [])
    if not policies:
        return {}
    p = policies[0]
    tags_raw = p.get("tags", [])
    # c7n resource type → terraform resource type (strip terraform. prefix for display)
    resource = p.get("resource", "")
    tf_resource = resource.replace("terraform.", "") if resource.startswith("terraform.") else resource
    return {
        "title": p.get("name", ""),
        "description": p.get("description", "").strip(),
        "severity": p.get("metadata", {}).get("severity", "medium") if isinstance(p.get("metadata"), dict) else "medium",
        "tags": tags_raw if isinstance(tags_raw, list) else [],
        "terraform_resources": [tf_resource] if tf_resource else [],
    }


def _build_entry(policy_id: str, engine: str, service: str, rel_file: str, meta: dict) -> dict:
    tags = list(meta.get("tags", []))
    # Normalize tags to kebab-case
    tags = [t.lower().replace("_", "-").strip() for t in tags]
    # Add engine, service, severity tags if not present
    for auto_tag in [engine, service, meta.get("severity", "medium").lower()]:
        if auto_tag and auto_tag not in tags:
            tags.append(auto_tag)

    return {
        "id": policy_id,
        "engine": engine,
        "service": service,
        "file": rel_file,
        "description": meta.get("description", f"{policy_id} policy").strip(),
        "severity": meta.get("severity", "medium").lower(),
        "terraform_resources": meta.get("terraform_resources", []),
        "tags": sorted(set(tags)),
        "params": [],
    }


def main() -> None:
    entries = []
    errors = []

    for service_dir in sorted(LIBRARY.iterdir()):
        if not service_dir.is_dir() or service_dir.name.startswith("_"):
            continue
        service = service_dir.name

        # Rego policies
        for rego_file in sorted(service_dir.glob("*.rego")):
            policy_id = rego_file.stem
            if policy_id in RUNTIME_ONLY:
                continue
            text = rego_file.read_text(encoding="utf-8")
            meta = _parse_rego_meta(text)
            rel = str(rego_file.relative_to(LIBRARY))
            entries.append(_build_entry(policy_id, "rego", service, rel, meta))

        # c7n policies
        for yml_file in sorted(service_dir.glob("*.yml")):
            policy_id = yml_file.stem
            if policy_id in RUNTIME_ONLY:
                continue
            try:
                text = yml_file.read_text(encoding="utf-8")
                meta = _parse_c7n_meta(text)
                rel = str(yml_file.relative_to(LIBRARY))
                entries.append(_build_entry(policy_id, "c7n", service, rel, meta))
            except Exception as e:
                errors.append(f"  {yml_file}: {e}")

    manifest = {"policies": entries}
    MANIFEST.write_text(yaml.dump(manifest, default_flow_style=False, sort_keys=False), encoding="utf-8")

    print(f"Generated manifest with {len(entries)} entries")
    if errors:
        print(f"Errors ({len(errors)}):")
        for err in errors:
            print(err)
    print(f"Written to: {MANIFEST}")


if __name__ == "__main__":
    main()
