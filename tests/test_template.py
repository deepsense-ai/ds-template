import os
import re
import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Sequence


class JinjaSolvedValidator:
    """Tests if all jinja templates are matched."""
    def __init__(self):
        self.brackets_matcher = re.compile("(?:\{\{|\{\%).*cookiecutter.*(?:\}\}|\%\})")

    def has_unresolved(self, content: str) -> bool:
        return self.brackets_matcher.search(content) is not None


def test_regex():
    val = JinjaSolvedValidator()
    assert val.has_unresolved('asd {{cookiecutter.foo }}{{ cookie.foo }} {{ % {{ }} }}are a') == True
    assert val.has_unresolved('{{ % {{ }} }}') == False
    assert val.has_unresolved('''maa aal
                              asd dd {%- cookiecutter.zlo -%}
                              ''') == True
    assert val.has_unresolved('}} {{') == False

@contextmanager
def change_dir(dir : Path):
    assert dir.is_dir()
    assert dir.exists()
    cwd = Path.cwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(cwd)


def run_command(command: str, dir: Path):
    with change_dir(dir):
        try:
            return subprocess.check_call(shlex.split(command))
        except subprocess.CalledProcessError as ex:
            print(ex)
            return ex.returncode


def assert_jinja_resolved(files: Sequence[Path]) -> None:
    """Asserts to make sure no curly braces appear in a file name nor in it's content.
    """
    text_files = ['.txt', '.py', '.rst', '.md', '.cfg', '.toml', '.json', '.yaml', '.yml', '.ini', '.sh', '.ipynb']
    validator = JinjaSolvedValidator()
    for file in files:
        assert validator.has_unresolved(file.name) == False
        if file.is_file() and file.suffix in text_files:
            content = file.read_text(encoding="utf-8")
            assert validator.has_unresolved(content) == False


def test_template_project(cookies):
    result = cookies.bake(extra_context={
        "client_name": "ds.ai",
        "project_name": "hello",
        "ci": "GitLab"
        })

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "ds-ai-hello"
    assert result.project_path.is_dir()

    rpath: Path = result.project_path
    assert_jinja_resolved(rpath.rglob("*"))


def test_template_creates_package(cookies):
    result = cookies.bake(extra_context={
        "client_name": "test",
        "project_name": "test",
        "ci": "None"
    })
    assert result.exit_code == 0
    assert result.exception is None

    rpath: Path = result.project_path
    assert run_command("uv build", rpath) == 0, "uv build failed!"

    dist_path = rpath / "dist"
    assert dist_path.is_dir() is True, "The dist directory was not created"

    dist_files = ["test-0.0.1.dev0.tar.gz", "test-0.0.1.dev0-py3-none-any.whl"]
    assert all((dist_path / file).exists() for file in dist_files), "Some distribution files were not found"


def test_template_project_no_cicd(cookies):
    result = cookies.bake(extra_context={
        "client_name": "no",
        "project_name": "cicd",
        "ci": "None"
    })
    assert result.exit_code == 0
    assert result.exception is None

    rpath: Path = result.project_path
    assert (rpath / ".gitlab-ci.yml").exists() is False
    assert (rpath / ".github").exists() is False


def test_template_project_with_gitlab(cookies):
    result = cookies.bake(extra_context={
        "client_name": "with",
        "project_name": "gitlab",
        "ci": "GitLab"
    })
    assert result.exit_code == 0
    assert result.exception is None

    rpath: Path = result.project_path
    assert (rpath / ".gitlab-ci.yml").exists() is True
    assert (rpath / ".github").exists() is False


def test_template_project_with_github(cookies):
    result = cookies.bake(extra_context={
        "client_name": "with",
        "project_name": "github",
        "ci": "Github"
    })
    assert result.exit_code == 0
    assert result.exception is None

    rpath: Path = result.project_path
    assert (rpath / ".gitlab-ci.yml").exists() is False
    assert (rpath / ".github").exists() is True


def test_template_project_with_jupytext(cookies):
    result = cookies.bake(extra_context={
        "client_name": "no",
        "project_name": "jupytext",
        "jupytext": "Yes"
        })
    assert result.exit_code == 0
    assert result.exception is None

    rpath: Path = result.project_path
    jupytext_pos = (rpath / ".pre-commit-config.yaml").read_text(encoding="utf-8").find("jupytext")
    assert jupytext_pos != -1
    assert len(list((rpath / "notebooks").glob("*.py"))) > 0, "Notebook should have py:percent file"


def test_template_project_no_jupytext(cookies):
    result = cookies.bake(extra_context={
        "client_name": "no",
        "project_name": "jupytext",
        "jupytext": "No"
        })
    assert result.exit_code == 0
    assert result.exception is None

    rpath: Path = result.project_path
    jupytext_pos = (rpath / ".pre-commit-config.yaml").read_text(encoding="utf-8").find("jupytext")
    assert jupytext_pos == -1
    assert len(list((rpath / "notebooks").glob("*.py"))) == 0, "Notebook should not have a py:percent file"
