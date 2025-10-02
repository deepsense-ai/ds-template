"""
Base classes for template configuration.
"""

import inspect
import pathlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import questionary
import typer

SimpleTypes = str | bool | int | float | list["SimpleTypes"] | dict[str, "SimpleTypes"]


class WrappedOption[I: SimpleTypes | None]:
    """Wrapped typer.Option with a default value"""

    def __init__(self, option: typer.Option, default: I = None):
        self._option = option
        self._default = default

    @property
    def option(self) -> typer.Option:
        """Get the underlying typer.Option"""
        return self._option

    @property
    def default(self) -> I:
        """Get the default value"""
        return self._default

    @property
    def param_type(self) -> type[I]:
        """Get the type of the default value"""
        if self._default is not None:
            return type(self._default)
        return str  # Default fallback type


class Question[T: SimpleTypes](ABC):
    """Base class for template questions"""

    @property
    @abstractmethod
    def question_type(self) -> str:
        """Type of the question"""
        pass

    def __init__(self, name: str, message: str, default: T | None = None):
        self.name = name
        self.message = message
        self.default = default

    def to_dict(self) -> dict[str, SimpleTypes]:
        """Convert question properties to a dictionary representation."""
        return {"name": self.name, "message": self.message, "default": self.default, "type": self.question_type}

    def prompt(self) -> T:
        """Base method to prompt for and return an answer"""
        raise NotImplementedError("Subclasses must implement prompt()")

    def to_typer_option(self) -> WrappedOption[T]:
        """Convert question to a typer Option with appropriate type annotation."""
        # Default implementation for base Question
        return WrappedOption(typer.Option(self.default, help=self.message), self.default)


class TextQuestion(Question[str]):
    """Text input question"""

    question_type: str = "text"

    def prompt(self) -> str:
        """Display a text input prompt and return the user's text response."""
        return questionary.text(self.message, default=self.default or "").ask()

    def to_typer_option(self) -> WrappedOption[str]:
        """Convert TextQuestion to a typer Option."""
        return WrappedOption(typer.Option(self.default, help=self.message), self.default)


class ListQuestion(Question[str]):
    """List selection question"""

    question_type: str = "list"

    def __init__(self, name: str, message: str, choices: list[str], default: str | None = None):
        super().__init__(name, message, default)
        self.choices = choices

    def to_dict(self) -> dict[str, SimpleTypes]:
        """Convert question properties to a dictionary including choices."""
        result = super().to_dict()
        result["choices"] = self.choices
        return result

    def prompt(self) -> str:
        """Display a list selection prompt and return the user's selection."""
        return questionary.select(self.message, choices=self.choices, default=self.default).ask()

    def to_typer_option(self) -> WrappedOption[str]:
        """Convert ListQuestion to a typer Option."""
        help_text = f"{self.message}. Choices: {', '.join(self.choices)}"
        return WrappedOption(typer.Option(self.default, help=help_text), self.default)


class MultiSelectQuestion(Question[list[str]]):
    """Multi-select checkbox question"""

    question_type: str = "checkbox"

    def __init__(
        self,
        name: str,
        message: str,
        choices: list[str | dict[str, str]],
        default: list[str] | None = None,
    ):
        super().__init__(name, message, default)
        self.choices = choices
        self._choice_map = self._build_choice_map()

    def _build_choice_map(self) -> dict[str, str]:
        """Build a mapping from display names to values."""
        choice_map = {}
        for choice in self.choices:
            if isinstance(choice, dict):
                display_name = choice["display_name"]
                value = choice["value"]
                choice_map[display_name] = value
            else:
                # If it's just a string, use it as both display name and value
                choice_map[choice] = choice
        return choice_map

    def _get_display_choices(self) -> list[str]:
        """Get the list of display names for the choices."""
        display_choices = []
        for choice in self.choices:
            if isinstance(choice, dict):
                display_choices.append(choice["display_name"])
            else:
                display_choices.append(choice)
        return display_choices

    def _get_default_display_names(self) -> list[str]:
        """Convert default values to display names."""
        if not self.default or not isinstance(self.default, list):
            return []

        # Reverse mapping: value -> display_name
        value_to_display = {v: k for k, v in self._choice_map.items()}
        return [value_to_display.get(value, value) for value in self.default]

    def to_dict(self) -> dict[str, SimpleTypes]:
        """Convert question properties to a dictionary including choices."""
        result = super().to_dict()
        result["choices"] = self._get_display_choices()
        return result

    def prompt(self) -> list[str]:
        """Display a multi-select checkbox prompt and return the user's selections as values."""
        # Create questionary Choice objects that map display names to values
        qchoices = []
        for choice in self.choices:
            if isinstance(choice, dict):
                qchoices.append(
                    questionary.Choice(
                        title=choice["display_name"],
                        value=choice["value"],
                        checked=choice["value"] in (self.default or [])
                    )
                )
            else:
                qchoices.append(
                    questionary.Choice(
                        title=choice,
                        value=choice,
                        checked=choice in (self.default or [])
                    )
                )

        return questionary.checkbox(self.message, choices=qchoices).ask()

    def to_typer_option(self) -> WrappedOption[list[str]]:
        """Convert MultiSelectQuestion to a typer Option."""
        choices_text = ", ".join(self._get_display_choices())
        help_text = f"{self.message}. Choices: {choices_text}"
        return WrappedOption(typer.Option(self.default, help=help_text), self.default)


