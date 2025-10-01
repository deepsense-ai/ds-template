"""
CLI interface for ds-repo.
"""

import pathlib
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .repo import RepoInfo

app = typer.Typer(
    name="ds-repo",
    help="CLI tool for data science repository management",
    add_completion=False,
)
console = Console()


@app.command()
def info(
    path: Optional[pathlib.Path] = typer.Argument(None, help="Path to the repository (default: current directory)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
) -> None:
    """
    Show repository information.

    Finds the root pyproject.toml and displays basic project info.
    """
    if path is None:
        path = pathlib.Path.cwd()

    try:
        repo_info = RepoInfo(path)
        project_info = repo_info.get_project_info()

        # Create a table for project information
        table = Table(show_header=False, box=None)
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        # Add basic info
        table.add_row("Project Name", project_info["name"])
        table.add_row("Version", project_info["version"])
        table.add_row("Root Path", str(project_info["root_path"]))

        if project_info.get("description"):
            table.add_row("Description", project_info["description"])

        if project_info.get("python_version"):
            table.add_row("Python Version", project_info["python_version"])

        # Show project type
        if project_info.get("is_monorepo"):
            table.add_row("Type", "Monorepo")
            if verbose and project_info.get("packages"):
                packages_str = ", ".join(project_info["packages"])
                table.add_row("Packages", packages_str)
        else:
            table.add_row("Type", "Single Package")

        # Display the table in a panel
        panel = Panel(
            table,
            title=f"[bold blue]{project_info['name']}[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
        console.print(panel)

        # Show additional details if verbose
        if verbose:
            if project_info.get("dependencies"):
                console.print("\n[bold cyan]Dependencies:[/bold cyan]")
                for dep in project_info["dependencies"]:
                    console.print(f"  • {dep}")

            if project_info.get("dev_dependencies"):
                console.print("\n[bold cyan]Dev Dependencies:[/bold cyan]")
                for dep in project_info["dev_dependencies"]:
                    console.print(f"  • {dep}")

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error reading project info:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def validate(
    path: Optional[pathlib.Path] = typer.Argument(None, help="Path to the repository (default: current directory)"),
) -> None:
    """
    Validate the repository structure and configuration.
    """
    if path is None:
        path = pathlib.Path.cwd()

    console.print("[yellow]Repository validation not yet implemented[/yellow]")
    console.print("This command will check:")
    console.print("  • Project structure consistency")
    console.print("  • Configuration file validity")
    console.print("  • Dependency conflicts")
    console.print("  • Code style compliance")


@app.command()
def deps(
    path: Optional[pathlib.Path] = typer.Argument(None, help="Path to the repository (default: current directory)"),
    check: bool = typer.Option(False, "--check", help="Check for outdated dependencies"),
    update: bool = typer.Option(False, "--update", help="Update dependencies"),
) -> None:
    """
    Manage project dependencies.
    """
    if path is None:
        path = pathlib.Path.cwd()

    console.print("[yellow]Dependency management not yet implemented[/yellow]")
    console.print("This command will allow you to:")
    console.print("  • List all project dependencies")
    console.print("  • Check for outdated packages")
    console.print("  • Update dependencies safely")
    console.print("  • Resolve dependency conflicts")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
