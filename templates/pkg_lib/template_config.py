import tomllib
from pathlib import Path
from typing import Any

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


class PkgLibTemplateConfig(TemplateConfig):
    """Python package / Library code template configuration"""

    name: str = "Library"
    description: str = "Shared library that may be used between one or more components, packaged as a Python module"
    template_group: str = "package"

    questions: list = [
        TextQuestion(name="pkg_name", message="Package name (will be used as module name)", default="my-lib-package"),
    ]

    def __init__(self):
        super().__init__()
        # Validate monorepo and get pyproject data
        self.pyproject_data = get_pyproject_data()

        # Extract Python version from pyproject.toml
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", ">=3.10")
        # Extract just the version number without the >= prefix
        self.python_version = requires_python.replace(">=", "")

    def build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build additional context including pyproject data."""
        additional_context = super().build_context(context)
        additional_context.update({"python_version": self.python_version, "pyproject_data": self.pyproject_data})
        return additional_context

# Create instance of the config to be imported
config = PkgLibTemplateConfig()

