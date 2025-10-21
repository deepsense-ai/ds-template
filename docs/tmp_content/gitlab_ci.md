# GitLab CI Configuration

This is an **optional** template option that creates a comprehensive CI/CD pipeline for your project.

## What's Included

The GitLab CI pipeline includes seven stages:

1. **Preparation** - Docker image building and caching
2. **Lint** - Code quality and style checks
3. **Test** - Unit testing and coverage analysis
4. **Package** - Python package building
5. **Pages** - Documentation generation
6. **Security** - Vulnerability scanning
7. **Deploy** - Artifact deployment and publishing

```{note}
To reduce computations and costs, CI is only executed on Merge Requests and the default branch.
Most jobs can be interrupted by newer code changes using the `interruptible: true` flag.
```

## Modern Tooling Integration

### Ruff for Code Quality
The pipeline uses **Ruff** for fast, comprehensive code quality checks:
- **Unified linting** - Replaces multiple individual tools
- **Automatic formatting** - Black-compatible code formatting
- **Import sorting** - isort-compatible import organization
- **Security scanning** - bandit-compatible security checks

### uv Package Management
Modern Python package management with **uv**:
- **Fast dependency resolution** - Significantly faster than pip
- **Workspace support** - Monorepo package management
- **Lock file generation** - Reproducible builds
- **Cross-platform compatibility** - Works on all platforms

### MkDocs Documentation
Modern documentation generation with **MkDocs**:
- **Material theme** - Professional documentation appearance
- **Interactive features** - Search, navigation, diagrams
- **Auto-generation** - Package documentation and API references
- **GitLab Pages** - Automatic documentation hosting

## Pipeline Stages

### Merge Request Pipeline
When a developer opens a Merge Request, the pipeline runs:
- **Lint stage** - Code quality and style validation
- **Test stage** - Unit testing and coverage analysis
- **Package stage** - Python package building
- **Security stage** - Vulnerability scanning

![Merge Request stages](../_static/stages_mr.png)

### Main Branch Pipeline
After merge completion, additional stages execute:
- **Pages stage** - Documentation generation and hosting
- **Deploy stage** - Artifact deployment and publishing
- **Manual triggers** - Optional package releases

![Main branch stage](../_static/stages_main.png)

### Docker Image Management
When pre-commit configuration changes, a preparation stage builds Docker images:
- **Image building** - Creates optimized pre-commit environment
- **Registry upload** - Stores images in GitLab Container Registry
- **Caching** - Reduces build times for subsequent runs
- **Versioning** - Tags images with commit SHA and latest

![Preparation stage](../_static/stage_preparation.png)

The Docker image is defined as `PRECOMMIT_IMAGE: $CI_REGISTRY_IMAGE/precommit` and includes:
- **Pre-commit hooks** - All linting and formatting tools
- **uv package manager** - Fast dependency management
- **Python environment** - Configured Python runtime

## Detailed Stage Information

### Preparation Stage
- **Purpose**: Build and cache Docker images for faster subsequent runs
- **Triggers**: Changes to `docker/precommit/Dockerfile` or pre-commit configuration
- **Duration**: 3-5 minutes for initial build, faster with caching
- **Output**: Docker image with pre-commit environment and tools

### Lint Stage
- **Purpose**: Code quality and style validation
- **Tools**: Ruff (linting, formatting, import sorting), mypy (type checking), bandit (security)
- **Duration**: ~20 seconds with Docker image, ~2 minutes without
- **Output**: Code quality reports and formatted code

### Test Stage
- **Purpose**: Unit testing and coverage analysis
- **Tools**: pytest with coverage reporting
- **Coverage**: 
  - ![Code coverage](../_static/coverage.png)
  - Red lines = not covered, green lines = covered
  - Percentage coverage reporting
  - ![Tests](../_static/tests.png)
- **License checking**: Validates package licenses against allowlist
- **Artifacts**: Test results, coverage reports, license information

### Package Stage
- **Purpose**: Build Python packages for distribution
- **Tools**: uv build for modern package building
- **Output**: Wheel (.whl) and source distribution (.tar.gz) files
- **Artifacts**: Built packages available for download

