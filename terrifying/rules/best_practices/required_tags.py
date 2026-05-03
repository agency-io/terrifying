"""RequiredTags rule — flags resources that are missing required tag keys."""

from __future__ import annotations

from terrifying.core import Rule, Violation, TerraformContext


class RequiredTags(Rule):
    """Flags resources that are missing one or more required tag keys."""

    def __init__(self, tags: list[str]):
        self.tags = tags

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for resources missing required tags."""
        violations = []
        for resource in context.resources:
            resource_tags = resource.attributes.get("tags", None)
            for tag in self.tags:
                if resource_tags is None:
                    violations.append(
                        Violation(
                            rule=self.rule_id,
                            file=resource.file,
                            message=(
                                f"Resource {resource.type}.{resource.name} "
                                f"is missing required tag '{tag}'"
                            ),
                        )
                    )
                elif isinstance(resource_tags, dict) and tag not in resource_tags:
                    violations.append(
                        Violation(
                            rule=self.rule_id,
                            file=resource.file,
                            message=(
                                f"Resource {resource.type}.{resource.name} "
                                f"is missing required tag '{tag}'"
                            ),
                        )
                    )
        return violations
