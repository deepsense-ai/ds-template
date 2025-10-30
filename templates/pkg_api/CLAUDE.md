# API Package Rules

This package provides a **FastAPI** RESTful API service with router-based architecture and lifespan management.

## Router Rules

- **ALL** new endpoints must be in separate router files in `routers/` directory
- **ALWAYS** use `APIRouter()` for new routers
- **MUST** include routers in `main.py` using `app.include_router(router, prefix="/api/v1", tags=["tag_name"])`
- Keep routers focused and single-purpose (one router per domain/feature)

## Endpoint Rules

- **ALWAYS** use async functions for endpoints: `async def endpoint_name()`
- **MUST** use Pydantic models for request/response validation
- **MUST** include docstrings (these appear in OpenAPI docs)
- Use proper HTTP status codes (200, 201, 404, 500, etc.)

## Configuration Rules

- **ALL** configuration must use Pydantic Settings in `config.py`
- **ALL** settings must load from `.env` file via `env_file = ".env"`
- CORS origins must be configurable via `cors_origins` in settings

## Application Lifespan Rules

- **MUST** use lifespan context manager for startup/shutdown logic
- Store shared resources (database pools, connections) in `app.state` during lifespan
- Access app state in routes via `request: Request` parameter
- Clean up resources in shutdown phase

## Request/Response Rules

- **ALWAYS** use Pydantic models for request/response validation
- **NEVER** use raw dict returns - always return typed models
- Use `HTTPException` for error responses with appropriate status codes

## Health Check Rules

- Implement `/health` endpoint for basic health check
- Implement `/health/ready` for readiness probe (check dependencies)
- Implement `/health/live` for liveness probe
- Return 503 status if dependencies are unavailable

## File Structure Rules

- Main app in `main.py` with lifespan management
- Routers in `routers/` directory (use `APIRouter`)
- Configuration in `config.py` with Pydantic Settings
- Use FastAPI's dependency injection system for shared dependencies