### Pages Stage
- **Purpose**: Generate and host documentation
- **Tools**: MkDocs with Material theme
- **Features**: Interactive documentation with search and navigation
- **Output**: Static documentation site hosted on GitLab Pages
- **Package info**: ![Licenses in documentation](../_static/docs_lic.png)

### Security Stage
- **Purpose**: Vulnerability scanning and security analysis
- **Tools**: Trivy for comprehensive security scanning
- **Compliance**: Required for SOC 2 Certification
- **Output**: Security reports in JSON and HTML formats
- **Artifacts**: Detailed vulnerability information

### Deploy Stage (Main Branch Only)
- **Purpose**: Deploy artifacts and publish packages
- **Documentation**: Uploads to GitLab Pages for team access
- **Packages**: Uploads to GitLab Package Registry
- **Manual triggers**: Optional package releases
- **Output**: ![Package in registry](../_static/pip_reg.png)

## Artifacts and Reports

![Artifacts](../_static/artifacts.png)

The pipeline generates comprehensive artifacts for analysis and deployment:

### Test Artifacts
- **licenses.txt** - Detected package licenses and compliance information
- **requirements-freeze.txt** - Pinned package versions for reproducible builds
- **dist/** - Built Python packages (wheel and source distributions)
- **coverage.xml** - Code coverage data in XML format
- **test-results.xml** - JUnit XML test results

### Security Artifacts
- **trivy-report.json** - Security scan results in JSON format
- **trivy-report.txt** - Human-readable security report
- **dependency-scanning** - GitLab dependency scanning integration

### Documentation Artifacts
- **public/** - Generated MkDocs documentation site
- **Package information** - License and dependency documentation

## License Validation

The pipeline includes automated license checking using `pip-licenses`:

- **License extraction** - Automatically detects package licenses
- **Allowlist validation** - Checks against approved licenses in `.license-whitelist.txt`
- **Exception handling** - Exempted libraries in `.libraries-whitelist.txt`
- **CI integration** - Fails pipeline on license violations

### Configuration Files
- **`.license-whitelist.txt`** - Approved licenses (one per line)
- **`.libraries-whitelist.txt`** - Exempted libraries (single line)

```{warning}
`.license-whitelist.txt` must have a license in each distinct line.

`.libraries-whitelist.txt` must be contained in single line (e.g. "foo bar").
```

## GitLab Integration

### GitLab Pages
Static documentation hosting with automatic deployment:
- **Job name**: Must be `pages` for automatic hosting
- **Documentation**: MkDocs-generated site with Material theme
- **Access**: Available to all project members
- **Custom domain**: Can be configured for custom URLs

### GitLab Package Registry
Python package distribution and storage:
- **Manual triggers** - Package uploads require manual approval
- **Version management** - Automatic versioning and tagging
- **Private registry** - Secure package storage
- **Integration** - Works with pip and uv package managers

### GitLab Container Registry
Docker image storage and management:
- **Pre-commit images** - Optimized development environments
- **Versioning** - SHA-tagged and latest images
- **Caching** - Faster subsequent builds
- **Security** - Private image storage

## Best Practices

### YAML Configuration
1. **Use YAML validator** in your editor for syntax checking
2. **Test on branches** - Create temporary repositories for testing
3. **Use GitLab validator** - [CI Lint tool](https://docs.gitlab.com/ee/ci/lint.html)
4. **Add conditions last** - Test jobs before adding `if` conditions

### Pipeline Optimization
- **Docker caching** - Use prepared images for faster builds
- **Parallel jobs** - Run independent jobs simultaneously
- **Artifact management** - Clean up old artifacts regularly
- **Resource limits** - Set appropriate resource constraints

### Security Considerations
- **Secret management** - Use GitLab CI/CD variables for sensitive data
- **Access control** - Limit pipeline access to authorized users
- **Vulnerability scanning** - Regular security assessments
- **Compliance** - Maintain SOC 2 certification requirements

