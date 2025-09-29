import json
from pathlib import Path
import stat
import shutil

print("Running post generation...")

files_to_be_removed = []

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
    ".github/workflows/documentation.yml"
]

BUMPVERSION_FILES = [
    ".bumpversion.cfg",
    "bump_version.sh"
]

{% if cookiecutter.ci != "GitLab" %}
files_to_be_removed.extend(GITLAB_FILES)
{% endif %}

{% if cookiecutter.ci != "Github" %}
files_to_be_removed.extend(GITHUB_FILES)
{% endif %}

{% if cookiecutter.jupytext != "Yes" %}
files_to_be_removed.append("notebooks/example.py")
{% endif %}

{% if cookiecutter.docs == "No docs" %}
files_to_be_removed.extend(DOCS_FILES)
{% endif %}

{% if cookiecutter.versioning != "Bumpversion" %}
files_to_be_removed.extend(BUMPVERSION_FILES)
{% endif %}

{% if cookiecutter.client_name != "ds" %}
with open("branding/branding.json", "r") as f:
    branding = json.load(f)
    branding["name"] = '{{ cookiecutter.client_name }}'
    with open("branding/branding.json", "w") as f:
        json.dump(branding, f, indent=4)
{% endif %}

print("Cleaning files... 🌀")
for path in files_to_be_removed:
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
