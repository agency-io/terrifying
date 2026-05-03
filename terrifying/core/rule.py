from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import TerraformContext


@dataclass
class Violation:
    """A single rule or parse violation found during a check."""

    rule: str
    file: Path
    message: str
    line: int | None = None
    severity: str = "error"


class Rule:
    """Base class for all terrifying rules.

    Subclasses implement ``check()`` and get a ``rule_id`` derived
    automatically from the class name (CamelCase → snake_case).
    """

    @property
    def rule_id(self) -> str:
        name = type(self).__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    def check(self, context: TerraformContext) -> list[Violation]:
        raise NotImplementedError
