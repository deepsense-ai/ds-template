# Semantic Versioning & Packaging

The ds-template includes semantic versioning support for distributing your Python packages.

## What's Included

### Semantic Versioning
- **Standard versioning** using `major.minor.patch` scheme
- **Development versions** with `dev` suffix for pre-release packages
- **Automated versioning** through CI/CD pipelines
- **Version file** for easy inspection and automation

### Package Building
- **Modern packaging** with `pyproject.toml` configuration
- **uv build** for fast, reliable package building
- **Multi-platform support** for different operating systems
- **Dependency management** with lock files for reproducible builds

## Version Management

### Development Workflow
```bash
# Check current version
cat src/my_package/VERSION

# Build package
uv build

# Install locally for testing
uv pip install dist/my_package-0.1.0-py3-none-any.whl
```

### CI/CD Integration
- **GitHub Actions** automatically builds and uploads packages
- **GitLab CI** publishes to GitLab Package Registry
- **Version tagging** creates releases automatically
- **Development builds** include build numbers

## Configuration

Version management is configured in:
- **`pyproject.toml`** - Package metadata and build settings
- **`VERSION` file** - Current version number
- **CI/CD workflows** - Automated versioning and publishing

## Publishing

### GitHub Packages
- **Automatic publishing** on version tags
- **Public or private** package repositories
- **Easy installation** with `uv pip install`

### GitLab Package Registry
- **Private package registry** for internal use
- **Manual deployment** for development versions
- **Release deployment** for stable versions

## Best Practices

- **Use semantic versioning** for all packages you plan to distribute
- **Tag releases** with version numbers (e.g., `v1.0.0`)
- **Test packages** before publishing
- **Document changes** in release notes

For detailed versioning configuration, see the `[project]` section in your package's `pyproject.toml` file.