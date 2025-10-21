# Python Monorepo Structure

The ds-template generates modern Python workspaces using a **monorepo architecture** with multiple packages managed through **uv workspaces**. The system includes several **package type templates** that can be combined to create the optimal project structure for your needs.

## Monorepo Architecture

Generated projects follow a clean monorepo structure:

```
my-project/
├── pyproject.toml          # Workspace configuration
├── mise.toml              # Development environment
├── packages/               # Individual packages
│   ├── my_project_core/   # Core utilities
│   ├── my_project_api/    # API service
│   └── my_project_frontend/ # Frontend application
├── docs/                  # Documentation
└── tests/                 # Shared tests
```

## Monorepo Benefits

The monorepo architecture provides several advantages for modern Python development:

- **Unified codebase** - All related packages in a single repository with shared configuration
- **Atomic changes** - Update multiple packages simultaneously in a single commit
- **Consistent tooling** - Unified linting, testing, and CI/CD across all packages
- **Simplified dependency management** - uv workspace handles inter-package dependencies automatically
- **Independent deployment** - Each package can be deployed separately while sharing common code
- **Easier refactoring** - Move code between packages without breaking external dependencies

## Available Package Types

The template includes several package types organized into three main categories:

### Core Packages
- **Core Package** (`pkg_core`) - Shared utilities, configuration, and common functionality

### Functional Packages
- **API Package** (`pkg_api`) - FastAPI-based REST services with Docker support
- **Worker Package** (`pkg_worker`) - Background task processing with Docker support
- **CLI Package** (`pkg_cli`) - Command-line tools and utilities
- **Library Package** (`pkg_lib`) - Reusable Python libraries

### Frontend Packages
- **Frontend Package** (`pkg_frontend_streamlit`) - Streamlit web applications with branding integration

> **Note:** Frontend packages are connected to a `branding/` directory in the generated project, which contains branding assets and configuration for consistent visual identity across the application.

## Package Features

Each package type includes:

- **Proper Python packaging** with `pyproject.toml`
- **Docker support** (where applicable)
- **Type hints** and documentation
- **Testing setup** with pytest
- **Dependency management** - Inter-package dependencies handled automatically by uv workspace
- **External dependencies** managed per package in their `pyproject.toml`
- **AI-powered generation** selects appropriate packages based on your description

## Configuration

The workspace is configured through:
- **Root `pyproject.toml`** - Workspace settings and shared dev dependencies
- **Package `pyproject.toml`** - Individual package configuration
- **`mise.toml`** - Development environment management

For detailed configuration options, see the `[tool.uv.workspace]` and `[tool.uv]` sections in your project's `pyproject.toml` file.