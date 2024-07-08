from pathlib import Path
import stat
import shutil

print("Running post generation...")

ci = "{{ cookiecutter.ci }}"

REMOVE_PATHS = []

gitlab_files = [
    ".gitlab-ci.yml",
    "docker/precommit"
]

github_files = [
    ".github/",
]

docs_files = [
    "docs/",
    "build_docs.sh",
    ".github/workflows/documentation.yaml"
]

{% if cookiecutter.ci != "GitLab" %}
REMOVE_PATHS.extend(gitlab_files)
{% endif %}

{% if cookiecutter.ci != "Github" %}
REMOVE_PATHS.extend(github_files)
{% endif %}

{% if cookiecutter.jupytext != "Yes" %}
REMOVE_PATHS.extend(["notebooks/example.py"])
{% endif %}

{% if cookiecutter.docs == "No docs" %}
REMOVE_PATHS.extend(docs_files)
{% endif %}

print("Cleaning files... 🌀")
for path in REMOVE_PATHS:
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
