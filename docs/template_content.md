# Template Content

This section provides comprehensive information about what's included in generated projects and how the template system works.

## Generated Project Structure

When you generate a project with ds-template, you get a modern Python workspace with:

### 1. Modern Python Workspace
- **`pyproject.toml`** - Modern Python project configuration with uv workspace support
- **`mise.toml`** - Development environment management and tool versioning
- **`packages/`** - Multi-package monorepo structure with individual package templates
- **`docs/`** - Documentation source with MkDocs configuration

### 2. Code Quality & Testing
- **Ruff** - Fast linting, formatting, and security scanning
- **mypy** - Type checking and validation
- **pytest** - Modern testing framework with coverage reporting

For detailed code quality configuration, see [Code Quality](tmp_content/precommit.md).

### 3. Documentation (MkDocs with Material theme)
- **Modern documentation** - MkDocs with Material Design theme
- **Interactive features** - Search, navigation, Mermaid diagrams, and tabs
- **Auto-generated content** - Package documentation and API references
- **Custom styling** - Branded documentation appearance and theming

### 4. CI/CD Integration (Optional)
Choose from three options:

- **GitHub Actions** - Comprehensive workflows with security scanning and package building
- **GitLab CI** - Multi-stage pipeline with Docker support and package registry
- **No CI** - Local development only with all tools available

For detailed CI/CD configuration, see [GitHub CI](tmp_content/github_ci.md) or [GitLab CI](tmp_content/gitlab_ci.md).

### 5. Development Tools
- **uv** - Fast Python package manager and project management
- **mise** - Development environment management and tool versioning
- **License checking** - Automated license compliance validation
- **Docker support** - Pre-commit Docker image for consistent environments
- **Scripts** - Utility scripts for package creation and management

Mise is used both in the ds-template project itself and in all generated projects. See [Development Tools](tmp_content/mise.md) for detailed setup and usage instructions.

### 6. AI-Powered Features
- **Intelligent project generation** - Describe your project and let AI create the structure
- **Interactive customization** - Claude Code integration for project adaptation
- **Template-based packages** - AI selects appropriate package types from available templates
- **Real-time assistance** - Get help with implementation and customization

## Template System

The system includes several proven package templates for different use cases, using Jinja2 templating for dynamic content generation based on user input. All template files are organized in the `templates/` directory with individual package templates for different use cases.

For detailed information about each package type and monorepo structure, see [Python Structure](tmp_content/python_structure.md).

## Detailed Documentation

- [Python Structure](tmp_content/python_structure.md) - Monorepo and package organization
- [Code Quality](tmp_content/precommit.md) - Ruff-based linting and formatting
- [Development Tools](tmp_content/mise.md) - Environment management and tooling
- [GitLab CI](tmp_content/gitlab_ci.md) - GitLab CI/CD pipeline configuration
- [GitHub CI](tmp_content/github_ci.md) - GitHub Actions workflow configuration
- [Semantic Versioning](tmp_content/semver_package.md) - Version management and packaging

The generated project provides a solid foundation for professional data science and Python development with modern tooling and best practices built-in.

