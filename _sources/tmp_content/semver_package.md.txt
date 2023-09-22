(_packaging_semver)=
# Packaging & semantic version

```{note}
GitLab CI by default provides manual deploy to private GitLab Package Registry - _development_ version, as well as _release_.
```

It is a good practice to have semantic versions, especially when one wants to distribute software.

This is not required for many research projects, but it is essential and very useful when one wants to share his work.

We strongly recommend to learn more about semantic version and read [semver dedicated page](https://semver.org/).

By default `(major.minor.patch)` numbering scheme is provided by a bash script wrapper on `bump2version` tool:

```bash
./bump_version.sh [major|minor|patch]
```

The script makes a new commit with a message and modifies `src/<name>/VERSION` file.
Detailed configuration is in `.bumpconfig.cfg` file.

`VERSION` file is introduced as it allows to inspect/modify version reliable with simple UNIX tools, without need to parse python code. It simplifies greatly automated builds or introspection capabilities.

```{tip}
`bump2version` tool is chosen, because it helps you to follow semantic versioning scheme but also can modify different files as it is _language agnostic_ and can work with non-python code as well and centralizes version string control in one place. 

Check [documentation](https://pypi.org/project/bump2version/) for more details.
```

By default, all version will have `dev` suffix (and `dev<build_number>` on CI is recommended) - this informs that package is made during _development_.

During release the "dev<number>" should be dropped to signal it is no more development preview but that it is suitable to be used by other people.


```{note}
`.bumpconfig.cfg` configuration could be moved to `pyproject.toml` but it modifies the file during use and it resulted in conflicts with linters, which is why it is done the way it is now.
```

Example usage:

```bash
# assume current_version = 0.1.3 and we want to increase the middle number (minor)
$ ./bump_version.sh minor
# current_version = 0.2.0 and it executes
# git commit -m “Bump version 0.1.3 - 0.2.0”
```

```{warning}
`./bump_version.sh release` - should be called only on CI job to ensure proper release cycle.

You also need to be aware of valid version format, you can read about regex rules on [GitLab rules](https://docs.gitlab.com/ee/user/packages/pypi_repository/#ensure-your-version-string-is-valid).
```