class ConfirmQuestion(Question[bool]):
    """Yes/No confirmation question"""

    question_type: str = "confirm"

    def prompt(self) -> bool:
        """Confirm question prompt"""
        return questionary.confirm(self.message, default=self.default if self.default is not None else False).ask()

    def to_typer_option(self) -> WrappedOption[bool]:
        """Convert ConfirmQuestion to a typer Option."""
        return WrappedOption(typer.Option(self.default, help=self.message), self.default)


class TemplateConfig:
    """Base class for template configuration"""

    name: str = ...
    description: str = ...
    template_group: str = ...
    location: str = ...
    slug: str = ...
    welcome_message: str | None = None

    questions: list[Question] = []

    def __init_subclass__(cls) -> None:
        # Allow location to be set explicitly, otherwise derive from file path
        if not hasattr(cls, "location") or cls.location is ...:
            file_path = pathlib.Path(inspect.getfile(cls))
            if file_path.parent.name != "ds_templater":
                cls.location = file_path.parent.name

        # Generate slug from location if not set
        if not hasattr(cls, "slug") or cls.slug is ...:
            cls.slug = cls.location.replace("_", "-")

        # Validate required fields
        if cls.slug is ...:
            raise ValueError(f"slug is not set for {cls.__name__}")
        if cls.location is ...:
            raise ValueError(f"location is not set for {cls.__name__}")
        if cls.template_group is ...:
            raise ValueError(f"template_group is not set for {cls.__name__}")
        if cls.name is ...:
            raise ValueError(f"name is not set for {cls.__name__}")
        if cls.description is ...:
            raise ValueError(f"description is not set for {cls.__name__}")
        if cls.questions is ...:
            raise ValueError(f"questions is not set for {cls.__name__}")

    @property
    def questions_map(self) -> dict[str, Question]:
        """Get questions as a dictionary of name to Question"""
        return {q.name: q for q in self.questions}

    def build_context(self, context: dict[str, SimpleTypes]) -> dict[str, SimpleTypes]:
        """
        Build additional context based on the answers.
        Override this method in template configs to add custom context.

        Args:
            context: Dictionary containing the current context including answers
                    from questions

        Returns:
            Dictionary containing additional context variables
        """
        return {}

    def should_include_file(self, file_path: pathlib.Path, context: dict[str, SimpleTypes]) -> bool:
        """
        Determine whether a file should be included in the generated project.
        Override this method in template configs to add custom file filtering logic.

        Args:
            file_path: Path object representing the file relative to the template root
            context: Dictionary containing the current context including answers
                    from questions and additional context

        Returns:
            Boolean indicating whether the file should be included
        """
        return True

    def get_conditional_directories(self) -> dict[str, tuple[str, Any]]:
        """
        Define directories that should be conditionally included based on context variables.

        Returns:
            Dictionary mapping directory paths to context variable names that control inclusion.
            For example: {"observability": ("variable", 23)} means the observability/ directory
            will only be included if context["variable"] is equal 23.
        """
        return {}

    def get_project_directory_name(self, context: dict[str, SimpleTypes]) -> str:
        """
        Get the project directory name based on the context.
        Override this method in template configs to add custom project directory naming logic.
        """
        name = context.get("project_name", self.name + "-" + datetime.now().strftime("%Y%m%d%H%M%S"))
        return name.replace(" ", "-").lower()

    def get_config_schema(self) -> dict[str, SimpleTypes]:
        """Show JSON schema for this template configuration."""
        return {
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "template_group": self.template_group,
            "questions": self.questions_map,
            "welcome_message": self.welcome_message,
        }
