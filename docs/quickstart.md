# Quick Start

This template is the result of our experiences at [deepsense.ai](https://deepsense.ai/) with building AI projects and represents our internal best practices. While some settings might be more or less restrictive than you need, we believe it's better to start with a solid baseline and modify it later than to start from scratch.

The AI-powered features bridge the gap between high-level project vision and implementation details, making it easier to bootstrap complex data science projects while maintaining flexibility for customization.

Get up and running with ds-template in minutes using either traditional template generation or AI-powered project creation.

## Prerequisites

- **Python 3.11+** installed on your system
- **uv** package manager
- **Git** for version control

## Installation

No installation required! Use `uvx` to run the tool directly:

```bash
uvx create-ds-app
```

## Project Generation Workflow

When you run `uvx ds-template`, you'll be guided through this process:

### Step 1: Basic Questions
1. **Project name**
2. **Python version** 
3. **CI/CD provider selection:** GitHub, GitLab, or None

### Step 2:Template Generation

1. **Select which packages** you want to include (e.g., `core`, `api`, `frontend`)
2. **Generate initial project** with selected components

> **Note:**  
> The generated project is a solid starting point and should be treated as a demo or basic skeleton. You'll likely want to tailor it to your real-world needs!

---


## Generated Project Structure

After generation, you'll get a modern Python workspace with:

```
my-project/
├── pyproject.toml          # Modern Python project configuration
├── mise.toml              # Development environment management
├── mkdocs.yml             # Documentation configuration
├── packages/              # Multi-package monorepo structure
│   ├── my_project_core/   # Core utilities and configuration
│   ├── my_project_api/    # FastAPI service (if selected)
│   └── my_project_frontend/ # Streamlit dashboard (if selected)
├── docs/                  # Documentation source
├── tests/                 # Test suite
└── .github/               # CI/CD workflows (if GitHub selected)
```

## Next Steps

### 1. Install Dependencies

```bash
cd my-project
uv sync  # Install all dependencies
```

### 2. Run Development Environment

```bash
mise install  # Set up development environment
mise trust    # Mark this project as trusted to enable automatic activation and hooks in mise
```

> **Note:** Mise is used for development environment management. See [Development Tools](tmp_content/mise.md) for detailed setup instructions.

### 3. Start Development

```bash
# Run tests
uv run pytest

# Check code quality
uv run ruff check .

# Start development server (if API package)
uv run python -m my_project_api.main

# Start frontend (if Streamlit package)
uv run streamlit run my_project_frontend/app.py
```

### 4. Customize Your Project

- **Edit configuration** in `pyproject.toml`
- **Add your code** in the appropriate package directories
- **Update documentation** in the `docs/` folder
- **Configure CI/CD** in `.github/` or `.gitlab-ci.yml`

## Repository Setup

### Option 1: Generate First, Then Connect

```bash
# Generate project
uvx ds-templte
cd my-project

# Initialize git and connect to remote
git init
git remote add origin <your-repo-url>
git add .
git commit -m "Initial project setup with ds-template"
git push -u origin main
```

### Option 2: Clone Empty Repo First

```bash
# Clone empty repository
git clone <your-repo-url>
cd my-repo

# Generate project in existing directory
uvx ds-templte
# Follow prompts, ensure project name matches repo name

# Commit and push
git add .
git commit -m "Initial project setup with ds-template"
git push origin main
```

## Learn More
- [Template Content](template_content.md) - What's included in generated projects
