# Python code structure

It is really very basic python package based on [src-based approach](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
Aside of advantages mentioned under the provided link, this structure is preferred due to the following internal reasons:
- `src/` becomes standard interface for people to look for
- easier for templating: tools can be easily configured to target `src/` - no need to configure on the fly or hardcode package name
- later can evolved into multi module project.

## Why python package

Having python package allows to much easier sharing and reusing code. It also reduces headache with hardcoding paths and with proper testing it can capture issues with missing or incompatible dependencies (as PIP does not solve versions with already installed packages.)

```{Tip}
In one project we might work on training and inference code together with some frontend.

Python package can ship with code such that:

`pip install magic[train]` installs all dependencies for training.

`pip install magic` installs onnx + other inference code.

Then if you have FastAPI or Streamlit app you install _lean_ package which reduces docker size.
It also enables sharing with other users.
```

`requirements-dev.txt` is used to keep track of packages used in development (developer use only).

The structure of python package is:

- `setup.cfg` - the most interesting file: declares package metadata, install dependencies etc.
- `setup.py` - almost empty, it is used to ensure `pip -e .` works due to legacy reasons.
- `src/` directory for all code.
    - _any package name_
        - `__init__.py`
        - `__version__.py`
        - `VERSION`
        - _any python code_
    - `py.typed` - empty file signals to mypy that type annotations are present in python code.
- `MANIFEST.in` - optional, used to include non-python files in package (like `py.typed` or `*.pyi`).

```{tip}
To create new package you can base on the files listed above.
```

Version in `VERSION` file is recommended to be used together with `bump_version.sh` script - see {ref}`packaging page <_packaging_semver>`. This file is read by `__version__.py`.

## Python multi project

Usually, the above structure is enough. However, project might grow and require something more complex and the template does not support this case.

For example one can imagine a project with:
- visual_processing
- text_processing


### Install one package, multiple modules

The first easiest approach is to add new python modules to `src/` package like this:

- `src/`
    - `foo` <- (main module)
    - `bar`

or
- `src/`
    - `package_name`
        - `__version__.py`
        - `VERSION`
        - (...)
    - `foo/`
    - `bar/`

One package should be then a _main_ with the same name as full package containing `__version__.py` file.

Alternative and recommended way is to move `VERSION` to project root and make `setup.cfg` to use it (and remember to modify `.bumpversion.cfg` file) - this would be a _multi module python package_.

`pip install foo`  would then result in valid code:
```python
import foo
import bar
```

### Install many packages, single module

If packages can be isolated then the best way is to move to structure:

- `components/`
    - `foo`
        - `src/`
        - `setup.cfg`
        - `setup.py`
        - (...) etc.
    - `bar`
        - `src/`
          - (...)

Then one would call
- `pip install foo bar` given packages uploaded to some PIP registry
- `pip install -e components/foo -e components/bar` for dev local install

To ensure quality one would also need to use **nox/tox** to test packages in isolation and without python registry it is a little cumbersome to use.

It is rather useful for a case when project have really independent modules but one have to use only single repository (_monorepo_ case) and/or all packages are to be used together and are tied together in their release cycle.

### Use multiple repositories

The last approach is best for really independent projects - is to basically have each package in its own repository.

This is the best clean approach, but then one have to ensure that release cycle and CI/CD is correctly setup. One can also used git submodule but this can lead to other problems but is easiest in short term especially if code is very stable.