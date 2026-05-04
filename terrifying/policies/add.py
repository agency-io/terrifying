"""Logic for adding bundled policies to a project."""
from __future__ import annotations

import dataclasses
import difflib
import sys
from pathlib import Path

from ruamel.yaml import YAML

from terrifying.policies.library import PolicyEntry


@dataclasses.dataclass
class _FileOp:
    dest: Path
    source: str
    engine: str


@dataclasses.dataclass
class _Delta:
    file_ops: list[_FileOp]
    yml_before: str
    yml_after: str
    config_path: Path
    new_config: dict


def _load_yml(config_path: Path) -> tuple[dict, str]:
    yaml = YAML()
    yaml.preserve_quotes = True
    if config_path.exists():
        text = config_path.read_text(encoding="utf-8")
        import io
        data = yaml.load(text) or {}
    else:
        text = ""
        data = {}
    return data, text


def _dump_yml(data: dict) -> str:
    yaml = YAML()
    yaml.default_flow_style = False
    import io
    buf = io.StringIO()
    yaml.dump(data, buf)
    return buf.getvalue()


def _ensure_nested(data: dict, *keys: str) -> dict:
    node = data
    for key in keys:
        if key not in node or not isinstance(node[key], dict):
            node[key] = {}
        node = node[key]
    return node


def _collect_params(entries: list[PolicyEntry], config: dict) -> dict[str, dict]:
    """Prompt for unique undeclared params; return {engine: {name: value}}."""
    existing_opa = (
        config.get("policies", {}).get("opa", {}).get("params", {}) or {}
    )
    existing_c7n = (
        config.get("policies", {}).get("c7n", {}).get("params", {}) or {}
    )

    rego_entries = [e for e in entries if e.engine == "rego"]
    c7n_entries = [e for e in entries if e.engine == "c7n"]

    # Collect all unique param names needed
    rego_params_needed: dict[str, object] = {}
    for e in rego_entries:
        for p in e.params:
            if p.name not in existing_opa and p.name not in rego_params_needed:
                rego_params_needed[p.name] = p.default

    c7n_params_needed: dict[str, object] = {}
    for e in c7n_entries:
        for p in e.params:
            if p.name not in existing_c7n and p.name not in c7n_params_needed:
                c7n_params_needed[p.name] = p.default

    # Shared param names — prompt once
    shared = set(rego_params_needed) & set(c7n_params_needed)
    prompted: dict[str, object] = {}

    all_needed = {**rego_params_needed, **c7n_params_needed}
    for name, default in all_needed.items():
        if name in prompted:
            continue
        label = f"{name} [default: {default}]: " if default is not None else f"{name}: "
        try:
            val = input(label).strip()
        except EOFError:
            val = ""
        prompted[name] = val if val else default

    opa_new = {k: prompted[k] for k in rego_params_needed if k in prompted}
    c7n_new = {k: prompted[k] for k in c7n_params_needed if k in prompted}

    # Notify about shared params written to both
    for name in shared:
        if name in prompted:
            print(f"  (shared param '{name}' will be written to both opa and c7n sections)")

    return {"opa": opa_new, "c7n": c7n_new}


