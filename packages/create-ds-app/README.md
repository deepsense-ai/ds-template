# Create DS App

Set up a modern data science project by running one command.

## Installation

```bash
pip install -e packages/create_ds_app
```

## Usage

```bash
# Interactive mode - prompts for all options
create-ds-app

# Create a monorepo project
create-ds-app --template monorepo_base

# Create a package library
create-ds-app --template pkg_lib --project-name my-lib

# Create a CLI package
create-ds-app --template pkg_cli
```

## Templates

This package uses `ds-templater` for template management and includes:

- `monorepo_base`: Base monorepo structure
- `pkg_lib`: Python library package template
- `pkg_cli`: CLI application template

## Customization

Templates are defined in the `templates/` directory. Each template includes:
- `template_config.py`: Configuration and questions
- Template files with Jinja2 syntax