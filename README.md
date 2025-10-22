# [deepsense.ai](https://deepsense.ai) Project Template 

Useful template to bootstrap new professional data science and python projects.

[Documentation](https://deepsense-ai.github.io/ds-template/)

##### Table of Contents  
* [What is it?](#what-is-it)  
* [What are the benefits?](#what-are-the-benefits)
* [Getting started](#getting-started)  

# What is it?

A comprehensive project template generator for data science and Python projects, which generates basic, 
most common configuration using proven templates.

It is a result of our experiences with building data science projects and is a part of our internal best practices, however it is not a silver bullet and should be treated as a starting point for your project.
Especially some settings might be less/more restrictive than you need, but we believe it is better to start with a good baseline and modify it later than to start from scratch.

# What are the benefits?

Generated project consists of:

1. **Modern Python Workspace Structure**:
    * `pyproject.toml` - modern Python project configuration with uv workspace support
    * `mise.toml` - development environment management
    * `packages/` directory for multi-package monorepo structure
    * Individual package templates (API, CLI, Core, Frontend, Worker, Library)

2. **Code Quality & Linting** (via Ruff):
    * **Code formatting** - automatic code formatting
    * **Import sorting** - organized import statements
    * **Type checking** - mypy integration for type safety
    * **Security scanning** - bandit for security vulnerability detection
    * **Code style** - comprehensive linting rules (pycodestyle, pyflakes, pylint, etc.)
    * **Documentation** - pydocstyle for docstring standards
    * **Modernization** - pyupgrade for Python version compatibility

3. **Testing & Coverage**:
    * **pytest** - modern testing framework with async support
    * **Coverage reporting** - comprehensive test coverage analysis
    * **Test discovery** - automatic test detection and execution

4. **Documentation** (MkDocs with Material theme):
    * **Modern documentation** - MkDocs with Material Design theme
    * **Interactive features** - search, navigation, Mermaid diagrams
    * **Auto-generated content** - package documentation and API references
    * **Custom styling** - branded documentation appearance

5. **CI/CD Integration** (optional - choose GitHub, GitLab, or None):
    * **GitHub Actions** (if selected):
        - Automated linting and testing on every push/PR
        - Security scanning with Trivy
        - Package building and artifact upload
        - Code coverage reporting
    * **GitLab CI** (if selected):
        - Multi-stage pipeline (lint, test, package, pages, security, deploy)
        - Docker-based pre-commit image for faster builds
        - GitLab Pages documentation hosting
        - Package registry integration
        - Security vulnerability scanning

6. **Development Tools**:
    * **uv** - fast Python package manager and project management
    * **License checking** - automated license compliance validation
    * **Docker support** - pre-commit Docker image for consistent environments
    * **Scripts** - utility scripts for package creation and management

Most up-to date descriptions, tips and explanations are in the [documentation](https://deepsense-ai.github.io/ds-template/).

# Getting started

## Usage

```bash
# Create a new data science application
uvx ds-template
```
Select from predefined package types and generate a standard project structure

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/deepsense-ai/ds-template.git
cd ds-template

# Install dependencies
uv sync

# Run the CLI
uv run ds-template
```

## Creating Custom Templates

Templates are stored in the `templates/` directory. Each template consists of:

1. A directory with the template name
2. A `template_config.py` file with template metadata and questions
3. Template files, with `.j2` extension for files that should be processed as Jinja2 templates

Available variables in templates:
- `project_name`: Name of the project
- `pkg_name`: Name of the python package
- `python_version`: Python version
- Custom variables from template questions
