import pathlib
from typing import Any

from create_ds_app.questions import CommonQuestions
from ds_templater import ListQuestion, TemplateConfig


class StandardTemplateConfig(TemplateConfig):
    """Standard AI Project template configuration"""

    name: str = "Standard AI Project"
    description: str = "A modern AI project template with workspace structure"
    template_group: str = "monorepo"

    questions: list = [
        CommonQuestions.project_name,
        CommonQuestions.python_version,
        ListQuestion(name="ci", message="Select CI provider", choices=["GitHub", "GitLab", "None"], default="GitHub"),
        ListQuestion(
            name="claude-code",
            message="How would you like to initialize your project?",
            choices=[
                "Just generate packages (core by default, more to choose)",
                "Run Claude-based workflow to create the app",
            ],
            default="Just generate packages (core by default, more to choose)",
        ),
    ]

    def get_project_directory_name(self, context: dict[str, Any]) -> str:
        """Get the project directory name based on the context."""
        return context["project_name"]

    def should_include_file(self, file_path: pathlib.Path, context: dict[str, Any]) -> bool:
        """
        Determine whether a file should be included in the generated project.
        Override this method in template configs to add custom file filtering logic.
        """
        # Handle CI/CD file inclusion based on user choice
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
