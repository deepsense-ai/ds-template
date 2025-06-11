# {{cookiecutter.project_name}}

Repository is created with deepsense.ai project template boilerplate. Adapt to your needs.
Documentation is available at [https://deepsense-ai.github.io/ds-template/](https://deepsense-ai.github.io/ds-template/).


# Setup developer environment

To start, you need to setup your local machine.

## Setup venv

You need to setup virtual environment, simplest way is to run from project root directory:

```bash
$ . ./setup_dev_env.sh
```

This will create a new venv, install dependencies and activate the environment.

## Install pre-commit

To ensure code quality we use pre-commit hook with several checks. Setup it by:

```
pre-commit install
```

All updated files will be reformatted and linted before the commit.

To reformat and lint all files in the project, use:

```
pre-commit run --all-files
```

The used linters are configured in `.pre-commit-config.yaml`. You can use `pre-commit autoupdate` to bump tools to the latest versions.

# Work with the project

## Manage dependencies

The project uses `uv`, a fast and modern Python package manager that manages dependencies via the `pyproject.toml` file.

### Add dependencies

To add a new package and update the `pyproject.toml` and `uv.lock` files, use:

```bash
uv add <package-name>
```

You can also specify versions, extras, or assign to specific groups:

```bash
uv add requests==2.31.0     # specific version  
uv add fastapi[all]         # with extras  
uv add --dev pytest         # dev-only dependencies  
uv add --group foo uvicorn  # custom group from [dependency-groups]
```

### Remove dependencies

To remove a package and clean up both `pyproject.toml` and `uv.lock` files, use:

```bash
uv remove <package-name>
```

Example:

```bash
uv remove pandas
```

### Lock & install dependencies

Dependency metadata can also be updated manually by editing the `pyproject.toml` file directly.
After making changes, run the following commands to update the `uv.lock` file and install the dependencies:

```bash
uv lock
uv sync
```

You can also sync specific groups:

```bash
uv sync --dev        # development dependencies  
uv sync --group foo  # custom dependency group in dependency-groups
```

## Autoreload within notebooks

When you install project's package add below code (before imports) in your notebook:
```
# Load the "autoreload" extension
%load_ext autoreload
# Change mode to always reload modules: you change code in src, it gets loaded
%autoreload 2
```
Read more about different modes in [documentation](https://ipython.org/ipython-doc/3/config/extensions/autoreload.html).

All code should be in `src/` to make reusability and review straightforward, keep notebooks simple for exploratory data analysis.
See also [Cookiecutter Data Science opinion](https://drivendata.github.io/cookiecutter-data-science/#notebooks-are-for-exploration-and-communication).

{%- if cookiecutter.docs != "No docs" %}
# Project documentation

In `docs/` directory are Sphinx RST/Markdown files.

To build documentation locally, in your configured environment, you can use `build_docs.sh` script:

```bash
$ ./build_docs.sh
```

Then open `public/index.html` file.

Please read the official [Sphinx documentation](https://www.sphinx-doc.org/en/master/) for more details.
{% endif -%}

{% if cookiecutter.ci == "GitLab" %}

### GitLab Pages Documentation

By default **Gitlab** pipelines have `pages` step which will build sphinx documentation automatically on main branch - and it will push it to **GitLab Pages** to be statically hosted.

To access it, you need to have a link, which can be found on **GitLab -> Settings -> Pages** page.

Only people with repository access can view it.

Please read more about it [here](https://docs.gitlab.com/ee/user/project/pages/index.html).

{%- endif -%}

{%- if cookiecutter.ci == "Github" %}

### Github Actions Documentation

By default **Github Actions** pipelines have `documentation` workflow which will build sphinx documentation automatically on main branch - and it will push it to a branch - it can be hosted on **Github Pages** if you enable it.

To access it, you need to enable it, on **Github repository -> Settings -> Pages** page select **Deploy from a branch** and select **gh-pages**. Link will appear here after deployment.

**WARNING:** Only on Github Enterprise you can make it private so only people with repository access can view it.

Please read more about it [here](https://docs.github.com/en/pages/quickstart).

{%- endif -%}

{%- if cookiecutter.jupytext == "Yes" %}

# Jupyter notebooks and jupytext

To make notebooks more friendly for code review and version control we use `jupytext` to sync notebooks with python files. If you have not used it before, please read [jupytext documentation](https://jupytext.readthedocs.io/en/latest/).

There is pre-commit hook which automatically generates and syncs notebooks with python files on each commit.

Please ensure you do not edit/modify manually or by other means generated py:percent files as they will conflict with jupytext change detection and lead to endless loop.
Treat them as read-only files and edit only notebooks.

{%- endif -%}

{%- if cookiecutter.versioning == "Bumpversion" %}
# Semantic version bump

To bump version of the library please use `bump2version` which will update all version strings.

NOTE: Configuration is in `.bumpversion.cfg` and **this is a main file defining version which should be updated only with bump2version**.

For convenience there is bash script which will create commit, to use it call:

```bash
# to create a new commit by increasing one semvar:
$ ./bump_version.sh minor
$ ./bump_version.sh major
$ ./bump_version.sh patch
# to see what is going to change run:
$ ./bump_version.sh --dry-run major
```
Script updates the **VERSION** and `pyproject.toml` files to match the new version.

You can configure it to update version string in other files as well - please check out the bump2version configuration file.
{% endif -%}

{% if cookiecutter.ci == "GitLab" %}

On GitLab CI, you can build development, test package and upload it manually as minor.major.patch-dev{BUILD_NUMBER} to PIP registry.

Every MR keeps package for 7 days each (check `package` artifact).

On the main branch you can trigger _release_ which uploads minor.major.patch version to PIP registry.

{% endif %}
