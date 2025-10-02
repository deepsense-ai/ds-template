import pathlib
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

    def should_include_file(self, file_path: pathlib.Path, context: dict[str, Any]) -> bool:
        """
        Determine whether a file should be included in the generated project.
        Override this method in template configs to add custom file filtering logic.
        """
        # Handle CI/CD file inclusion based on user choice
        print(file_path, context)
        ci_provider = context["ci"]

        # Include GitHub Actions files only if GitHub is selected
        if str(file_path).startswith(".github/") and ci_provider != "GitHub":
            return False
            
        # Include GitLab CI file only if GitLab is selected
        if str(file_path).startswith(".gitlab-ci.yml") and ci_provider != "GitLab":
            return False
            
        # Include license files only if CI is not "None"
        if str(file_path) in [".license-whitelist.txt", ".libraries-whitelist.txt"] and ci_provider == "None":
            return False
            
        return True

    def get_conditional_directories(self):
        return {".github": ("ci", "GitHub")}

# Create instance of the config to be imported
config = StandardTemplateConfig()
