"""Common questions used across templates."""

from ds_templater import ListQuestion, TextQuestion


class CommonQuestions:
    """Container for common questions used across templates."""

    project_name = TextQuestion(name="project_name", message="Project name", default="my-ds-project")

    python_version = ListQuestion(
        name="python_version",
        message="Select Python version",
        choices=["3.13", "3.12", "3.11", "3.10"],
        default="3.13",
    )
