import importlib.resources
import yaml
from terrifying.policies.library import load_manifest


def test_c7n_policies_terraform_resource():
    pkg = importlib.resources.files("terrifying.policies.library")
    entries = [e for e in load_manifest() if e.engine == "c7n"]
    assert len(entries) > 0
    for entry in entries:
        source = (pkg / entry.file).read_text(encoding="utf-8")
        data = yaml.safe_load(source)
        for policy in data.get("policies", []):
            resource = policy.get("resource", "")
            assert resource.startswith("terraform."), (
                f"{entry.file}: policy '{policy.get('name')}' resource '{resource}' "
                "does not start with 'terraform.'"
            )
