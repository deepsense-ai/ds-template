# Project Structure

## Directory Structure

```
{{ project_name | lower | replace('_', '-') }}/
{% if ci == "GitHub" %}├── .github/workflows/         # CI/CD workflows
{% elif ci == "GitLab" %}├── .gitlab-ci.yml             # GitLab CI configuration
{% endif %}├── docs/                      # Documentation
├── src/{{ pkg_name }}/        # Main package
│   ├── __init__.py
│   ├── cli.py                # CLI interface
│   └── core.py               # Core functionality
├── tests/                     # Test suite
├── pyproject.toml            # Project configuration
└── README.md
```

## Key Files

- **`src/{{ pkg_name }}/`** - Main Python package
- **`tests/`** - Test files
- **`pyproject.toml`** - Dependencies and configuration
{% if ci == "GitHub" %}- **`.github/workflows/`** - CI/CD automation
{% elif ci == "GitLab" %}- **`.gitlab-ci.yml`** - GitLab CI configuration
{% endif %}
