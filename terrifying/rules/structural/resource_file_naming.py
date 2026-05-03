"""ResourceFileNaming rule — enforces a naming pattern on .tf files."""

import re

from terrifying.core import Rule, Violation, TerraformContext


class ResourceFileNaming(Rule):
    """Fails if any .tf file name does not match the required regex pattern."""

    def __init__(self, pattern: str):
        self.pattern = pattern
        self._compiled = re.compile(pattern)

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for files whose names do not match the pattern."""
        violations = []
        for tf_file in context.files:
            if not self._compiled.fullmatch(tf_file.path.name):
                violations.append(
                    Violation(
                        rule=self.rule_id,
                        file=tf_file.path,
                        message=(
                            f"{tf_file.path.name} does not match"
                            f" required pattern {self.pattern}"
                        ),
                    )
                )
        return violations
