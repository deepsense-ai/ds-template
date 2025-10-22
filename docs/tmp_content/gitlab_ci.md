# GitLab CI Configuration

This is an **optional** template option that creates a CI/CD pipeline for your project.

## What's Included

The GitLab CI pipeline includes four stages:

1. **Lint** - Code quality and style checks
2. **Test** - Unit testing and coverage analysis  
3. **Security** - Vulnerability scanning
4. **Pages** - Documentation generation

## Pipeline Stages

### Lint Stage
- **Purpose**: Code quality and style validation
- **Tools**: Ruff (linting), mypy (type checking), license checking
- **Triggers**: Merge requests, main, and develop branches

### Test Stage
- **Purpose**: Unit testing and coverage analysis
- **Tools**: pytest with coverage reporting
- **Artifacts**: Test results, coverage reports, license information
- **Triggers**: Merge requests, main, and develop branches

### Security Stage
- **Purpose**: Vulnerability scanning and security analysis
- **Tools**: Trivy for comprehensive security scanning
- **Output**: Security reports in SARIF format
- **Artifacts**: trivy-results.sarif
- **Triggers**: All branches and commits

### Pages Stage
- **Purpose**: Generate and host documentation
- **Tools**: MkDocs with Material theme
- **Output**: Documentation site hosted on GitLab Pages
- **Triggers**: Main branch only
