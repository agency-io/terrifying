"""Bundled policy library — manifest loader and policy file access."""
from __future__ import annotations

import dataclasses
import importlib.resources
from pathlib import Path

import yaml


@dataclasses.dataclass
class ParamDescriptor:
    name: str
    type: str
    description: str
    default: object


@dataclasses.dataclass
class PolicyEntry:
    id: str
    engine: str  # "rego" | "c7n"
    service: str
    file: str
    description: str
    severity: str
    terraform_resources: list[str]
    tags: list[str]
    params: list[ParamDescriptor]

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


def load_manifest() -> list[PolicyEntry]:
    """Load all policy entries from the bundled manifest.yaml."""
    pkg = importlib.resources.files("terrifying.policies.library")
    manifest_text = (pkg / "manifest.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(manifest_text)
    entries = []
    for raw in data.get("policies", []):
        params = [
            ParamDescriptor(
                name=p["name"],
                type=p["type"],
                description=p["description"],
                default=p.get("default"),
            )
            for p in raw.get("params", [])
        ]
        entries.append(
            PolicyEntry(
                id=raw["id"],
                engine=raw["engine"],
                service=raw["service"],
                file=raw["file"],
                description=raw["description"],
                severity=raw["severity"],
                terraform_resources=raw.get("terraform_resources", []),
                tags=raw.get("tags", []),
                params=params,
            )
        )
    return entries


def get_policy_source(entry: PolicyEntry) -> str:
    """Return the raw policy file contents for a manifest entry."""
    pkg = importlib.resources.files("terrifying.policies.library")
    return (pkg / entry.file).read_text(encoding="utf-8")


def filter_by_tags(entries: list[PolicyEntry], tags: list[str]) -> list[PolicyEntry]:
    """Return entries that carry ALL of the given tags."""
    return [e for e in entries if all(e.has_tag(t) for t in tags)]


def filter_by_engine(entries: list[PolicyEntry], engine: str) -> list[PolicyEntry]:
    """Return entries matching engine. 'both' returns all entries."""
    if engine == "both":
        return list(entries)
    return [e for e in entries if e.engine == engine]
