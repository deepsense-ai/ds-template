# GitHub Actions CI

This is an **optional** template option that creates comprehensive CI workflows for your project.

## What's Included

The GitHub Actions workflow includes four main jobs:

### 1. **Lint and Static Analysis**
- **Ruff** - Fast linting and formatting checks
- **mypy** - Type checking and type safety validation
- **bandit** - Security vulnerability scanning
- **License checking** - Validates package licenses against allowlist

### 2. **Unit Tests**
- **pytest** - Comprehensive test suite execution
- **Coverage reporting** - Code coverage analysis and reporting
- **Multi-Python support** - Tests across Python versions
- **Test artifacts** - JUnit XML reports for GitHub integration

### 3. **Security Scanning**
- **Trivy** - Container and filesystem vulnerability scanning
- **SARIF reporting** - Security results integration with GitHub Security tab
- **Dependency scanning** - Third-party package vulnerability detection

### 4. **Package Building**
- **uv build** - Modern Python package building
- **Artifact upload** - Built packages available for download
- **Multi-platform support** - Cross-platform package compatibility

![Main CI workflow](../_static/gh.png)

## Modern Tooling

### Ruff Integration
The workflow uses **Ruff** for fast, comprehensive code quality checks:
- **10-100x faster** than traditional linters
- **Unified tooling** - replaces black, isort, flake8, pylint
- **Automatic fixes** - Many issues can be auto-corrected
- **Comprehensive rules** - Style, logic, security, and documentation

### uv Package Management
Modern Python package management with **uv**:
- **Fast dependency resolution** - Significantly faster than pip
- **Workspace support** - Monorepo package management
- **Lock file generation** - Reproducible builds
- **Cross-platform compatibility** - Works on all platforms

### Code Coverage

Default code coverage setup uses Codecov integration:
- **Coverage reporting** - Detailed coverage metrics
- **PR comments** - Coverage changes in pull requests
- **Coverage badges** - Visual coverage status
- **Historical tracking** - Coverage trends over time

![Code coverage comment preview](../_static/gh_coverage.png)

## Artifacts

Generated artifacts available for download from GitHub UI:

![Github artifacts](../_static/gh_artifacts.png)

### Build Artifacts
- **dist/** - Built Python packages (wheel and source distribution)
- **Coverage reports** - HTML and XML coverage reports
- **Test results** - JUnit XML test reports

### Security Artifacts
- **trivy-results.sarif** - Security scan results in SARIF format
- **Security reports** - Detailed vulnerability information

### License Artifacts
- **licenses.txt** - Detected package licenses
- **License validation** - Compliance checking results

## License Validation

The workflow includes automated license checking:

- **pip-licenses** - Extracts package license information
- **Allowlist validation** - Checks against approved licenses
- **Compliance reporting** - Detailed license analysis
- **CI integration** - Fails build on license violations

### Configuration Files
- **`.license-whitelist.txt`** - Approved licenses (one per line)
- **`.libraries-whitelist.txt`** - Exempted libraries (single line)

```{warning}
`.license-whitelist.txt` must have a license in each distinct line.

`.libraries-whitelist.txt` must be contained in single line (e.g. "foo bar").
```

## GitHub Actions hints

Please get familiar with official documentation before you modify the yaml configuration.

Changing YAML is error-prone so here are protips:

1. Visual Studio Code (and maybe other editors too) have an extension which helps with Github Actions - it can be found [here](https://marketplace.visualstudio.com/items?itemName=cschleiden.vscode-github-actions).
1. Use YAML validator in your editor to fix wrong whitespaces.
1. Operate on branch first or create a temporary test repository.
1. `if` and similar conditions should be added last, after testing a job.

## Workflow Features

### Multi-Python Support
The workflow supports multiple Python versions:
- **Python 3.11** - Minimum supported version
- **Python 3.12** - Current stable version  
- **Python 3.13** - Latest version

### Monorepo Support
- **Workspace management** - Handles multiple packages
- **Package-specific testing** - Tests individual packages
- **Dependency resolution** - Manages inter-package dependencies
- **Selective building** - Builds only changed packages

### Security Integration
- **Trivy scanning** - Comprehensive vulnerability detection
- **SARIF reporting** - GitHub Security tab integration
- **Dependency scanning** - Third-party package analysis
- **License compliance** - Automated license validation

## GitHub Actions Tips

Please get familiar with official documentation before modifying YAML configuration.

### Best Practices
1. **Visual Studio Code** has a GitHub Actions extension for YAML validation
2. **Use YAML validator** in your editor to fix whitespace issues
3. **Test on branches** - Create temporary repositories for testing
4. **Add conditions last** - Test jobs before adding `if` conditions
5. **Use marketplace actions** - Prefer official and well-maintained actions

### Common Modifications
- **Add Python versions** - Extend matrix strategy
- **Modify triggers** - Change `on` conditions
- **Add environment variables** - Use `env` section
- **Customize artifacts** - Modify `artifacts` configuration