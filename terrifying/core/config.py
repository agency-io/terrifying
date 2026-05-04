"""Configuration loader and rule factory for terrifying."""

from __future__ import annotations

import dataclasses
from pathlib import Path

import yaml

from terrifying.core.rule import Rule


@dataclasses.dataclass
class Config:
    """Parsed terrifying.yml configuration."""

    rules: dict[str, dict]
    custom_path: Path | None = None
    opa_policy_dir: Path | None = None
    c7n_policy_dir: Path | None = None
    terraform_path: Path | None = None


class ConfigLoader:  # pylint: disable=too-few-public-methods
    """Loads terrifying.yml and builds the rule and adapter lists."""

    def load(self, path: Path) -> Config:
        """Load config from terrifying.yml at path. Returns empty Config if file absent."""
        yml = path / "terrifying.yml"
        if not yml.exists():
            return Config(rules={})
        with open(yml, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        rules = {}
        for key, params in (data.get("rules") or {}).items():
            rules[key] = params or {}
        custom_path = None
        if "custom" in data and "path" in data["custom"]:
            custom_path = Path(data["custom"]["path"])
        opa_policy_dir = None
        if "policies" in data and "opa" in data["policies"]:
            opa_policy_dir = Path(data["policies"]["opa"])
        c7n_policy_dir = None
        if "policies" in data and "c7n" in data["policies"]:
            c7n_policy_dir = Path(data["policies"]["c7n"])
        terraform_path = None
        if "terraform" in data and "path" in data["terraform"]:
            terraform_path = Path(data["terraform"]["path"])
        return Config(
            rules=rules,
            custom_path=custom_path,
            opa_policy_dir=opa_policy_dir,
            c7n_policy_dir=c7n_policy_dir,
            terraform_path=terraform_path,
        )

    def build_rules(self, config: Config) -> list[Rule]:
        """Instantiate rules from config, passing configured parameters."""
        from terrifying.rules.structural import (  # pylint: disable=import-outside-toplevel
            MaxResourcesPerFile,
            MaxLinesPerFile,
            ResourceFileNaming,
        )
        from terrifying.rules.best_practices import (  # pylint: disable=import-outside-toplevel
            NoHardcodedValues,
            VariablesHaveDescriptions,
            OutputsHaveDescriptions,
            RequiredTags,
        )

        registry: dict[str, type] = {
            "max_resources_per_file": MaxResourcesPerFile,
            "max_lines_per_file": MaxLinesPerFile,
            "resource_file_naming": ResourceFileNaming,
            "no_hardcoded_values": NoHardcodedValues,
            "variables_have_descriptions": VariablesHaveDescriptions,
            "outputs_have_descriptions": OutputsHaveDescriptions,
            "required_tags": RequiredTags,
        }
        rules = []
        for key, params in config.rules.items():
            if key in registry:
                rules.append(registry[key](**params))
        return rules
