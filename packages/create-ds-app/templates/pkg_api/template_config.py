import tomllib
from pathlib import Path

from ds_templater import TemplateConfig, TextQuestion


def validate_monorepo() -> bool:
    """Check if we're inside a monorepo by looking for pyproject.toml at root."""
    current_dir = Path.cwd()
    pyproject_path = current_dir / "pyproject.toml"

    if not pyproject_path.exists():
        raise ValueError("pyproject.toml not found in current directory. Make sure you're in a monorepo root.")

    return True


def get_pyproject_data() -> dict:
    """Fetch data from pyproject.toml."""
    validate_monorepo()

    pyproject_path = Path.cwd() / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    return data


class PkgApiTemplateConfig(TemplateConfig):
    """API package template configuration"""

    name: str = "API package"
    description: str = "RESTful API service that will be dockerized and deployed to servers"
    template_group: str = "package"

    questions: list = [
        TextQuestion(name="pkg_name", message="Package name (will be used as module name)", default="api-service"),
        TextQuestion(name="api_title", message="API title", default="My API Service"),
        TextQuestion(name="api_port", message="API port", default="8000"),
    ]

    def __init__(self):
        super().__init__()
        # Validate monorepo and get pyproject data
        self.pyproject_data = get_pyproject_data()

        # Extract Python version from pyproject.toml
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", ">=3.10")
        self.python_version = requires_python

    def get_template_vars(self) -> dict:
        """Get template variables including pyproject data."""
        base_vars = super().get_template_vars()
        base_vars.update({"python_version": self.python_version, "pyproject_data": self.pyproject_data})
        return base_vars


# Create instance of the config to be imported
config = PkgApiTemplateConfig()