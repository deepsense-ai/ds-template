from typing import Any

from ds_templater import ConfirmQuestion, ListQuestion, TemplateConfig

# Import CommonQuestions using a try-except for flexibility
try:
    from create_ds_app.questions import CommonQuestions
except ImportError:
    # Fallback if running standalone
    from ds_templater import ListQuestion as ListQ
    from ds_templater import TextQuestion

    class CommonQuestions:
        project_name = TextQuestion(name="project_name", message="Project name", default="my-ds-project")
        python_version = ListQ(
            name="python_version",
            message="Select Python version",
            choices=["3.13", "3.12", "3.11", "3.10"],
            default="3.13",
        )


class StandardTemplateConfig(TemplateConfig):
    """Standard AI Project template configuration"""

    name: str = "Standard AI Project"
    description: str = "A modern AI project template with workspace structure"
    template_group: str = "monorepo"

    questions: list = [
        CommonQuestions.project_name,
        CommonQuestions.python_version,
        ListQuestion(name="ci", message="Select CI provider", choices=["GitHub", "GitLab", "None"], default="GitHub"),
    ]

    def get_project_directory_name(self, context: dict[str, Any]) -> str:
        """Get the project directory name based on the context."""
        return context["project_name"].replace("-", "_")


# Create instance of the config to be imported
config = StandardTemplateConfig()
