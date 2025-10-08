"""
Standalone script to add packages to existing monorepo projects.
"""

import argparse
import pathlib
import sys
from typing import Optional

# Add the src directory to the path so we can import our modules
script_dir = pathlib.Path(__file__).parent
src_dir = script_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from create_ds_app.package_generator import PackageGenerator


def add_package(
    project_root: pathlib.Path, package_name: str, package_type: str, templates_dir: Optional[pathlib.Path] = None
) -> bool:
    """
    Add a new package to an existing monorepo project.

    Args:
        project_root: Path to the monorepo project root
        package_name: Name of the package to create
        package_type: Type of package ("cli" or "lib")
        templates_dir: Path to templates directory (optional)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Set default templates directory
        if templates_dir is None:
            templates_dir = script_dir.parent / "templates"

        # Initialize package generator
        generator = PackageGenerator(templates_dir)

        # Resolve project root
        project_root = project_root.resolve()

        print(f"Using project root: {project_root}")

        # Validate project root
        try:
            generator.find_project_root(project_root)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        # Map type to template name
        template_map = {
            "cli": "pkg_frontend_streamlit",
            # "lib": "pkg_lib"
        }

        if package_type not in template_map:
            print(f"Error: Invalid package type '{package_type}'. Must be 'cli' or 'lib'")
            return False

        template_name = template_map[package_type]

        # Generate package
        print(f"Creating {package_type} package '{package_name}' using template '{template_name}'...")

        # Get additional parameters for the template
        from create_ds_app.template_utils import get_template_defaults
        
        # Get project name from pyproject.toml or use default
        project_name = "my-project"  # Default fallback
        try:
            import tomllib
            pyproject_path = project_root / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    pyproject_data = tomllib.load(f)
                    project_name = pyproject_data.get("project", {}).get("name", project_name)
        except Exception:
            pass  # Use default if we can't read pyproject.toml
        
        context = get_template_defaults(template_name, package_name, project_name)

        # Find packages directory
        packages_dir = generator.find_packages_directory(project_root)
        output_dir = packages_dir / package_name

        # Generate the package
        generator.generate_package(
            template_name=template_name, package_name=package_name, output_dir=output_dir, **context
        )

        # Register in workspace
        generator.register_package_in_workspace(project_root, package_name)

        # Update README
        generator.update_readme_with_package(project_root, package_name, package_type)

        print(f"\n✅ Successfully created package '{package_name}'!")
        print(f"📍 Location: {output_dir}")
        print(f"🔧 Template: {template_name}")
        print("\nNext steps:")
        print(f"1. cd packages/{package_name}")
        print("2. uv sync --dev")
        print("3. Start developing!")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_add_cli_package(project_path: str):
    """Test adding a CLI package to my_ds_projectN."""
    project_root = pathlib.Path(project_path)
    package_name = "test-cli-tool"
    package_type = "cli"

    print("Testing add_package function...")
    print(f"Project root: {project_root}")
    print(f"Package name: {package_name}")
    print(f"Package type: {package_type}")
    print("-" * 50)

    success = add_package(project_root, package_name, package_type)

    if success:
        print("\n🎉 Test passed! Package created successfully.")
    else:
        print("\n❌ Test failed! Package creation failed.")

    return success


def test_add_lib_package(project_path: str):
    """Test adding a library package to my_ds_projectN."""
    project_root = pathlib.Path(project_path)
    package_name = "test-library"
    package_type = "lib"

    print("Testing add_package function...")
    print(f"Project root: {project_root}")
    print(f"Package name: {package_name}")
    print(f"Package type: {package_type}")
    print("-" * 50)

    success = add_package(project_root, package_name, package_type)

    if success:
        print("\n🎉 Test passed! Package created successfully.")
    else:
        print("\n❌ Test failed! Package creation failed.")

    return success


def main() -> None:
    parser = argparse.ArgumentParser(description="Test CLI and library package generation in a DS project.")
    parser.add_argument(
        "project_path", type=str, help="Path to the project directory where packages should be created."
    )
    args = parser.parse_args()
    project_path = args.project_path

    print("🧪 Testing package generation functionality...")
    print("=" * 60)

    # Test CLI package
    print("\n1. Testing CLI package creation:")
    cli_success = test_add_cli_package(project_path)

    print("\n" + "=" * 60)

    # Test library package
    print("\n2. Testing library package creation:")
    lib_success = test_add_lib_package(project_path)

    print("\n" + "=" * 60)
    print("\n📊 Test Results:")
    print(f"CLI package: {'✅ PASS' if cli_success else '❌ FAIL'}")
    print(f"Library package: {'✅ PASS' if lib_success else '❌ FAIL'}")

    if cli_success and lib_success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
