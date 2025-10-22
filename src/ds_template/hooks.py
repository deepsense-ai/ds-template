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

import pathlib
import subprocess
import traceback
from typing import Any

import questionary
from ds_templater import HookConfig
from rich.console import Console

import ds_template
from ds_template.package_generator import PackageGenerator


def _get_available_package_types() -> dict[str, str]:
    """
    Get available package types from the package generator.

    Returns:
        Dictionary mapping package type names to their descriptions
    """
    generator = PackageGenerator(pathlib.Path(__file__).parent.parent.parent / "templates")
    generator.registry.discover_templates()
    package_templates = generator.registry.get_templates(group="package")

    result = {}
    for template in package_templates:
        result[template.location] = template.description
    return result


def _get_package_choices() -> list[dict[str, str]]:
    """Get package type choices for multi-select question."""
    package_types = _get_available_package_types()
    choices = []
    for pkg_type, description in package_types.items():
        # Extract display name from package type (e.g., "pkg_api" -> "API")
        display_name = pkg_type.replace("pkg_", "").replace("_", " ").title()
        choices.append({"name": f"{display_name} - {description}", "value": pkg_type})
    return choices


def generate_packages_hook(project_path: pathlib.Path, context: dict[str, Any], console: Console) -> None:
    """
    Generate selected packages if user chose manual package generation.

    Args:
        project_path: Path to the created project
        context: Template context with user answers
        console: Rich console for output
    """
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

    project_name = context.get("project_name", "my-ds-project")

    try:
        templates_dir = pathlib.Path(ds_template.__file__).parent.parent.parent / "templates"
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
                pkg_name = f"{project_name.replace('-', '_')}_{suffix}"

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

        console.print(f"[dim]{traceback.format_exc()}[/dim]")


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
        subprocess.run(["uv", "sync"], cwd=project_path, capture_output=True, text=True, check=True)  # noqa: S607
        console.print("[green]✓ Dependencies installed successfully![/green]")
    except subprocess.CalledProcessError as e:
        console.print("[yellow]Warning: uv sync failed with error:[/yellow]")
        console.print(f"[yellow]{e.stderr}[/yellow]")
        console.print("[yellow]You may need to run 'uv sync' manually.[/yellow]")
    except FileNotFoundError:
        console.print("[yellow]Warning: uv is not installed. Please install uv and run 'uv sync' manually.[/yellow]")


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
]
