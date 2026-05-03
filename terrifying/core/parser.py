from __future__ import annotations

from pathlib import Path
from typing import Any

import hcl2

from .context import (
    Local,
    ModuleCall,
    Output,
    Resource,
    TerraformContext,
    TerraformFile,
    Variable,
)
from .rule import Violation


def _strip(value: Any) -> Any:
    """Strip surrounding HCL string quotes from a single value.

    python-hcl2 v4+ preserves the HCL template string delimiters, returning
    ``"prod"`` as the Python string ``'"prod"'``.  This helper removes those
    outer quotes so callers always receive clean Python strings.
    """
    if isinstance(value, str) and len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


def _strip_attrs(value: Any) -> Any:
    """Recursively strip HCL string quotes from an attribute dict or value."""
    if isinstance(value, str):
        return _strip(value)
    if isinstance(value, dict):
        return {k: _strip_attrs(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_strip_attrs(item) for item in value]
    return value


class Parser:
    """Parses a directory of .tf files into a TerraformContext."""

    def parse_directory(self, path: Path) -> TerraformContext:
        """Parse all .tf files in *path* and return an aggregated context.

        Files that fail to parse produce a ``parse_error`` violation;
        parsing continues for all remaining files.
        """
        tf_files = sorted(path.glob("*.tf"))
        files: list[TerraformFile] = []
        parse_violations: list[Violation] = []

        for tf_path in tf_files:
            tf_file, violations = self._parse_file(tf_path)
            parse_violations.extend(violations)
            if tf_file is not None:
                files.append(tf_file)

        return TerraformContext(files=files, parse_violations=parse_violations)

    # ── Private helpers ────────────────────────────────────────────────────────

    def _parse_file(
        self, path: Path
    ) -> tuple[TerraformFile | None, list[Violation]]:
        try:
            with open(path) as fh:
                data = hcl2.load(fh)
            line_count = len(path.read_text().splitlines())
            tf_file = TerraformFile(
                path=path,
                resources=self._extract_resources(data, path),
                variables=self._extract_variables(data, path),
                outputs=self._extract_outputs(data, path),
                locals=self._extract_locals(data, path),
                module_calls=self._extract_modules(data, path),
                line_count=line_count,
            )
            return tf_file, []
        except Exception as exc:
            violation = Violation(
                rule="parse_error",
                file=path,
                message=f"Failed to parse {path.name}: {exc}",
                severity="error",
            )
            return None, [violation]

    def _extract_resources(self, data: dict, path: Path) -> list[Resource]:
        resources = []
        for block in data.get("resource", []):
            for rtype, names in block.items():
                for rname, attrs in names.items():
                    resources.append(
                        Resource(
                            type=_strip(rtype),
                            name=_strip(rname),
                            attributes=_strip_attrs(attrs) if isinstance(attrs, dict) else {},
                            file=path,
                        )
                    )
        return resources

    def _extract_variables(self, data: dict, path: Path) -> list[Variable]:
        variables = []
        for block in data.get("variable", []):
            for vname, attrs in block.items():
                attrs = attrs if isinstance(attrs, dict) else {}
                variables.append(
                    Variable(
                        name=_strip(vname),
                        description=_strip(attrs.get("description")),
                        default=_strip(attrs.get("default")),
                        type=_strip(attrs.get("type")),
                        file=path,
                    )
                )
        return variables

    def _extract_outputs(self, data: dict, path: Path) -> list[Output]:
        outputs = []
        for block in data.get("output", []):
            for oname, attrs in block.items():
                attrs = attrs if isinstance(attrs, dict) else {}
                outputs.append(
                    Output(
                        name=_strip(oname),
                        description=_strip(attrs.get("description")),
                        value=_strip(attrs.get("value")),
                        file=path,
                    )
                )
        return outputs

    def _extract_locals(self, data: dict, path: Path) -> list[Local]:
        locals_list = []
        for block in data.get("locals", []):
            if isinstance(block, dict):
                for lname, lvalue in block.items():
                    locals_list.append(
                        Local(name=_strip(lname), value=_strip(lvalue), file=path)
                    )
        return locals_list

    def _extract_modules(self, data: dict, path: Path) -> list[ModuleCall]:
        modules = []
        for block in data.get("module", []):
            for mname, attrs in block.items():
                attrs = attrs if isinstance(attrs, dict) else {}
                modules.append(
                    ModuleCall(
                        name=_strip(mname),
                        source=_strip(attrs.get("source", "")),
                        arguments={k: _strip_attrs(v) for k, v in attrs.items() if k != "source"},
                        file=path,
                    )
                )
        return modules
