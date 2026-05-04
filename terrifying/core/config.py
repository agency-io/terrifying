"""Configuration loader and rule factory for terrifying."""

from __future__ import annotations

import dataclasses
from pathlib import Path

import yaml

from terrifying.core.rule import Rule


@dataclasses.dataclass
class PolicyConfig:
    """Configuration for a single policy engine section (OPA or c7n)."""

    path: Path
    params: dict = dataclasses.field(default_factory=dict)
    policies: dict[str, dict] = dataclasses.field(default_factory=dict)

    def merged_params(self, policy_name: str) -> dict:
        """Return global params merged with per-policy overrides."""
        policy_overrides = self.policies.get(policy_name, {}).get("params", {})
        return {**self.params, **policy_overrides}


@dataclasses.dataclass
class Config:
    """Parsed terrifying.yml configuration."""

    rules: dict[str, dict]
    custom_path: Path | None = None
    opa: PolicyConfig | None = None
    c7n: PolicyConfig | None = None
    terraform_path: Path | None = None


class ConfigLoader:  # pylint: disable=too-few-public-methods
    """Loads terrifying.yml and builds the rule and adapter lists."""

    def _parse_policy_config(self, value, base_path: Path) -> PolicyConfig | None:
        """Parse a policy config value — either a plain path string or nested dict."""
        if value is None:
            return None
        if isinstance(value, str):
            # backward compat: plain string path
            return PolicyConfig(path=base_path / value)
        # nested dict format
        path = base_path / value["path"]
        params = value.get("params") or {}
        policies = {}
        for name, policy_data in (value.get("policies") or {}).items():
            policies[name] = policy_data or {}
        return PolicyConfig(path=path, params=params, policies=policies)

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
        policies_data = data.get("policies") or {}
        opa = self._parse_policy_config(policies_data.get("opa"), path)
        c7n = self._parse_policy_config(policies_data.get("c7n"), path)
        terraform_path = None
        if "terraform" in data and "path" in data["terraform"]:
            terraform_path = Path(data["terraform"]["path"])
        return Config(
            rules=rules,
            custom_path=custom_path,
            opa=opa,
            c7n=c7n,
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
