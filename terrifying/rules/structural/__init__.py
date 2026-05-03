"""terrifying.rules.structural — rules that enforce structural conventions on .tf files."""

from .max_resources_per_file import MaxResourcesPerFile
from .max_lines_per_file import MaxLinesPerFile
from .resource_file_naming import ResourceFileNaming

__all__ = [
    "MaxResourcesPerFile",
    "MaxLinesPerFile",
    "ResourceFileNaming",
]
