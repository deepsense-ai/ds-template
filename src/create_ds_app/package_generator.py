"""
Package generation functionality for adding new packages to existing projects.
"""

import pathlib
from typing import Optional

import questionary
import typer
from ds_templater import TemplateRegistry, TemplateRenderer
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from tomlkit import dumps, inline_table, parse

console = Console()


class PackageGenerator:
    """Handles generation of new packages within existing monorepo projects."""

    def __init__(self, templates_dir: pathlib.Path):
        """Initialize the package generator with templates directory."""
        self.templates_dir = templates_dir
        self.registry = TemplateRegistry(templates_dir)
        self.renderer = TemplateRenderer()
        self.coding_instructions = ""

    def find_project_root(self, start_path: pathlib.Path = None) -> pathlib.Path:
        """
        Find the project root by looking for pyproject.toml with workspace configuration.

        Args:
            start_path: Starting directory to search from (defaults to current directory)

        Returns:
            Path to the project root

        Raises:
            ValueError: If no valid project root is found
        """
        if start_path is None:
            start_path = pathlib.Path.cwd()

        current_path = start_path.resolve()

        # Walk up the directory tree looking for pyproject.toml
        while current_path != current_path.parent:
            pyproject_path = current_path / "pyproject.toml"

            if pyproject_path.exists():
                try:
                    with open(pyproject_path, encoding="utf-8") as f:
                        data = parse(f.read())

                    # Check if this is a workspace configuration
                    if "tool" in data and "uv" in data["tool"] and "workspace" in data["tool"]["uv"]:
                        workspace_config = data["tool"]["uv"]["workspace"]
                        if "members" in workspace_config:
                            logger.info(f"Found project root at: {current_path}")
                            return current_path

                except Exception as e:
                    logger.debug(f"Error reading pyproject.toml at {pyproject_path}: {e}")
                    pass

            current_path = current_path.parent

        raise ValueError(
            "No valid monorepo project root found. "
            "Make sure you're in a directory with a pyproject.toml that has workspace configuration."
        )

    def find_packages_directory(self, project_root: pathlib.Path) -> pathlib.Path:
        """
        Find the packages directory within the project root.

        Args:
            project_root: Path to the project root

        Returns:
            Path to the packages directory

        Raises:
            ValueError: If packages directory is not found
        """
        packages_dir = project_root / "packages"

        if not packages_dir.exists():
            raise ValueError(f"Packages directory not found at {packages_dir}")

        if not packages_dir.is_dir():
            raise ValueError(f"Packages path exists but is not a directory: {packages_dir}")

        logger.info(f"Found packages directory at: {packages_dir}")
        return packages_dir

    def get_available_package_templates(self) -> list[str]:
        """Get list of available package templates."""
        package_templates = []
        # First discover templates if not already done
        self.registry.discover_templates()

        # Get all package templates
        package_template_configs = self.registry.get_templates(group="package")
        for template_config in package_template_configs:
            package_templates.append(template_config.location)
        return package_templates

    def select_package_template(self) -> str:
        """Interactive selection of package template."""
        available_templates = self.get_available_package_templates()

        if not available_templates:
            raise ValueError("No package templates available")

        # Create choices with descriptions
        choices = []
        for template_name in available_templates:
            template_config = self.registry.get_template(template_name)
            if template_config:
                description = getattr(template_config, "description", "No description")
                choices.append(questionary.Choice(title=f"{template_name}: {description}", value=template_name))

        selected = questionary.select("Select package template:", choices=choices).ask()

        if not selected:
            raise typer.Abort()

        return selected

    def generate_package(
        self, template_name: str, package_name: str, output_dir: Optional[pathlib.Path] = None, **kwargs
    ) -> pathlib.Path:
        """
        Generate a new package using the specified template.

        Args:
            template_name: Name of the template to use
            package_name: Name for the new package
            output_dir: Directory to generate the package in (defaults to packages/package_name)
            **kwargs: Additional template parameters

        Returns:
            Path to the generated package directory
        """
        # Discover templates if not already done
        self.registry.discover_templates()

        template_config = self.registry.get_template(template_name)
        if not template_config:
            raise ValueError(f"Template '{template_name}' not found")

        # Set default output directory if not provided
        if output_dir is None:
            # We need to find the project root and packages directory
            project_root = self.find_project_root()
            packages_dir = self.find_packages_directory(project_root)
            output_dir = packages_dir / package_name

        # Prepare template context
        context = {"pkg_name": package_name, **kwargs}

        # Add any additional context from template config
        if hasattr(template_config, "build_context"):
            additional_context = template_config.build_context(context)
            context.update(additional_context)

        # Generate the package
        template_path = self.templates_dir / template_name
        self.renderer.create_project(
            template_config=template_config, template_path=template_path, project_path=str(output_dir), context=context
        )

        logger.info(f"Generated package '{package_name}' at {output_dir}")
        return output_dir

    def register_package_in_workspace(self, project_root: pathlib.Path, package_name: str) -> None:
        """
        Register the new package in the workspace pyproject.toml and save the updated file.

        Args:
            project_root: Path to the project root
            package_name: Name of the package to register
        """
        pyproject_path = project_root / "pyproject.toml"

        # Read current pyproject.toml
        with open(pyproject_path, encoding="utf-8") as f:
            data = parse(f.read())

        workspace_config = data.get("tool", {}).get("uv", {}).get("workspace", {})
        members = workspace_config.get("members", [])

        package_pattern = f"packages/{package_name}"
        known_first_party = (
            data.get("tool", {}).get("ruff", {}).get("lint", {}).get("isort", {}).get("known-first-party", [])
        )

        if package_pattern not in members:
            members.append(package_pattern)
            known_first_party.append(package_name)
            if "dependencies" not in data["project"]:
                data["project"]["dependencies"] = []
            data["project"]["dependencies"].append(package_name)

            if "tool" not in data:
                data["tool"] = {}
            if "uv" not in data["tool"]:
                data["tool"]["uv"] = {}
            if "workspace" not in data["tool"]["uv"]:
                data["tool"]["uv"]["workspace"] = {}
            data["tool"]["uv"]["workspace"]["members"] = members

            if "sources" not in data["tool"]["uv"]:
                data["tool"]["uv"]["sources"] = {}
            table = inline_table()
            table["workspace"] = True
            table._is_table = True  # enforce inline formatting
            data["tool"]["uv"]["sources"][package_name] = table

            if "ruff" not in data["tool"]:
                data["tool"]["ruff"] = {}
            if "lint" not in data["tool"]["ruff"]:
                data["tool"]["ruff"]["lint"] = {}
            if "isort" not in data["tool"]["ruff"]["lint"]:
                data["tool"]["ruff"]["lint"]["isort"] = {}
            if "known-first-party" not in data["tool"]["ruff"]["lint"]["isort"]:
                data["tool"]["ruff"]["lint"]["isort"]["known-first-party"] = []
            data["tool"]["ruff"]["lint"]["isort"]["known-first-party"] = known_first_party

            # Save the updated pyproject.toml
            with open(pyproject_path, "w", encoding="utf-8") as f:
                f.write(dumps(data))
            logger.info(
                f"Registered package '{package_name}' in workspace and sources, and saved updated pyproject.toml"
            )
        else:
            logger.info(f"Package '{package_name}' already registered in workspace")

    def update_readme_with_package(self, project_root: pathlib.Path, package_name: str, package_type: str) -> None:
        """
        Update README.md to include information about the new package.

        Args:
            project_root: Path to the project root
            package_name: Name of the new package
            package_type: Type of package (cli, lib, etc.)
        """
        readme_path = project_root / "README.md"

        if not readme_path.exists():
            logger.warning("README.md not found, skipping README update")
            return

        # Read current README
        with open(readme_path) as f:
            content = f.read()

        # Add package information if not already present
        package_section = f"\n## Packages\n\n- **{package_name}**: {package_type} package\n"

        if "## Packages" not in content:
            # Add packages section before the end of the file
            content += package_section
        # Check if this package is already mentioned
        elif package_name not in content:
            # Find the packages section and add the new package
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.strip() == "## Packages":
                    # Insert after the packages header
                    lines.insert(i + 1, f"- **{package_name}**: {package_type} package")
                    break
            content = "\n".join(lines)

        # Write back to file
        with open(readme_path, "w") as f:
            f.write(content)

        logger.info(f"Updated README.md with package '{package_name}'")

    def create_package_interactive(self) -> None:
        """Interactive package creation workflow."""
        try:
            # Find project root
            project_root = self.find_project_root()
            console.print(f"[green]Found project root: {project_root}[/green]")

            # Select template
            template_name = self.select_package_template()
            template_config = self.registry.templates[template_name]

            # Get package name
            package_name = questionary.text("Package name:", default="my-package").ask()

            if not package_name:
                raise typer.Abort()

            # Get additional parameters from template
            context = {"pkg_name": package_name}

            if hasattr(template_config, "questions"):
                for question in template_config.questions:
                    if question.name != "pkg_name":  # Skip pkg_name as we already have it
                        value = question.ask()
                        if value is not None:
                            context[question.name] = value

            # Generate package
            output_dir = self.generate_package(template_name, package_name, **context)

            # Register in workspace
            self.register_package_in_workspace(project_root, package_name)

            # Update README
            package_type = getattr(template_config, "description", "package")
            self.update_readme_with_package(project_root, package_name, package_type)

            console.print(
                Panel(
                    f"[green]Successfully created package '{package_name}'![/green]\n\n"
                    f"Location: {output_dir}\n"
                    f"Template: {template_name}\n\n"
                    f"Next steps:\n"
                    f"1. cd packages/{package_name}\n"
                    f"2. uv sync --dev\n"
                    f"3. Start developing!",
                    title="Package Created",
                    border_style="green",
                )
            )

        except Exception as e:
            console.print(f"[red]Error creating package: {e}[/red]")
            raise typer.Exit(1)
