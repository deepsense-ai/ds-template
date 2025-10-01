"""
Repository information and management utilities.
"""

import pathlib
import tomllib
from typing import Any, Optional


class RepoInfo:
    """Handles repository information extraction and analysis."""

    def __init__(self, path: pathlib.Path):
        """
        Initialize RepoInfo with a path.

        Args:
            path: Path to start searching for the repository root.
        """
        self.start_path = path.resolve()
        self.root_path = self._find_root()
        self.pyproject_path = self.root_path / "pyproject.toml"

    def _find_root(self) -> pathlib.Path:
        """
        Find the repository root by looking for pyproject.toml.

        Returns:
            Path to the repository root.

        Raises:
            FileNotFoundError: If no pyproject.toml is found.
        """
        current = self.start_path
        if current.is_file():
            current = current.parent

        while current != current.parent:
            if (current / "pyproject.toml").exists():
                return current
            current = current.parent

        raise FileNotFoundError(
            f"No pyproject.toml found in {self.start_path} or any parent directory. "
            "Please run this command from within a project directory."
        )

    def _read_pyproject(self) -> dict[str, Any]:
        """
        Read and parse the pyproject.toml file.

        Returns:
            Parsed pyproject.toml content.
        """
        with open(self.pyproject_path, "rb") as f:
            return tomllib.load(f)

    def get_project_info(self) -> dict[str, Any]:
        """
        Get comprehensive project information.

        Returns:
            Dictionary containing project information.
        """
        pyproject = self._read_pyproject()
        project = pyproject.get("project", {})

        info = {
            "name": project.get("name", "unknown"),
            "version": project.get("version", "unknown"),
            "description": project.get("description", ""),
            "root_path": self.root_path,
            "python_version": project.get("requires-python", None),
        }

        # Check if it's a monorepo
        packages_dir = self.root_path / "packages"
        if packages_dir.exists() and packages_dir.is_dir():
            info["is_monorepo"] = True
            info["packages"] = self._find_packages(packages_dir)
        else:
            info["is_monorepo"] = False

        # Get dependencies
        info["dependencies"] = project.get("dependencies", [])

        # Get dev dependencies (check various common locations)
        dev_deps = []
        if "tool" in pyproject:
            # Check uv dev-dependencies
            if "uv" in pyproject["tool"] and "dev-dependencies" in pyproject["tool"]["uv"]:
                dev_deps.extend(pyproject["tool"]["uv"]["dev-dependencies"])
            # Check poetry dev-dependencies
            elif "poetry" in pyproject["tool"] and "group" in pyproject["tool"]["poetry"]:
                for group in pyproject["tool"]["poetry"]["group"].values():
                    if "dependencies" in group:
                        dev_deps.extend(group["dependencies"].keys())

        info["dev_dependencies"] = dev_deps

        return info

    def _find_packages(self, packages_dir: pathlib.Path) -> list[str]:
        """
        Find all packages in the packages directory.

        Args:
            packages_dir: Path to the packages directory.

        Returns:
            List of package names.
        """
        packages = []
        for item in packages_dir.iterdir():
            if item.is_dir() and (item / "pyproject.toml").exists():
                try:
                    with open(item / "pyproject.toml", "rb") as f:
                        pkg_pyproject = tomllib.load(f)
                        pkg_name = pkg_pyproject.get("project", {}).get("name", item.name)
                        packages.append(pkg_name)
                except Exception:
                    # If we can't read the pyproject.toml, use the directory name
                    packages.append(item.name)
        return sorted(packages)

    def get_package_info(self, package_name: str) -> Optional[dict[str, Any]]:
        """
        Get information about a specific package in a monorepo.

        Args:
            package_name: Name of the package.

        Returns:
            Dictionary containing package information, or None if not found.
        """
        packages_dir = self.root_path / "packages"
        if not packages_dir.exists():
            return None

        # Try to find the package
        for item in packages_dir.iterdir():
            if item.is_dir() and item.name == package_name:
                pkg_pyproject_path = item / "pyproject.toml"
                if pkg_pyproject_path.exists():
                    try:
                        with open(pkg_pyproject_path, "rb") as f:
                            pkg_pyproject = tomllib.load(f)
                            project = pkg_pyproject.get("project", {})
                            return {
                                "name": project.get("name", package_name),
                                "version": project.get("version", "unknown"),
                                "description": project.get("description", ""),
                                "path": item,
                                "dependencies": project.get("dependencies", []),
                            }
                    except Exception as e:
                        return {"error": str(e), "path": item}

        return None
