"""Logic for adding bundled policies to a project."""

from __future__ import annotations

import copy
import dataclasses
import difflib
import io
from pathlib import Path

from ruamel.yaml import YAML

from terrifying.policies.library import PolicyEntry, get_policy_source


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

        data = yaml.load(text) or {}
    else:
        text = ""
        data = {}
    return data, text


def _dump_yml(data: dict) -> str:
    yaml = YAML()
    yaml.default_flow_style = False
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


def _params_needed(
    entries: list[PolicyEntry], engine: str, existing: dict
) -> dict[str, object]:
    """Return {name: default} for params not already in existing."""
    needed: dict[str, object] = {}
    for e in entries:
        if e.engine != engine:
            continue
        for p in e.params:
            if p.name not in existing and p.name not in needed:
                needed[p.name] = p.default
    return needed


def _prompt_param(name: str, default: object) -> object:
    """Prompt the user for a param value; return default on empty input or EOF."""
    label = f"{name} [default: {default}]: " if default is not None else f"{name}: "
    try:
        val = input(label).strip()
    except EOFError:
        val = ""
    return val if val else default


def _collect_params(entries: list[PolicyEntry], config: dict) -> dict[str, dict]:
    """Prompt for unique undeclared params; return {engine: {name: value}}."""
    existing_opa = config.get("policies", {}).get("opa", {}).get("params", {}) or {}
    existing_c7n = config.get("policies", {}).get("c7n", {}).get("params", {}) or {}

    rego_needed = _params_needed(entries, "rego", existing_opa)
    c7n_needed = _params_needed(entries, "c7n", existing_c7n)
    shared = set(rego_needed) & set(c7n_needed)

    prompted: dict[str, object] = {}
    for name, default in {**rego_needed, **c7n_needed}.items():
        if name not in prompted:
            prompted[name] = _prompt_param(name, default)

    for name in shared:
        if name in prompted:
            print(
                f"  (shared param '{name}' will be written to both opa and c7n sections)"
            )

    return {
        "opa": {k: prompted[k] for k in rego_needed if k in prompted},
        "c7n": {k: prompted[k] for k in c7n_needed if k in prompted},
    }


def _engine_path(config: dict, engine_key: str, default: str) -> str:
    """Return the configured path for an engine section, or the default."""
    section = config.get("policies", {}).get(engine_key)
    if isinstance(section, dict):
        return section.get("path") or default
    return default


def _build_file_ops(
    entries: list[PolicyEntry], opa_dir: Path, c7n_dir: Path
) -> list[_FileOp]:
    """Build the list of file copy operations for the given entries."""
    ops = []
    for entry in entries:
        ext = ".rego" if entry.engine == "rego" else ".yml"
        out_dir = opa_dir if entry.engine == "rego" else c7n_dir
        ops.append(
            _FileOp(
                dest=out_dir / f"{entry.id}{ext}",
                source=get_policy_source(entry),
                engine=entry.engine,
            )
        )
    return ops


def _update_engine_section(
    policies: dict, key: str, path_str: str, params: dict
) -> None:
    """Ensure the engine section exists with path and params set."""
    if not isinstance(policies.get(key), dict):
        policies[key] = {}
    if "path" not in policies[key]:
        policies[key]["path"] = path_str
    if params:
        policies[key].setdefault("params", {}).update(params)


def _build_delta(
    entries: list[PolicyEntry],
    new_params: dict[str, dict],
    config_path: Path,
) -> _Delta:
    """Build a delta describing files to copy and config changes to make."""
    config, yml_before = _load_yml(config_path)

    opa_path_str = _engine_path(config, "opa", "./policies/opa")
    c7n_path_str = _engine_path(config, "c7n", "./policies/c7n")
    opa_dir = (config_path.parent / opa_path_str).resolve()
    c7n_dir = (config_path.parent / c7n_path_str).resolve()

    file_ops = _build_file_ops(entries, opa_dir, c7n_dir)

    new_config = copy.deepcopy(config) if config else {}
    policies = _ensure_nested(new_config, "policies")
    if any(e.engine == "rego" for e in entries):
        _update_engine_section(policies, "opa", opa_path_str, new_params.get("opa", {}))
    if any(e.engine == "c7n" for e in entries):
        _update_engine_section(policies, "c7n", c7n_path_str, new_params.get("c7n", {}))

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
                print(
                    f"  '{p.name}' already set in terrifying.yml — keeping existing value"
                )

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
