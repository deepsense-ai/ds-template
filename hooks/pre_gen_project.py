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

print("Template looks ok.")