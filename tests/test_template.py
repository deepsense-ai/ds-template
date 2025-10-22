import tempfile
from pathlib import Path

import pytest
import tomlkit

from ds_template.banners import BLUE, RESET, create_banner, create_divider, join_multiline_texts, wrap_with_dividers
from ds_template.hooks import _get_available_package_types, _get_package_choices
from ds_template.main import TEMPLATES_DIR, entrypoint
from ds_template.package_generator import PackageGenerator


def test_banners_join_multiline_texts():
    """Test joining two multi-line texts side by side."""
    left = "line1\nline2"
    right = "right1\nright2\nright3"
    result = join_multiline_texts(left, right, spacing=2)

    lines = result.split("\n")
    assert len(lines) == 3  # max height of both inputs
    assert "line1" in lines[0]
    assert "right1" in lines[0]
    assert "line2" in lines[1]
    assert "right2" in lines[1]
    assert "right3" in lines[2]


def test_banners_create_divider():
    """Test divider creation with specified width."""
    width = 10
    divider = create_divider(width)
    assert divider.startswith(BLUE)
    assert divider.endswith(RESET)
    # Check that the actual divider content has the right width
    content = divider[len(BLUE) : len(divider) - len(RESET)]
    assert len(content) == width
    assert content == "═" * width


def test_banners_wrap_with_dividers():
    """Test wrapping content with dividers."""
    content = "test content"
    width = 20
    wrapped = wrap_with_dividers(content, width)

    lines = wrapped.split("\n")
    assert len(lines) == 3  # top divider, content, bottom divider
    assert lines[0] == lines[2]  # top and bottom dividers should be identical
    assert lines[1] == content


def test_banners_create_banner():
    """Test banner creation with project info."""
    project_info = "Test Project\nVersion 1.0"
    banner = create_banner(project_info)

    assert isinstance(banner, str)
    assert len(banner) > 0
    # Should contain dividers (blue equals signs)
    assert "═" in banner
    # Should contain project info
    assert "Test Project" in banner
    assert "Version 1.0" in banner


def test_package_generator_find_project_root():
    """Test finding project root with valid pyproject.toml."""
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create a valid pyproject.toml with workspace config
        pyproject_content = {"tool": {"uv": {"workspace": {"members": ["packages/*"]}}}}

        pyproject_path = temp_path / "pyproject.toml"
        with open(pyproject_path, "w") as f:
            f.write(tomlkit.dumps(pyproject_content))

        # Create packages directory
        (temp_path / "packages").mkdir()

        generator = PackageGenerator(Path(__file__).parent.parent / "templates")
        found_root = generator.find_project_root(temp_path)

        assert found_root == temp_path


def test_package_generator_find_project_root_not_found():
    """Test that ValueError is raised when no project root is found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        generator = PackageGenerator(Path(__file__).parent.parent / "templates")

        with pytest.raises(ValueError, match="No valid monorepo project root found"):
            generator.find_project_root(temp_path)


def test_package_generator_find_packages_directory():
    """Test finding packages directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        packages_dir = temp_path / "packages"
        packages_dir.mkdir()

        generator = PackageGenerator(Path(__file__).parent.parent / "templates")
        found_packages = generator.find_packages_directory(temp_path)

        assert found_packages == packages_dir


def test_package_generator_find_packages_directory_not_found():
    """Test that ValueError is raised when packages directory is not found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        generator = PackageGenerator(Path(__file__).parent.parent / "templates")

        with pytest.raises(ValueError, match="Packages directory not found"):
            generator.find_packages_directory(temp_path)


def test_hooks_get_available_package_types():
    """Test getting available package types from hooks."""
    package_types = _get_available_package_types()

    assert isinstance(package_types, dict)
    # Should have some package types available
    assert len(package_types) > 0
    # All values should be strings (descriptions)
    for description in package_types.values():
        assert isinstance(description, str)


def test_hooks_get_package_choices():
    """Test getting package choices for multi-select."""
    choices = _get_package_choices()

    assert isinstance(choices, list)
    assert len(choices) > 0

    for choice in choices:
        assert "name" in choice
        assert "value" in choice
        assert isinstance(choice["name"], str)
        assert isinstance(choice["value"], str)
        assert choice["value"].startswith("pkg_")


def test_main_entrypoint_import():
    """Test that main module can be imported and has expected functions."""
    assert callable(entrypoint)
    assert isinstance(TEMPLATES_DIR, Path)
    assert TEMPLATES_DIR.exists()
