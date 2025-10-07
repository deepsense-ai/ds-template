import tomllib
from pathlib import Path
from typing import Any

from ds_templater import TemplateConfig, TextQuestion


def validate_monorepo() -> bool:
    """Check if we're inside a monorepo by looking for pyproject.toml at root."""
    pyproject_path = Path.cwd() / "pyproject.toml"

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


class PkgFrontendStreamlitTemplateConfig(TemplateConfig):
    """Streamlit frontend package template configuration"""

    name: str = "Streamlit Frontend"
    description: str = "Interactive web application using Streamlit framework for rapid prototyping"
    template_group: str = "package"
    instructions: str = """# Frontend Package Usage

This package provides a **Streamlit** web application with **branding integration** and **component-based architecture**.

## Key Features

- **Streamlit**: Rapid web app development for data science
- **Branding System**: Automatic integration with company branding
- **Component Architecture**: Reusable UI components
- **Configuration Management**: Environment-based settings
- **Docker Ready**: Pre-configured for containerization

## Branding Integration

### Automatic Branding
The app automatically loads branding from `branding/branding.json`:
```python
from .utils.branding import load_branding

branding = load_branding()
# Access: branding["name"], branding["colors"], branding["logo"]
```

### Branding Configuration
Update `branding/branding.json`:
```json
{
    "name": "Your Company Name",
    "colors": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e"
    },
    "logo": "path/to/logo.png"
}
```

## App Development

### Basic App Structure
```python
import streamlit as st
from .config import settings
from .utils.branding import load_branding

st.set_page_config(
    page_title=settings.app_title,
    page_icon="🚀",
    layout="wide"
)

branding = load_branding()
st.title(f"🚀 {branding['name']}")
```

### Component Usage
```python
from .components.sidebar import create_sidebar
from .components.charts import create_chart

# Use sidebar component
with create_sidebar():
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Analytics"])

# Use chart component
if page == "Analytics":
    create_chart(data)
```

### Running the App
```bash
# Development
uv run streamlit run packages/<frontend_package>/src/<package_name>/app.py

# With custom port
uv run streamlit run packages/<frontend_package>/src/<package_name>/app.py --server.port 8501
```

## Development
- Main app in `app.py`
- Components in `components/` directory
- Utilities in `utils/` directory
- Configuration in `config.py`
- Always use the branding system for consistent UI
- Leverage Streamlit's caching for performance
"""

    questions: list = [
        TextQuestion(name="pkg_name", message="Package name (will be used as module name)", default="frontend-streamlit"),
        TextQuestion(name="app_title", message="Application title", default="My Streamlit App"),
        TextQuestion(name="app_port", message="Application port", default="8501"),
    ]

    def __init__(self):
        super().__init__()
        # Validate monorepo and get pyproject data
        self.pyproject_data = get_pyproject_data()

        # Extract Python version from pyproject.toml
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", "3.13")
        self.python_version = requires_python.replace(">=", "")

    def build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build additional context including pyproject data."""
        additional_context = super().build_context(context)
        additional_context.update(
            {
                "python_version": self.python_version, 
                "pyproject_data": self.pyproject_data,
                "app_port": context.get("app_port", "8501"),
                "app_title": context.get("app_title", "My Streamlit App"),
            }
        )
        return additional_context


# Create instance of the config to be imported
config = PkgFrontendStreamlitTemplateConfig()