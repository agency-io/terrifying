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


def _cmd_check(args: argparse.Namespace) -> None:
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

    if config.opa and config.opa.path.is_dir():
        # pylint: disable=import-outside-toplevel
        from terrifying.policies.opa import OpaAdapter

        violations.extend(OpaAdapter(config.opa).run(context))

    if config.c7n and config.c7n.path.is_dir():
        # pylint: disable=import-outside-toplevel
        from terrifying.policies.c7n import C7nAdapter

        violations.extend(C7nAdapter(config.c7n).run(tf_dir))

    if args.format == "json":
        print(json.dumps([_violation_to_dict(v) for v in violations]))
    else:
        for v in violations:
            print(_format_text(v))

    has_errors = any(v.severity == "error" for v in violations)
    sys.exit(1 if has_errors else 0)


def _cmd_list(args: argparse.Namespace) -> None:
    # pylint: disable=import-outside-toplevel
    from terrifying.policies.library import filter_by_engine, filter_by_tags, load_manifest

    entries = filter_by_engine(load_manifest(), args.engine)
    if args.tags:
        entries = filter_by_tags(entries, args.tags)

    if not entries:
        print("No policies match the given filters.")
        return

    current_service = None
    for entry in sorted(entries, key=lambda e: (e.service, e.id, e.engine)):
        if entry.service != current_service:
            print(f"\n{entry.service.upper()}")
            current_service = entry.service
        engine_label = "[rego]" if entry.engine == "rego" else "[c7n] "
        print(f"  {engine_label}  {entry.id:<50} {entry.severity:<8}  {entry.description[:60]}")

    print(f"\n{len(entries)} policies")


def _cmd_add(args: argparse.Namespace) -> None:
    # pylint: disable=import-outside-toplevel
    from terrifying.policies.library import (
        filter_by_engine,
        load_manifest,
    )
    from terrifying.policies.add import run_add

    entries = filter_by_engine(load_manifest(), args.engine)
    policy_ids = list(args.policy_ids) if args.policy_ids else []

    if policy_ids:
        id_set = {e.id for e in entries}
        unknown = [pid for pid in policy_ids if pid not in id_set]
        if unknown:
            print(f"Error: unknown policy ID(s): {', '.join(unknown)}", file=sys.stderr)
            sys.exit(1)
        entries = [e for e in entries if e.id in set(policy_ids)]
    else:
        # TUI mode
        try:
            from terrifying.tui import run_tui
        except ImportError:
            print(
                "TUI requires textual: pip install terrifying[tui]",
                file=sys.stderr,
            )
            sys.exit(1)
        entries = run_tui(entries, args.engine)
        if not entries:
            print("No policies selected.")
            return

    run_add(entries, dry_run=args.dry_run)


def main() -> None:
    """Entry point for the terrifying CLI."""
    parser = argparse.ArgumentParser(
        prog="terrifying", description="Architecture testing for Terraform"
    )
    sub = parser.add_subparsers(dest="command")

    check = sub.add_parser("check", help="Check a Terraform directory")
    check.add_argument("directory", help="Path to Terraform directory")
    check.add_argument("--format", choices=["text", "json"], default="text")

    add = sub.add_parser("add", help="Add bundled policies to your project")
    add.add_argument(
        "policy_ids",
        nargs="*",
        metavar="policy-id",
        help="Policy IDs to add (omit to launch TUI browser)",
    )
    add.add_argument(
        "--engine",
        choices=["rego", "c7n", "both"],
        default="both",
        help="Which engine variant(s) to add (default: both)",
    )
    add.add_argument(
        "--dry-run",
        action="store_true",
        help="Print delta without writing any files",
    )

    list_cmd = sub.add_parser("list", help="List available bundled policies")
    list_cmd.add_argument(
        "--engine",
        choices=["rego", "c7n", "both"],
        default="both",
        help="Filter by engine (default: both)",
    )
    list_cmd.add_argument(
        "--tag",
        action="append",
        dest="tags",
        metavar="TAG",
        help="Filter by tag (can be repeated, e.g. --tag fsbp --tag s3)",
    )

    args = parser.parse_args()

    if args.command == "check":
        _cmd_check(args)
    elif args.command == "add":
        _cmd_add(args)
    elif args.command == "list":
        _cmd_list(args)
    else:
        parser.print_help()
        sys.exit(1)
