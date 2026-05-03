"""Runner — executes rules against a TerraformContext and collects violations."""

from __future__ import annotations

from .context import TerraformContext
from .rule import Rule, Violation


class Runner:  # pylint: disable=too-few-public-methods
    """Executes a list of rules against a TerraformContext and collects violations."""

    def run(self, rules: list[Rule], context: TerraformContext) -> list[Violation]:
        """Run all rules against *context* and return the combined violations."""
        violations: list[Violation] = []
        for rule in rules:
            violations.extend(rule.check(context))
        return violations
