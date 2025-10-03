"""
CLI utilities and command handlers for template operations.
"""

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any

import questionary
import typer
import yaml
from rich.console import Console
from rich.panel import Panel

from .config import TemplateConfig
from .registry import TemplateRegistry
from .renderer import TemplateRenderer

console = Console()


class ParameterHandler:
    """Handles parameter parsing and loading from various sources."""

    @staticmethod
    def parse_key_value_params(params: list[str]) -> dict[str, Any]:
        """Parse key=value parameters from command line."""
        result = {}
        for param in params:
            if "=" not in param:
                console.print(f"[red]Invalid parameter format: '{param}'. Expected 'key=value'[/red]")
                continue
            key, value = param.split("=", 1)
            # Try to parse value as JSON for complex types
            try:
                # Try to parse as JSON (for bool, int, list, etc.)
                parsed_value = json.loads(value.lower() if value.lower() in ["true", "false"] else value)
                result[key] = parsed_value
            except (json.JSONDecodeError, ValueError):
                # If it fails, treat as string
                result[key] = value
        return result

    @staticmethod
    def load_params_from_yaml(yaml_file: str) -> dict[str, Any]:
        """Load parameters from a YAML file."""
        yaml_path = pathlib.Path(yaml_file)
        if not yaml_path.exists():
            console.print(f"[red]YAML file '{yaml_file}' not found![/red]")
            sys.exit(1)

        with open(yaml_path) as f:
            try:
                params = yaml.safe_load(f)
                if not isinstance(params, dict):
                    console.print("[red]YAML file must contain a dictionary of parameters![/red]")
                    sys.exit(1)
                return params
            except yaml.YAMLError as e:
                console.print(f"[red]Error parsing YAML file: {e}[/red]")
                sys.exit(1)

    @staticmethod
    def get_template_defaults(template_config: TemplateConfig) -> dict:
        """Get template default values as a dictionary."""
        defaults = {}
        for question in template_config.questions:
            if question.default is not None:
                defaults[question.name] = question.default
        return defaults

    @staticmethod
    def dump_defaults_to_yaml(template_config: TemplateConfig) -> str:
        """Return template defaults as YAML string."""
        defaults = ParameterHandler.get_template_defaults(template_config)
        return yaml.dump(defaults, default_flow_style=False, sort_keys=False)

    @staticmethod
    def interactive_editor_mode(template_config: TemplateConfig, initial_params: dict | None = None) -> dict[str, Any]:
        """Open defaults in editor and parse the result."""
        # Get defaults and merge with initial params
        defaults = ParameterHandler.get_template_defaults(template_config)
        if initial_params:
            defaults.update(initial_params)

        # Create temp file with defaults
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(defaults, f, default_flow_style=False, sort_keys=False)
            temp_file = f.name

        # Get editor from environment or use default
        editor = os.environ.get("EDITOR", "vi")

        console.print(f"[cyan]Opening {temp_file} in {editor}...[/cyan]")
        console.print("[yellow]Edit the parameters and save to continue.[/yellow]")

        # Open editor
        subprocess.run([editor, temp_file], check=True)

        # Load edited parameters
        params = ParameterHandler.load_params_from_yaml(temp_file)

        # Clean up temp file
        os.unlink(temp_file)

        return params


class TemplateSelector:
    """Handles template selection logic."""

    @staticmethod
    def select_template_interactively(
        registry: TemplateRegistry, template_name: str | None = None, group: str | None = None
    ) -> TemplateConfig | None:
        """
        Select a template either by name or interactively.

        Args:
            registry: The template registry
            template_name: Optional template name to select directly
            group: Optional group to filter templates

        Returns:
            Selected template config or None
        """
        # Get templates (filtered by group if provided)
        templates = registry.get_templates(group=group) if group else registry.get_templates()

        if not templates:
            console.print(f"[red]No templates found{f' in group {group}' if group else ''}![/red]")
            return None

        # If template name provided, try to get it directly
        if template_name:
            template_config = registry.get_template(template_name)
            if not template_config:
                console.print(f"[red]Template '{template_name}' not found![/red]")
                console.print("[yellow]Available templates:[/yellow]")
                for tmpl in templates:
                    console.print(f"  • {tmpl.location}")
                return None
            return template_config

        # If only one template available, select it automatically
        if len(templates) == 1:
            return templates[0]

        # Interactive selection
        template_choices = [
            questionary.Choice(
                title=f"{tmpl.name} ({tmpl.template_group}) - {tmpl.description}",
                value=tmpl.location,
            )
            for tmpl in templates
        ]

        template_location = questionary.select(
            "Select a template:",
            choices=template_choices,
        ).ask()

        if not template_location:
            return None

        return registry.get_template(template_location)


