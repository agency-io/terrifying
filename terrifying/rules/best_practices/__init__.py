"""terrifying.rules.best_practices — rules that enforce Terraform best practices."""

from .no_hardcoded_values import NoHardcodedValues
from .variables_have_descriptions import VariablesHaveDescriptions
from .outputs_have_descriptions import OutputsHaveDescriptions
from .required_tags import RequiredTags

__all__ = [
    "NoHardcodedValues",
    "VariablesHaveDescriptions",
    "OutputsHaveDescriptions",
    "RequiredTags",
]
