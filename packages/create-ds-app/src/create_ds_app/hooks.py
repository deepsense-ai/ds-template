"""
Post-generation hooks for create-ds-app.

This module provides a flexible hook system that allows running custom code
after project generation. Hooks can be filtered to run only for specific
templates based on template name or group.

Example usage:
    # Create a hook that only runs for monorepo templates
    HookConfig(
        hook=my_monorepo_hook,
        name="monorepo_setup",
        template_groups=["monorepo"]
    )

    # Create a hook that runs for all templates except specific ones
    HookConfig(
        hook=my_general_hook,
        name="general_setup",
        exclude_names=["test_template"]
    )
"""

import asyncio
import os
import pathlib
import shutil
import subprocess
import tempfile
from typing import Any

import questionary
from ds_templater import HookConfig
from rich.console import Console

from create_ds_app.coding_agent import get_available_package_types


def _get_package_choices() -> list[dict[str, str]]:
    """Get package type choices for multi-select question."""
    package_types = get_available_package_types()
    choices = []
    for pkg_type, description in package_types.items():
        # Extract display name from package type (e.g., "pkg_api" -> "API")
        display_name = pkg_type.replace("pkg_", "").replace("_", " ").title()
        choices.append({"name": f"{display_name} - {description}", "value": pkg_type})
    return choices


def uv_sync_hook(project_path: pathlib.Path, context: dict[str, Any], console: Console) -> None:
    """
    Run uv sync to install dependencies.

    Args:
        project_path: Path to the created project
        context: Template context with user answers
        console: Rich console for output
    """
    console.print("\n[bold cyan]Running uv sync to install dependencies...[/bold cyan]")
    try:
        result = subprocess.run(["uv", "sync"], cwd=project_path, capture_output=True, text=True, check=True)
        console.print("[green]✓ Dependencies installed successfully![/green]")
    except subprocess.CalledProcessError as e:
        console.print("[yellow]Warning: uv sync failed with error:[/yellow]")
        console.print(f"[yellow]{e.stderr}[/yellow]")
        console.print("[yellow]You may need to run 'uv sync' manually.[/yellow]")
    except FileNotFoundError:
        console.print("[yellow]Warning: uv is not installed. Please install uv and run 'uv sync' manually.[/yellow]")


def claude_code_setup_hook(project_path: pathlib.Path, context: dict[str, Any], console: Console) -> None:
    """
    Handle Claude-code integration if requested.

    Args:
        project_path: Path to the created project
        context: Template context with user answers
        console: Rich console for output
    """
    if context.get("claude-code", "") != "Run Claude-based workflow to create the app":
        return

    console.print("\n[bold cyan]Running Claude-code generation:[/bold cyan]")

    # Get project instructions from the user
    instructions = _open_file_in_editor_and_read(
        "# Enter your project description/instructions below.\n"
        "# Lines starting with # will be ignored.\n"
        "# Describe what your project should do, what components it needs, etc.",
        console,
        starting_line=5,
    )
    if instructions is None:
        return

    # Import the coding agent module
    try:
        from create_ds_app import coding_agent
    except ImportError:
        console.print("[red]Error: Could not import coding_agent module.[/red]")
        return

    # Run the async workflow
    try:
        _run_claude_workflow(instructions, project_path, context, console)
    except Exception as e:
        console.print(f"[red]Error running Claude workflow: {e}[/red]")


def _run_claude_workflow(
    instructions: str, project_path: pathlib.Path, context: dict[str, Any], console: Console
) -> None:
    """
    Run the complete Claude Code workflow asynchronously.

    Args:
        instructions: User's project instructions
        project_path: Path to create the project at
        context: Template context with user answers
        console: Rich console for output
    """
    from loguru import logger

    from create_ds_app import coding_agent

    # Step 1: Generate follow-up questions
    console.print("\n[bold]Step 1:[/bold] Generating follow-up questions...")

    try:
        questions = asyncio.run(coding_agent.get_follow_up_questions(instructions, context))

        # Step 2: Present questionnaire to user
        console.print("\n[bold]Step 2:[/bold] Please answer the following questions about your project:")
        questionnaire_answers = _present_questionnaire(questions, console)
    except Exception as e:
        logger.exception(e)
        questionnaire_answers = {}
    # Step 3: Continue with the workflow
    asyncio.run(coding_agent.continue_workflow_with_answers(instructions, questionnaire_answers, project_path, context, console))


