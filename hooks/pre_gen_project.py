import re
import sys

logo = """
██████  ███████ ███████ ██████  ███████ ███████ ███    ██ ███████ ███████     █████  ██ 
██   ██ ██      ██      ██   ██ ██      ██      ████   ██ ██      ██         ██   ██ ██ 
██   ██ █████   █████   ██████  ███████ █████   ██ ██  ██ ███████ █████      ███████ ██ 
██   ██ ██      ██      ██           ██ ██      ██  ██ ██      ██ ██         ██   ██ ██ 
██████  ███████ ███████ ██      ███████ ███████ ██   ████ ███████ ███████ ██ ██   ██ ██ 
"""
print(logo)
print("Validation of template values...")

package_name = '{{ cookiecutter.python_package_name }}'
valid_python_name = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
if not re.match(valid_python_name, package_name):
    print(f"ERROR: '{package_name}' is not a valid Python module name.")
    sys.exit(1)

# TODO temporary, until GitLab CI support for Semantic Release will be added
ci_type = '{{ cookiecutter.ci }}'
versioning_approach = '{{ cookiecutter.versioning }}'
if ci_type == 'GitLab' and versioning_approach == "Python Semantic Release":
    print(f"ERROR: 'Python Semantic Release' is currently not supported for projects with GitLab CI.")
    sys.exit(1)

print("Template looks ok.")