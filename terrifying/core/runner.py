from __future__ import annotations

from .context import TerraformContext
from .rule import Rule, Violation


class Runner:
    """Executes a list of rules against a TerraformContext and collects violations."""

    def run(self, rules: list[Rule], context: TerraformContext) -> list[Violation]:
        violations: list[Violation] = []
        for rule in rules:
            violations.extend(rule.check(context))
        return violations
