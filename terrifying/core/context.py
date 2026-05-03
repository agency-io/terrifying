from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .rule import Violation


@dataclass
class Resource:
    """A single Terraform resource block."""

    type: str
    name: str
    attributes: dict[str, Any]
    file: Path
    line: int | None = None


@dataclass
class Variable:
    """A single Terraform variable block."""

    name: str
    description: str | None
    default: Any
    type: str | None
    file: Path
    line: int | None = None


@dataclass
class Output:
    """A single Terraform output block."""

    name: str
    description: str | None
    value: Any
    file: Path
    line: int | None = None


@dataclass
class Local:
    """A single local value defined in a locals block."""

    name: str
    value: Any
    file: Path
    line: int | None = None


@dataclass
class ModuleCall:
    """A single Terraform module call."""

    name: str
    source: str
    arguments: dict[str, Any]
    file: Path
    line: int | None = None


@dataclass
class TerraformFile:
    """All parsed content from a single .tf file."""

    path: Path
    resources: list[Resource] = field(default_factory=list)
    variables: list[Variable] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)
    locals: list[Local] = field(default_factory=list)
    module_calls: list[ModuleCall] = field(default_factory=list)
    line_count: int = 0


@dataclass
class TerraformContext:
    """Aggregated view of all .tf files in a checked directory."""

    files: list[TerraformFile] = field(default_factory=list)
    parse_violations: list[Violation] = field(default_factory=list)

    @property
    def resources(self) -> list[Resource]:
        """Flat list of all resources across all files."""
        return [resource for tf_file in self.files for resource in tf_file.resources]

    def to_json(self) -> dict:
        """Serialise to a plain dict suitable for policy engine input."""
        return {
            "files": [_file_to_dict(f) for f in self.files],
            "resources": [_resource_to_dict(r) for r in self.resources],
        }


# ── Serialisation helpers ──────────────────────────────────────────────────────


def _resource_to_dict(r: Resource) -> dict:
    return {
        "type": r.type,
        "name": r.name,
        "attributes": r.attributes,
        "file": str(r.file),
        "line": r.line,
    }


def _variable_to_dict(v: Variable) -> dict:
    return {
        "name": v.name,
        "description": v.description,
        "default": v.default,
        "type": v.type,
        "file": str(v.file),
        "line": v.line,
    }


def _output_to_dict(o: Output) -> dict:
    return {
        "name": o.name,
        "description": o.description,
        "value": o.value,
        "file": str(o.file),
        "line": o.line,
    }


def _file_to_dict(f: TerraformFile) -> dict:
    return {
        "path": str(f.path),
        "line_count": f.line_count,
        "resources": [_resource_to_dict(r) for r in f.resources],
        "variables": [_variable_to_dict(v) for v in f.variables],
        "outputs": [_output_to_dict(o) for o in f.outputs],
    }
