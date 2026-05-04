"""Test that nested c7n section is parsed into a PolicyConfig."""

from terrifying.core.config import ConfigLoader, PolicyConfig


def test_c7n_section_parsed(tmp_path):
    """Nested c7n dict with path and params produces correct PolicyConfig."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text(
        "policies:\n"
        "  c7n:\n"
        "    path: ./c7n_policies\n"
        "    params:\n"
        "      required_tags:\n"
        "        - Environment\n"
        "        - Team\n"
    )
    config = ConfigLoader().load(tmp_path)
    assert isinstance(config.c7n, PolicyConfig)
    assert config.c7n.path == tmp_path / "c7n_policies"
    assert config.c7n.params == {"required_tags": ["Environment", "Team"]}
