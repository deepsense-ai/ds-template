# Code documentation

```{hint}

  To add your code use sphinx tool in project root directory:

    $ sphinx-apidoc -o docs/api/ src/{{ cookiecutter.python_package_name }}

  and add reference from any page which is reachable from the index page.
```

```python
    import {{ cookiecutter.__package_name }}
```

```{toctree}
---
maxdepth: 4
---
api/modules
```