def _build_delta(
    entries: list[PolicyEntry],
    new_params: dict[str, dict],
    config_path: Path,
) -> _Delta:
    config, yml_before = _load_yml(config_path)

    # Determine output directories
    opa_path_str = (
        config.get("policies", {}).get("opa", {}).get("path")
        if isinstance(config.get("policies", {}).get("opa"), dict)
        else None
    ) or "./policies/opa"
    c7n_path_str = (
        config.get("policies", {}).get("c7n", {}).get("path")
        if isinstance(config.get("policies", {}).get("c7n"), dict)
        else None
    ) or "./policies/c7n"

    opa_dir = (config_path.parent / opa_path_str).resolve()
    c7n_dir = (config_path.parent / c7n_path_str).resolve()

    from terrifying.policies.library import get_policy_source

    file_ops: list[_FileOp] = []
    for entry in entries:
        source = get_policy_source(entry)
        ext = ".rego" if entry.engine == "rego" else ".yml"
        out_dir = opa_dir if entry.engine == "rego" else c7n_dir
        dest = out_dir / f"{entry.id}{ext}"
        file_ops.append(_FileOp(dest=dest, source=source, engine=entry.engine))

    # Build updated config
    import copy
    new_config = copy.deepcopy(config) if config else {}

    policies = _ensure_nested(new_config, "policies")

    rego_entries = [e for e in entries if e.engine == "rego"]
    c7n_entries = [e for e in entries if e.engine == "c7n"]

    if rego_entries:
        if not isinstance(policies.get("opa"), dict):
            policies["opa"] = {}
        if "path" not in policies["opa"]:
            policies["opa"]["path"] = opa_path_str
        if new_params.get("opa"):
            params_node = policies["opa"].setdefault("params", {})
            params_node.update(new_params["opa"])

    if c7n_entries:
        if not isinstance(policies.get("c7n"), dict):
            policies["c7n"] = {}
        if "path" not in policies["c7n"]:
            policies["c7n"]["path"] = c7n_path_str
        if new_params.get("c7n"):
            params_node = policies["c7n"].setdefault("params", {})
            params_node.update(new_params["c7n"])

    yml_after = _dump_yml(new_config) if new_config != (config or {}) else yml_before

    return _Delta(
        file_ops=file_ops,
        yml_before=yml_before,
        yml_after=yml_after,
        config_path=config_path,
        new_config=new_config,
    )


def _print_delta(delta: _Delta) -> None:
    print("\nFiles to be created:")
    for op in delta.file_ops:
        label = "[rego]" if op.engine == "rego" else "[c7n] "
        print(f"  {label}  {op.dest}")

    if delta.yml_before != delta.yml_after:
        print(f"\nChanges to {delta.config_path}:")
        diff = difflib.unified_diff(
            delta.yml_before.splitlines(keepends=True),
            delta.yml_after.splitlines(keepends=True),
            fromfile="terrifying.yml (before)",
            tofile="terrifying.yml (after)",
        )
        print("".join(diff), end="")
    else:
        print("\nNo changes to terrifying.yml.")


def _apply_delta(delta: _Delta) -> None:
    for op in delta.file_ops:
        op.dest.parent.mkdir(parents=True, exist_ok=True)
        if op.dest.exists():
            print(f"  WARNING: {op.dest} already exists — skipping")
            continue
        op.dest.write_text(op.source, encoding="utf-8")
        print(f"  Written: {op.dest}")

    if delta.yml_before != delta.yml_after:
        delta.config_path.parent.mkdir(parents=True, exist_ok=True)
        delta.config_path.write_text(delta.yml_after, encoding="utf-8")
        print(f"  Updated: {delta.config_path}")


def run_add(entries: list[PolicyEntry], dry_run: bool = False) -> None:
    """Main entry point: collect params, build delta, confirm, apply."""
    config_path = Path.cwd() / "terrifying.yml"
    config, _ = _load_yml(config_path)

    # Collect params (prompts user)
    existing_opa_params = (
        config.get("policies", {}).get("opa", {}).get("params", {}) or {}
    )
    existing_c7n_params = (
        config.get("policies", {}).get("c7n", {}).get("params", {}) or {}
    )
    for e in entries:
        for p in e.params:
            target = existing_opa_params if e.engine == "rego" else existing_c7n_params
            if p.name in target:
                print(f"  '{p.name}' already set in terrifying.yml — keeping existing value")

    new_params = _collect_params(entries, config)

    delta = _build_delta(entries, new_params, config_path)
    _print_delta(delta)

    if dry_run:
        print("\n(dry-run: no files written)")
        return

    answer = input("\nApply? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        return

    _apply_delta(delta)
    print("\nDone.")