class CLICommands:
    """Generic CLI commands for template operations."""

    def __init__(self, templates_dir: pathlib.Path, post_creation_hooks: list | None = None):
        """
        Initialize CLI commands with templates directory.

        Args:
            templates_dir: Path to the templates directory
            post_creation_hooks: Optional list of hook configurations to run after project creation
        """
        self.templates_dir = templates_dir
        self.registry = self._setup_registry()
        self.renderer = TemplateRenderer()
        self.param_handler = ParameterHandler()
        self.selector = TemplateSelector()
        self.post_creation_hooks = post_creation_hooks or []

    def _setup_registry(self) -> TemplateRegistry:
        """Set up the template registry with available templates."""
        registry = TemplateRegistry(templates_dir=self.templates_dir)
        registry.discover_templates()

        # Set default templates for groups
        monorepo_templates = registry.get_templates(group="monorepo")
        if monorepo_templates:
            registry.set_default_template("monorepo", monorepo_templates[0].location)

        package_templates = registry.get_templates(group="package")
        if package_templates:
            registry.set_default_template("package", package_templates[0].location)

        return registry

    def create_interactive(
        self,
        template: str | None = None,
        project_name: str | None = None,
        output_dir: str = ".",
        params: list[str] | None = None,
        params_file: str | None = None,
        edit: bool = False,
        template_group: str | None = None,
    ) -> None:
        """
        Create a new project from a template in interactive mode.

        This is the main creation command that handles all the logic for
        creating a project from a template.
        """
        # Select template
        template_config = self.selector.select_template_interactively(
            self.registry, template_name=template, group=template_group
        )

        if not template_config:
            sys.exit(1)

        # Display template information
        console.print(
            Panel(
                f"[bold]{template_config.name}[/bold]\n{template_config.description}",
                title="[cyan]Selected Template[/cyan]",
                border_style="cyan",
            )
        )

        # Prepare CLI arguments
        cli_args = {"project_name": project_name} if project_name else {}

        # Load parameters from various sources
        loaded_params = {}

        # 1. Load from YAML file if provided
        if params_file:
            loaded_params.update(self.param_handler.load_params_from_yaml(params_file))
            console.print(f"[green]Loaded parameters from: {params_file}[/green]")

        # 2. Parse k=v parameters from command line
        if params:
            kv_params = self.param_handler.parse_key_value_params(params)
            loaded_params.update(kv_params)
            if kv_params:
                console.print(f"[green]Applied command-line parameters: {list(kv_params.keys())}[/green]")

        # 3. Handle interactive editor mode
        if edit:
            editor_params = self.param_handler.interactive_editor_mode(template_config, loaded_params)
            loaded_params.update(editor_params)
            console.print("[green]Applied parameters from editor[/green]")

        # Merge all parameters
        cli_args.update(loaded_params)

        # Prompt for template questions (will skip those already provided)
        answers = self.renderer.prompt_template_questions(template_config, cli_args)

        # Build context
        context = answers.copy()
        additional_context = template_config.build_context(context)
        context.update(additional_context)

        # Get project directory name
        project_name = template_config.get_project_directory_name(context)
        project_path = pathlib.Path(output_dir) / project_name

        # Check if project directory already exists
        if project_path.exists():
            console.print(f"[red]Directory '{project_path}' already exists![/red]")
            if not questionary.confirm("Do you want to overwrite it?", default=False).ask():
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(1)

        # Create the project
        template_path = self.templates_dir / template_config.location

        self.renderer.create_project(template_config, template_path, str(project_path), context)

        # Run post-creation hooks
        self._run_post_creation_hooks(project_path, context, template_config)

        # Show next steps
        console.print("\n[bold cyan]Next steps:[/bold cyan]")
        console.print(f"  cd {project_name}")
        console.print("  # Review the generated project structure")
        console.print("  # Start developing!")

    def list_templates(self, group: str | None = None) -> None:
        """
        List available templates, optionally filtered by group.

        Args:
            group: Optional group to filter templates
        """
        templates = self.registry.get_templates(group=group) if group else self.registry.get_templates()

        if not templates:
            console.print(f"[red]No templates found{f' in group {group}' if group else ''}![/red]")
            return

        console.print("[bold cyan]Available Templates:[/bold cyan]\n")

        # Group templates by their group for better display
        grouped = {}
        for tmpl in templates:
            if tmpl.template_group not in grouped:
                grouped[tmpl.template_group] = []
            grouped[tmpl.template_group].append(tmpl)

        for grp, tmpls in grouped.items():
            console.print(f"[bold yellow]{grp}:[/bold yellow]")
            for tmpl in tmpls:
                console.print(f"  [green]{tmpl.location}[/green] - {tmpl.description}")
            console.print()

    def dump_defaults(self, template: str | None = None, output_file: str | None = None) -> None:
        """
        Dump default values of a template configuration.

        Args:
            template: Template to dump defaults for (interactive selection if not provided)
            output_file: Optional file to save the defaults to
        """
        # Select template
        template_config = self.selector.select_template_interactively(self.registry, template_name=template)

        if not template_config:
            sys.exit(1)

        # Get defaults as YAML
        yaml_output = self.param_handler.dump_defaults_to_yaml(template_config)

        # Save to file or print to stdout
        if output_file:
            with open(output_file, "w") as f:
                f.write(yaml_output)
            console.print(f"[green]Defaults saved to: {output_file}[/green]")
        else:
            # Print to stdout (not using console.print to avoid formatting)
            print(yaml_output)

    def _run_post_creation_hooks(
        self, project_path: pathlib.Path, context: dict[str, Any], template_config: TemplateConfig
    ) -> None:
        """
        Run post-creation hooks.

        Args:
            project_path: Path to the created project
            context: Template context with user answers
            template_config: The template configuration being used
        """
        for hook_config in self.post_creation_hooks:
            # Check if it's a HookConfig object or plain function (for backward compatibility)
            if hasattr(hook_config, "should_run"):
                # HookConfig object
                if hook_config.should_run(template_config.location, template_config.template_group):
                    try:
                        console.print(f"[cyan]Running hook: {hook_config.name}[/cyan]")
                        hook_config.hook(project_path, context, console)
                    except Exception as e:
                        console.print(f"[yellow]Warning: Hook {hook_config.name} failed with error: {e}[/yellow]")
            else:
                # Plain function (backward compatibility)
                try:
                    hook_config(project_path, context, console)
                except Exception as e:
                    hook_name = getattr(hook_config, "__name__", "unknown")
                    console.print(f"[yellow]Warning: Hook {hook_name} failed with error: {e}[/yellow]")

    def open_file_in_editor_and_read(self, text: str) -> str | None:
        """
        Open temporary text file to edit and read it.

        Args:
            text: Text displayed in the editor
        """
        editor = os.environ.get("EDITOR")
        if not editor:
            raise OSError("The $EDITOR environment variable is not set. Please set it (e.g., export EDITOR=nano)")

        if not shutil.which(editor.split()[0]):
            raise FileNotFoundError(f"Editor '{editor}' not found in PATH.")

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode="r+", delete=False) as tf:
            temp_file_path = tf.name
            tf.write(text)
            tf.flush()

        try:
            # Open the editor and wait
            subprocess.run([*editor.split(), temp_file_path], check=True)

            # After editor closes, read contents
            with open(temp_file_path, encoding="utf-8") as f:
                lines = f.readlines()

            # Filter out comments and empty lines
            instructions = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

            if not instructions:
                console.print("[red]The file was not edited. Exiting.[/red]")
                return None

            return "\n".join(instructions)

        except subprocess.CalledProcessError:
            console.print("[red]Editor exited with non-zero status. Aborting.[/red]")
            return None

        finally:
            os.unlink(temp_file_path)


