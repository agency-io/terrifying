"""MaxLinesPerFile rule — enforces a per-file line count limit."""

from terrifying.core import Rule, Violation, TerraformContext


class MaxLinesPerFile(Rule):
    """Fails if any .tf file exceeds the configured maximum line count."""

    def __init__(self, max_lines: int = 150):
        self.max_lines = max_lines

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for files exceeding the line count limit."""
        violations = []
        for tf_file in context.files:
            if tf_file.line_count > self.max_lines:
                violations.append(
                    Violation(
                        rule=self.rule_id,
                        file=tf_file.path,
                        message=f"{tf_file.line_count} lines exceeds max of {self.max_lines}",
                    )
                )
        return violations
