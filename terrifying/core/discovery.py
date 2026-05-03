"""Custom rule discovery — loads Rule subclasses from a directory of Python files."""

from __future__ import annotations

import importlib.util
import logging
import sys
from pathlib import Path

from terrifying.core.rule import Rule

logger = logging.getLogger(__name__)


def discover_rules(path: Path) -> list[Rule]:
    """Import each .py file in path and return instances of Rule subclasses."""
    rules = []
    for py_file in sorted(path.glob("*.py")):
        try:
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[py_file.stem] = module
            spec.loader.exec_module(module)
            for attr in vars(module).values():
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Rule)
                    and attr is not Rule
                ):
                    rules.append(attr())
        except Exception:  # pylint: disable=broad-exception-caught
            logger.warning("Could not import %s", py_file)
    return rules
