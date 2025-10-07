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


class PkgApiTemplateConfig(TemplateConfig):
    """API package template configuration"""

    name: str = "API package"
    description: str = "RESTful API service that will be dockerized and deployed to servers"
    template_group: str = "package"
    instructions: str = """# API Package Usage

This package provides a **FastAPI** RESTful API service with **Pydantic** for data validation and settings management.

## Key Features

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic Settings**: Configuration management with environment variable support
- **Automatic Documentation**: Auto-generated OpenAPI/Swagger docs
- **Type Safety**: Full type hints and validation
- **Docker Ready**: Pre-configured for containerization

## Configuration Management

### Pydantic Settings with .env Support
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_title: str = "My API Service"
    api_port: int = 8000
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### Environment Variables
Create a `.env` file in your project root:
```bash
API_TITLE=My Custom API
API_PORT=9000
DEBUG=true
```

## API Development

### Basic Endpoint Structure
```python
from fastapi import FastAPI
from .config import settings

app = FastAPI(title=settings.api_title)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Running the API
```bash
# Development
uv run uvicorn packages.<api_package>.main:app --reload --port 8000

# Production
uv run uvicorn packages.<api_package>.main:app --host 0.0.0.0 --port 8000
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Development
- Main app in `main.py`
- Routers in `routers/` directory
- Configuration in `config.py`
- Use Pydantic models for request/response validation
- Leverage FastAPI's dependency injection system
"""

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
        requires_python = self.pyproject_data.get("project", {}).get("requires-python", "3.13")
        # Extract just the version number without the >= prefix
        self.python_version = requires_python.replace(">=", "")

    def build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build additional context including pyproject data."""
        additional_context = super().build_context(context)
        additional_context.update(
            {
                "python_version": self.python_version,
                "pyproject_data": self.pyproject_data,
                "api_port": context.get("api_port", "8000"),
                "api_title": context.get("api_title", "My API Service"),
            }
        )
        return additional_context

# Create instance of the config to be imported
config = PkgApiTemplateConfig()
