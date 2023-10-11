# **Cookiecutter template structure**

This is our specific template structure overview. It is highly recommended to learn about cookiecutter first from it's [original documentation](https://cookiecutter.readthedocs.io/en/stable/).

To use template you need `cookiecutter` to be installed (at least >= 2.1.1) and for local development/documentation generation you need to install `requirements.txt`:

```bash
pip install -r requirements.txt
```

Overall list of files can be seen below:

![Presentation of cookiecutter template files](_static/template_files.png)

## cookiecutter.json file

This file is crucial, as it defines questions and key-value substitutions which are applied to template files.

```
cookiecutter.json
```
Internally it uses Jinja template system and allows to use python or some extensions (like `slugify`).

## Hooks

There are two cookiecutter hooks that can be implemented: pre and post project generation.

```
hooks/pre_gen_project.py
hooks/post_gen_project.py
```

- **pre hook** - to validate variables content before cookiecutter generates files.
  - e.g. check if python package name provided by a user is correct
- **post hook** - second allows to clean up unnecessary files that are not needed or run additional code.
  - e.g. remove unnecessary files, fix file permissions etc.

## Project template directory

**All files that can be created by the template** are put there:

```bash
{{ cookiecutter.repo_name }}
```
Cookiecutter asks user for information, copies this directory, applies Jinja substitution and calls hooks defined as python code.

## Tests

We also have a few basic tests to ensure that cookiecutter project can be generated just fine.

In the future we will like to introduce some automating testing of generated project and maybe some example preview.


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
