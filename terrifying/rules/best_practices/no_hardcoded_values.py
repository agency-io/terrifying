"""NoHardcodedValues rule — flags plain string or numeric attribute values in resources."""

from __future__ import annotations

from terrifying.core import Rule, Violation, TerraformContext


def _is_reference(value: str) -> bool:
    """Return True if the string value is a Terraform reference expression."""
    ref_prefixes = ("var.", "local.", "data.")
    ref_interpolations = ("${var.", "${local.", "${data.")
    if any(value.startswith(p) for p in ref_prefixes):
        return True
    if any(value.startswith(p) for p in ref_interpolations):
        return True
    return False


class NoHardcodedValues(Rule):
    """Flags resource attributes with plain string or number values rather than references."""

    def __init__(self, allowed_attributes: list[str] | None = None):
        self.allowed_attributes: list[str] = allowed_attributes or []

    def _is_hardcoded(self, attr_key: str, attr_value: object) -> bool:
        """Return True if the attribute value is a hardcoded plain value."""
        if attr_key in self.allowed_attributes:
            return False
        if isinstance(attr_value, (dict, list)):
            return False
        if isinstance(attr_value, str) and _is_reference(attr_value):
            return False
        return isinstance(attr_value, (str, int, float))

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for hardcoded string or numeric attribute values."""
        violations = []
        for resource in context.resources:
            for attr_key, attr_value in resource.attributes.items():
                if not self._is_hardcoded(attr_key, attr_value):
                    continue
                msg = (
                    f"Resource {resource.type}.{resource.name} attribute "
                    f"'{attr_key}' has a hardcoded value: {attr_value!r}"
                )
                violations.append(
                    Violation(rule=self.rule_id, file=resource.file, message=msg)
                )
        return violations