def _present_questionnaire(questions: list[dict], console: Console) -> dict[str, Any] | None:
    """
    Present questionnaire to the user and collect answers.

    Args:
        questions: List of question dictionaries
        console: Rich console for output

    Returns:
        Dictionary of answers or None if cancelled
    """
    answers = {}

    try:
        for question in questions:
            q_type = question.get("type", "text")
            name = question.get("name", "question")
            message = question.get("message", "Question:")
            default = question.get("default", None)

            # Build the question based on type
            if q_type == "text":
                answer = questionary.text(message, default=default or "").ask()
            elif q_type == "password":
                answer = questionary.password(message).ask()
            elif q_type == "confirm":
                answer = questionary.confirm(message, default=default if default is not None else True).ask()
            elif q_type == "select":
                choices = question.get("choices", [])
                # Convert choices to questionary format
                q_choices = []
                for choice in choices:
                    if isinstance(choice, dict):
                        q_choices.append(
                            questionary.Choice(choice.get("name", choice.get("value")), choice.get("value"))
                        )
                    else:
                        q_choices.append(choice)
                answer = questionary.select(message, choices=q_choices, default=default).ask()
            elif q_type == "checkbox":
                choices = question.get("choices", [])
                # Convert choices to questionary format
                q_choices = []
                for choice in choices:
                    if isinstance(choice, dict):
                        q_choices.append(
                            questionary.Choice(
                                choice.get("name", choice.get("value")),
                                choice.get("value"),
                                checked=choice.get("checked", False),
                            )
                        )
                    else:
                        q_choices.append(choice)
                answer = questionary.checkbox(message, choices=q_choices).ask()
            elif q_type == "autocomplete":
                choices = question.get("choices", [])
                answer = questionary.autocomplete(message, choices=choices).ask()
            else:
                # Fallback to text for unknown types
                answer = questionary.text(f"{message} (type: {q_type})", default=default or "").ask()

            if answer is None:  # User cancelled
                return None

            answers[name] = answer

        return answers

    except Exception as e:
        console.print(f"[yellow]Error presenting questionnaire: {e}[/yellow]")


def _open_file_in_editor_and_read(text: str, console: Console, starting_line: int = 0) -> str | None:
    """
    Open temporary text file to edit and read it.

    Args:
        text: Text displayed in the editor
        console: Rich console for output
        starting_line: Line number to start editing from
    Returns:
        The edited text or None if cancelled
    """
    editor = os.environ.get("EDITOR")
    if not editor:
        console.print(
            "[yellow]Warning: The $EDITOR environment variable is not set. "
            "Please set it (e.g., export EDITOR=nano) to use Claude-code integration.[/yellow]"
        )
        return None

    if not shutil.which(editor.split()[0]):
        console.print(f"[yellow]Warning: Editor '{editor}' not found in PATH.[/yellow]")
        return None

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".tmp", mode="r+", delete=False) as tf:
        temp_file_path = tf.name
        tf.write(text)
        tf.write("\n\n\n\n")
        tf.flush()

    try:
        # Open the editor and wait
        command = [*editor.split(), temp_file_path]
        if starting_line > 0 and editor.split()[0].endswith("vim"):
            command.append(f"+{starting_line}")

        subprocess.run(command, check=True)

        # After editor closes, read contents
        with open(temp_file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Filter out comments and empty lines
        instructions = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

        if not instructions:
            console.print("[yellow]No instructions provided. Skipping Claude-code generation.[/yellow]")
            return None

        return "\n".join(instructions)

    except subprocess.CalledProcessError:
        console.print("[yellow]Editor exited with non-zero status. Skipping Claude-code generation.[/yellow]")
        return None

    finally:
        os.unlink(temp_file_path)


def generate_packages_hook(project_path: pathlib.Path, context: dict[str, Any], console: Console) -> None:
    """
    Generate selected packages if user chose manual package generation.

    Args:
        project_path: Path to the created project
        context: Template context with user answers
        console: Rich console for output
    """
    if context.get("claude-code", "") == "Run Claude-based workflow to create the app":
        return

    # Ask user to select packages
    console.print("\n[bold cyan]Package Selection[/bold cyan]")
    package_choices = _get_package_choices()

    # Convert to questionary format
    q_choices = []
    for choice in package_choices:
        q_choices.append(
            questionary.Choice(
                title=choice["name"],
                value=choice["value"],
                checked=(choice["value"] == "pkg_core"),  # Core is checked by default
            )
        )

    selected_packages = questionary.checkbox("Select packages to generate:", choices=q_choices).ask()

    if not selected_packages:
        console.print("[yellow]No packages selected. Skipping package generation.[/yellow]")
        return

    console.print("\n[bold cyan]Generating selected packages...[/bold cyan]")

    from create_ds_app.package_generator import PackageGenerator

    project_name = context.get("project_name", "my-ds-project")

    try:
        # Get templates directory
        import create_ds_app

        templates_dir = pathlib.Path(create_ds_app.__file__).parent.parent.parent / "templates"

        generator = PackageGenerator(templates_dir)
        packages_dir = project_path / "packages"

        for pkg_type in selected_packages:
            # Determine package name based on convention
            if pkg_type == "pkg_core":
                # Core package uses project name with underscores
                pkg_name = project_name.replace("-", "_")
            else:
                # Other packages use project-name-suffix format
                suffix = pkg_type.replace("pkg_", "")
                pkg_name = f"{project_name}-{suffix}"

            console.print(f"  [cyan]•[/cyan] Generating {pkg_type}: {pkg_name}")

            # Generate the package
            output_dir = packages_dir / pkg_name
            generator.generate_package(
                template_name=pkg_type,
                package_name=pkg_name,
                output_dir=output_dir,
                **context,
            )

            # Register package in workspace
            generator.register_package_in_workspace(project_path, pkg_name)

        console.print("[green]✓ Packages generated successfully![/green]")

    except Exception as e:
        console.print(f"[red]Error generating packages: {e}[/red]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")


DEFAULT_HOOKS = [
    HookConfig(
        hook=generate_packages_hook,
        name="generate_packages",
        template_groups=["monorepo"],
    ),
    HookConfig(
        hook=uv_sync_hook,
        name="uv_sync",
        template_groups=["monorepo"],
    ),
    HookConfig(
        hook=claude_code_setup_hook,
        name="claude_code_setup",
        template_groups=["monorepo"],
    ),
]
