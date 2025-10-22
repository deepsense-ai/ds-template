# GitHub Actions CI

This template creates CI/CD workflows with three main workflows: **CI**, **Release**, and **Documentation**.

## Workflows

### CI Workflow

#### Lint Job
- **Purpose**: Code quality and style validation
- **Tools**: Ruff (linting), mypy (type checking), license checking
- **Triggers**: Push/PR to main/develop branches

#### Test Job
- **Purpose**: Unit testing and coverage analysis
- **Tools**: pytest with coverage reporting
- **Artifacts**: Coverage reports uploaded to Codecov
- **Triggers**: Push/PR to main/develop branches

#### Security Job
- **Purpose**: Vulnerability scanning and security analysis
- **Tools**: Trivy for comprehensive security scanning
- **Output**: Security reports in SARIF format
- **Triggers**: Push/PR to main/develop branches

#### Build Job
- **Purpose**: Package building and artifact generation
- **Tools**: uv build for modern package building
- **Artifacts**: dist/ packages uploaded as GitHub artifacts
- **Triggers**: Push/PR to main/develop branches (after lint/test)

### Release Workflow

#### Release Job
- **Purpose**: Package publishing and release management
- **Tools**: uv build, PyPI publishing, GitHub releases
- **Features**: PyPI publishing, GitHub releases
- **Triggers**: Version tags (v*)

### Documentation Workflow

#### Docs Job
- **Purpose**: Generate and host documentation
- **Tools**: MkDocs with Material theme
- **Output**: Documentation site deployed to GitHub Pages
- **Triggers**: Push to main branch

## Key Features

- **Modern tooling**: Ruff, uv, MkDocs
- **Coverage reporting**
- **Build artifacts**
- **Security scanning**: Trivy with SARIF reporting
- **License validation**: Automated compliance checking
