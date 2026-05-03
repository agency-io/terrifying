"""CLI entry point for terrifying — runs rules against a Terraform directory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from terrifying.core.config import ConfigLoader
from terrifying.core.discovery import discover_rules
from terrifying.core.parser import Parser
from terrifying.core.rule import Violation
from terrifying.core.runner import Runner


def _format_text(v: Violation) -> str:
    """Format a violation as a human-readable text line."""
    line = f":{v.line}" if v.line is not None else ""
    return f"{v.file}{line} [{v.rule}] {v.severity}: {v.message}"


def _violation_to_dict(v: Violation) -> dict:
    """Convert a violation to a JSON-serialisable dictionary."""
    return {
        "rule": v.rule,
        "file": str(v.file),
        "line": v.line,
        "severity": v.severity,
        "message": v.message,
    }


def main() -> None:
    """Entry point for the terrifying CLI."""
    parser = argparse.ArgumentParser(
        prog="terrifying", description="Architecture testing for Terraform"
    )
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check", help="Check a Terraform directory")
    check.add_argument("directory", help="Path to Terraform directory")
    check.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.command != "check":
        parser.print_help()
        sys.exit(1)

    tf_dir = Path(args.directory)
    if not tf_dir.is_dir():
        print(f"Error: {tf_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    config_loader = ConfigLoader()
    config = config_loader.load(Path.cwd())
    rules = config_loader.build_rules(config)

    if config.custom_path and config.custom_path.is_dir():
        rules.extend(discover_rules(config.custom_path))

    context = Parser().parse_directory(tf_dir)
    violations = Runner().run(rules, context) + context.parse_violations

    if config.opa_policy_dir and config.opa_policy_dir.is_dir():
        # pylint: disable=import-outside-toplevel
        from terrifying.policies.opa import OpaAdapter

        violations.extend(OpaAdapter(config.opa_policy_dir).run(context))

    if config.c7n_policy_dir and config.c7n_policy_dir.is_dir():
        # pylint: disable=import-outside-toplevel
        from terrifying.policies.c7n import C7nAdapter

        violations.extend(C7nAdapter(config.c7n_policy_dir).run(tf_dir))

    if args.format == "json":
        print(json.dumps([_violation_to_dict(v) for v in violations]))
    else:
        for v in violations:
            print(_format_text(v))

    has_errors = any(v.severity == "error" for v in violations)
    sys.exit(1 if has_errors else 0)