def create_app(
    templates_dir: pathlib.Path, post_creation_hooks: list | None = None, template_group: str | None = None
) -> typer.Typer:
    """
    Create a Typer app with all template commands registered.

    Args:
        templates_dir: Path to the templates directory
        post_creation_hooks: Optional list of hook functions to run after project creation
        template_group: Optional template group to filter templates
    Returns:
        Configured Typer app
    """
    app = typer.Typer(
        name="create-ds-app",
        help="Set up a modern data science project by running one command",
    )

    cli = CLICommands(templates_dir, post_creation_hooks=post_creation_hooks)

    # Register the main callback for empty command (interactive mode)
    @app.callback(invoke_without_command=True)
    def main(
        ctx: typer.Context,
        template: str = typer.Option(None, "--template", "-t", help="Template to use"),
        project_name: str = typer.Option(None, "--project-name", "-n", help="Name of the project"),
        output_dir: str = typer.Option(".", "--output", "-o", help="Output directory"),
        params: list[str] = typer.Option([], "--param", "-p", help="Set parameters as key=value pairs"),
        params_file: str = typer.Option(None, "--params-file", "-f", help="Load parameters from YAML file"),
        edit: bool = typer.Option(False, "--edit", "-e", help="Open parameters in $EDITOR before creating project"),
    ):
        """
        Create a new data science project from a template.

        When run without subcommands, enters interactive mode.
        """
        if ctx.invoked_subcommand is None:
            # No subcommand - run interactive mode
            cli.create_interactive(
                template=template,
                project_name=project_name,
                output_dir=output_dir,
                params=params,
                params_file=params_file,
                edit=edit,
                template_group=template_group,
            )

    @app.command("list")
    def list_command(
        group: str = typer.Argument(None, help="Template group to filter by"),
    ):
        """List available templates, optionally filtered by group."""
        cli.list_templates(group=group)

    @app.command("dump-defaults")
    def dump_defaults_command(
        template: str = typer.Option(None, "--template", "-t", help="Template to dump defaults for"),
        output: str = typer.Option(None, "--output", "-o", help="File to save defaults to"),
    ):
        """Dump default values of a template configuration."""
        cli.dump_defaults(template=template, output_file=output)

    return app
