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


class PkgCliTemplateConfig(TemplateConfig):
    """Python CLI package template configuration"""

    name: str = "CLI"
    description: str = "Developer tools, evaluation pipelines and similar utilities packaged as executable commands"
    template_group: str = "package"
    instructions: str = """# CLI Package Usage

This package provides a command-line interface using **Typer** for fast and modern CLI development.

## Key Features

- **Typer Integration**: Built on Typer for type-safe CLI development
- **Automatic Help**: Commands automatically generate help text
- **Type Validation**: Input validation based on Python type hints
- **Rich Output**: Beautiful terminal output with colors and formatting

## Usage Examples

### Basic Command Structure
```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str = typer.Argument(..., help="Name to greet")):
    \"\"\"Say hello to someone.\"\"\"
    typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

### Running Commands
```bash
# Install the package
uv pip install -e packages/<package_name>

# Run the CLI
<cli_command> --help
<cli_command> hello John
```

### Advanced Features
- **Subcommands**: Organize commands into groups
- **Options**: Add flags and options with validation
- **Callbacks**: Execute code before/after commands
- **Progress Bars**: Show progress for long operations
- **Confirmation**: Ask for user confirmation

## Development
- Main CLI logic in `cli.py`
- Add new commands by decorating functions with `@app.command()`
- Use `typer.echo()` for output instead of `print()`
- Leverage type hints for automatic validation
"""

    questions: list = [
        TextQuestion(name="pkg_name", message="Package name (will be used as module name)", default="my-cli-package"),
        TextQuestion(name="cli_command", message="CLI command name", default="my-cli"),
        TextQuestion(name="version", message="Initial version", default="0.1.0"),
        TextQuestion(name="author", message="Author name and email", default="Your Name <your.email@example.com>"),
        TextQuestion(name="keywords", message="Keywords (comma-separated)", default="cli, tool"),
    ]

    def __init__(self):
        super().__init__()
        # Validate monorepo and get pyproject data
        self.pyproject_data = get_pyproject_data()

        # Extract Python version from pyproject.toml
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", "3.13")
        # Extract just the version number without the >= prefix
        self.python_version = requires_python.replace(">=", "")

    def build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build additional context including pyproject data."""
        additional_context = super().build_context(context)
        additional_context.update({"python_version": self.python_version, "pyproject_data": self.pyproject_data})
        return additional_context


# Create instance of the config to be imported
config = PkgCliTemplateConfig()
