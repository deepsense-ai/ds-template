"""
Template rendering and project creation.
"""

import os
import pathlib
import shutil
from typing import Any

import jinja2
import yaml
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree

from .config import SimpleTypes, TemplateConfig

console = Console()


class TemplateRenderer:
    """Handles template rendering and project creation."""

    def __init__(self):
        """Initialize the template renderer."""
        self.console = console

    def prompt_template_questions(
        self, template_config: TemplateConfig, cli_args: dict | None = None
    ) -> dict[str, SimpleTypes]:
        """
        Prompt user for template-specific questions, skipping those provided via CLI.

        Args:
            template_config: The template configuration.
            cli_args: Arguments provided via CLI.

        Returns:
            Dictionary of answers to the template questions.
        """
        import sys

        if cli_args is None:
            cli_args = {}

        answers = {}
        logger.debug(f"CLI args: {cli_args}")
        for question in template_config.questions:
            logger.debug(f"Prompting user for question: {question.name}")
            if question.name in cli_args:
                # Use CLI-provided value
                answers[question.name] = cli_args[question.name]
                print(f"Using CLI value for {question.name}: {cli_args[question.name]}")
            else:
                # Prompt user for value
                answer = question.prompt()
                # Check if user cancelled with Ctrl-C
                if answer is None:
                    # Exit immediately without further messages
                    sys.exit(1)
                answers[question.name] = answer

        return answers

    def create_project(
        self,
        template_config: TemplateConfig,
        template_path: pathlib.Path,
        project_path: str,
        context: dict[str, SimpleTypes],
    ) -> None:
        """
        Create a new project from the selected template.

        Args:
            template_config: The template configuration.
            template_path: Path to the template directory.
            project_path: Path where the project will be created.
            context: Context for rendering the templates.
        """
        # Create project directory if it doesn't exist
        os.makedirs(project_path, exist_ok=True)

        conditional_directories = template_config.get_conditional_directories()

        def should_include_path(path: pathlib.Path, base_path: pathlib.Path) -> bool:
            """Check if a path should be included based on conditional directories and file inclusion logic."""
            rel_path = path.relative_to(base_path)

            # Check conditional directories
            for dir_name, (context_var, expected_value) in conditional_directories.items():
                if (str(rel_path).startswith(dir_name) or str(rel_path) == dir_name) and context.get(
                    context_var
                ) != expected_value:
                    return False

            # Check template config's custom file inclusion logic
            return template_config.should_include_file(rel_path, context)

        def process_template_file(item: pathlib.Path, target_path: pathlib.Path) -> None:
            """Process a single template file."""
            if item.suffix == ".j2":
                with open(item) as f:
                    template_content = f.read()

                # Render template with context
                template = jinja2.Template(template_content)
                rendered_content = template.render(**context)

                # Remove .j2 extension for target
                target_path = target_path.with_suffix("")

                # Special handling for docker-compose files
                if (
                    target_path.name in ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"]
                    and target_path.exists()
                ):
                    # Read existing content and merge
                    with open(target_path) as f:
                        existing_content = f.read()
                    rendered_content = self._merge_docker_compose_files(existing_content, rendered_content)
                    self.console.print(
                        f"[cyan]Merged docker-compose files at {target_path.relative_to(project_path)}[/cyan]"
                    )

                # Write the (possibly merged) content
                with open(target_path, "w") as f:
                    f.write(rendered_content)
            else:
                # Create parent directories if they don't exist
                os.makedirs(target_path.parent, exist_ok=True)
                # Simple file copy
                shutil.copy2(item, target_path)

        def process_template_files(source_path: pathlib.Path) -> None:
            """Process files from a template directory."""
            for item in source_path.glob("**/*"):
                if item.name == "template_config.py":
                    continue  # Skip template config file

                # Check if this path should be included
                if not should_include_path(item, source_path):
                    continue

                # Get relative path from template root
                rel_path = str(item.relative_to(source_path))

                # Process path parts for Jinja templating (for directory names)
                path_parts = []
                for part in pathlib.Path(rel_path).parts:
                    if "{{" in part and "}}" in part:
                        # Render the directory name as a template
                        name_template = jinja2.Template(part)
                        rendered_part = name_template.render(**context)
                        path_parts.append(rendered_part)
                    else:
                        path_parts.append(part)

                # Construct the target path with processed directory names
                target_rel_path = os.path.join(*path_parts) if path_parts else ""
                target_path = pathlib.Path(project_path) / target_rel_path

                if item.is_dir():
                    os.makedirs(target_path, exist_ok=True)
                elif item.is_file():
                    process_template_file(item, target_path)

        # Process files with progress indicator
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=self.console
        ) as progress:
            progress.add_task("[cyan]Creating project structure...", total=None)
            process_template_files(template_path)

        # Display welcome message if configured
        if template_config.welcome_message:
            self.console.print(f"\n[bold cyan]{template_config.welcome_message}[/bold cyan]")

        # Display project structure
        self.console.print("\n[bold green]✓ Project created successfully![/bold green]")
        self.console.print(f"[bold]Project location:[/bold] {project_path}\n")

        # Create and display project tree
        self._display_project_tree(project_path)

    def _merge_docker_compose_files(self, existing_content: str, new_content: str) -> str:
        """Merge two docker-compose YAML files intelligently."""
        try:
            existing_data = yaml.safe_load(existing_content)
            new_data = yaml.safe_load(new_content)

            # Deep merge the YAML data
            merged_data = self._deep_merge_dicts(existing_data, new_data)

            # Convert back to YAML with proper formatting and document separator
            yaml_content = yaml.dump(merged_data, default_flow_style=False, sort_keys=False)
            # Add the document separator at the beginning
            return f"---\n{yaml_content}"
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not merge docker-compose files: {e}[/yellow]")
            # If merging fails, return the new content (override)
            return new_content

    def _deep_merge_dicts(self, dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """Deep merge two dictionaries, with dict2 values taking precedence."""
        result = dict1.copy()

        for key, value in dict2.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    # Recursively merge nested dictionaries
                    result[key] = self._deep_merge_dicts(result[key], value)
                elif isinstance(result[key], list) and isinstance(value, list):
                    # For lists, we'll concatenate and remove duplicates (if they're simple values)
                    if all(isinstance(item, (str, int, float)) for item in result[key] + value):
                        # Simple list - remove duplicates while preserving order
                        seen = set()
                        merged_list = []
                        for item in result[key] + value:
                            if item not in seen:
                                seen.add(item)
                                merged_list.append(item)
                        result[key] = merged_list
                    else:
                        # Complex list - just concatenate
                        result[key] = result[key] + value
                else:
                    # For other types, dict2 value takes precedence
                    result[key] = value
            else:
                result[key] = value

        return result

    def _display_project_tree(self, project_path: str) -> None:
        """Display the project structure as a tree."""
        tree = Tree("[bold blue]Project Structure[/bold blue]")
        project_root = pathlib.Path(project_path)

        def build_tree(node: Tree, path: pathlib.Path, level: int = 0) -> None:
            # Limit depth to avoid too much output
            if level > 3:
                return

            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for item in items:
                if item.is_dir():
                    # Skip common directories that are too verbose
                    if item.name in [".git", "__pycache__", "node_modules", ".venv"]:
                        continue
                    branch = node.add(f"[bold cyan]{item.name}/[/bold cyan]")
                    build_tree(branch, item, level + 1)
                else:
                    node.add(f"[green]{item.name}[/green]")

        build_tree(tree, project_root)
        self.console.print(tree)
