from pathlib import Path
import stat
import shutil

print("Running post generation...")

remove_paths = []

GITLAB_FILES = [
    ".gitlab-ci.yml",
    "docker/precommit"
]

GITHUB_FILES = [
    ".github/",
]

DOCS_FILES = [
    "docs/",
    "build_docs.sh",
    ".github/workflows/documentation.yaml"
]

{% if cookiecutter.ci != "GitLab" %}
remove_paths.extend(GITLAB_FILES)
{% endif %}

{% if cookiecutter.ci != "Github" %}
remove_paths.extend(GITHUB_FILES)
{% endif %}

{% if cookiecutter.jupytext != "Yes" %}
remove_paths.extend(["notebooks/example.py"])
{% endif %}

{% if cookiecutter.docs == "No docs" %}
remove_paths.extend(DOCS_FILES)
{% endif %}

print("Cleaning files... 🌀")
for path in remove_paths:
    path = Path(path)
    if path.exists() and path.is_file():
        print(f"Clean up file: '{path}'")
        path.unlink()
    elif path.exists() and path.is_dir():
        print(f"Clean up directory: '{path}'")
        shutil.rmtree(path)

# Solves problems when template fails to keep linux permissions. (e.g. after zipping template)
print("Updating permissions... 🚀")
for path in Path("").rglob("*.sh"):
    path.chmod(path.stat().st_mode | stat.S_IXUSR)

print("DONE 🎆")
