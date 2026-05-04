"""Test that nested opa section is parsed into a PolicyConfig."""

from terrifying.core.config import ConfigLoader, PolicyConfig


def test_opa_section_parsed(tmp_path):
    """Nested opa dict with path and params produces correct PolicyConfig."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text(
        "policies:\n"
        "  opa:\n"
        "    path: ./opa_policies\n"
        "    params:\n"
        "      required_tags:\n"
        "        - Environment\n"
        "        - Team\n"
    )
    config = ConfigLoader().load(tmp_path)
    assert isinstance(config.opa, PolicyConfig)
    assert config.opa.path == tmp_path / "opa_policies"
    assert config.opa.params == {"required_tags": ["Environment", "Team"]}
