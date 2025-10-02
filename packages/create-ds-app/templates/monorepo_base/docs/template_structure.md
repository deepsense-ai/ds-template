# **Template structure**

This is our specific template structure overview. The template uses Jinja2 templating system for file generation.

To use the template you need `uvx` to be installed and for local development/documentation generation you need to install dependencies:

```bash
pip install -r requirements.txt
```

Overall list of files can be seen below:

![Presentation of template files](_static/template_files.png)

## Template configuration

The template uses a configuration system that defines questions and key-value substitutions which are applied to template files.

```
template_config.py
```
Internally it uses Jinja template system and allows to use python or some extensions (like `slugify`).

## Template processing

The template system processes files and applies Jinja2 substitutions based on user input.

- **Pre-processing** - validates variables content before generating files
  - e.g. check if python package name provided by a user is correct
- **Post-processing** - allows to clean up unnecessary files or run additional code
  - e.g. remove unnecessary files, fix file permissions etc.

## Template directories

**All files that can be created by the template** are organized in template directories:

```bash
templates/
├── monorepo_base/
├── pkg_cli/
└── pkg_lib/
```
The create-ds-app tool asks user for information, copies template files, applies Jinja substitution and processes the generated project.

## Tests

We also have a few basic tests to ensure that the template project can be generated correctly.

In the future we will like to introduce some automated testing of generated project and maybe some example preview.


## Documentation

Actually what are you reading just now :)

We use Sphinx documentation and content is in `docs/` directory and it is hosted [on GitHub Pages](https://deepsense-ai.github.io/ds-template//).

To build locally:
```bash
# ensure you have sphinx and related packages installed first:
pip install -r requirements.txt
# then you can build with one command:
./build_docs.sh
# now open public/index.html
```
