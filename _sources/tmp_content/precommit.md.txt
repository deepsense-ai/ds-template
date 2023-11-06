(_precommit)=
# Pre-commit hooks and code quality

To ensure code consistency, good practices and remove any code smells we use pre-commit hook along with several linters and other tools.

**pre-commit** is a tool which allows to quickly scan on commit/push code **tracked by git** in the repository, enforcing checks in minimum viable scope - only changed files.

Configuration is in `.pre-commit-config.yaml`, where you can find all tools installed in isolated environment and some of their configuration.
Most of the tools have detailed configuration in `pyproject.toml` file and some might have dedicated file.

All linters run with autofix to reduce manual labor. Developer can review / modify automatic fixes as he needs to re-add and commit affected files.

```{tip}
`pre-commit autoupdate` can be used to update all linters to the most recent version.

`pre-commit run --all-files` runs for all tracked by git files. It usually runs on CI to ensure no files is overlooked.

`pre-commit run pylint --all-files` runs selected tools only - useful for fixing issues.
```

```{warning}
It is important to understand that pre-commit works in it's own virtual environment - this might lead to different behavior of running the same
linter with or without pre-commit due to side effects of some installed locally packages!
```

## `.pre-commit-config.yaml`

**Use scroll on the text inside the below panel**. It contains overview of some tools with an example configuration - it is not exactly the same as in the template.

```{raw} html

    <div id="kodemo-content" style="width:100%;height:525px;display:block;top:0;left:0;padding:0;margin:0"></div>
    <script src="../_static/precommit-tut.js"></script>
    <script src="../_static/kodemo-player.umd.js"></script>

    <script>
      const player = new KodemoPlayer(document.getElementById("kodemo-content"), {layout:"auto"});
      player.load(tutorial_content);
    </script>
```

```{tip}
There are some other great tools, like [ruff](https://github.com/charliermarsh/ruff) - it is fast, but it has not full feature parity with
other linters it tries to replace. However, if your project allows it - please consider to use it instead of pylint, isort etc.
```

## Docker image

To reduce CI stage time we use image created with `docker/precommit/Dockerfile`.

If project is created with GitLab pipelines then automatically it should build & use this image. If you are on different platform you need to configure it yourself.

## mypy - additional information

**mypy** needs special care. Default settings only checks for project issues and works out of box with correctly typed projects.
More strict options are not turned on by default as many data science libraries are not high quality and in practice it leads to 
frustration and minuscule gains in practice.

To discover or ignore what packages you use in a project that are untyped change mypy setting named `ignore_missing_imports=[true|false]`.
Some packages do not have typing information - and this settings raises error for ones which require type package.

To set a package-specific options you can do it this way:

```
[[tool.mypy.overrides]]
module = "foo.*"
...
```

For libraries that require installation of type package you need to perform manual operation specific for each project - you need to modify `.pre-commit-config.yaml` file, here is an example:

```
-   id: mypy
        ...
        # Required to have proper type annotations for external packages.
        additional_dependencies: [
            "fastapi~=0.83.0",
            "numpy~=1.23.3",
        ]
        ...
```

It is highly recommended to do that, as it allows mypy to catch more errors. For code missing type information it always assumes `Any` type.

Sometimes a package do not have any type information nor additional package with it - in that case you can suppress mypy error by manually
marking an exact library to be ignored as mentioned before. 

Please refer to [official mypy documentation](https://mypy.readthedocs.io/en/stable/index.html) for more information.

## jupytext - additional information

Jupyter notebooks are hard to review - to make it easier it is possible to use `jupytext` to convert them to `.py` files (py:percent format) automatically on commit.

If you have not used it before, please read [jupytext documentation](https://jupytext.readthedocs.io/en/latest/).

```{warning}
Do not edit generated files - they will be overwritten by jupytext due to detected differences. 

It is also important to ensure no other linting tool modifies them, as it might lead to endless loop of changes.
```