from pathlib import Path
import stat
print("Running post generation...")

ci = "{{ cookiecutter.ci }}"

REMOVE_PATHS = []

gitlab_files = [
    ".gitlab-ci.yml"
]

{% if cookiecutter.ci != "GitLab" %}
REMOVE_PATHS.extend(gitlab_files)
{% endif %}

{% if cookiecutter.jupytext != "Yes" %}
REMOVE_PATHS.extend(["notebooks/example.py"])
{% endif %}

print("Cleaning files... 🌀")
for path in REMOVE_PATHS:
    path = Path(path)
    if path.exists() and path.is_file():
        print(f"Clean up file: '{path}'")
        path.unlink()

#Solves problems when template fails to keep linux permissions. (e.g. after zipping template)
print("Updating permissions... 🚀")
for path in Path("").rglob("*.sh"):
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    
print("DONE 🎆")