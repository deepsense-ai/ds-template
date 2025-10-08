# API Package Usage

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