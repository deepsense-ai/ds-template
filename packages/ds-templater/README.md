# DS Templater

Template management system for data science projects. Provides APIs for:

- Registering new templates
- Configuring default template groups
- Managing template questions and context
- Rendering templates with Jinja2
- Custom file inclusion logic

## Installation

```bash
pip install -e packages/ds_templater
```

## Usage

```python
from ds_templater import TemplateRegistry, TemplateConfig

# Register a template
registry = TemplateRegistry()
registry.register_template(MyTemplateConfig())

# Get available templates
templates = registry.get_templates(group="monorepo")
```