"""
Template registry for managing and discovering templates.
"""

import importlib.util
import pathlib
import sys

from loguru import logger

from .config import TemplateConfig


class TemplateRegistry:
    """Registry for managing templates."""

    def __init__(self, templates_dir: pathlib.Path | None = None):
        """
        Initialize the template registry.

        Args:
            templates_dir: Directory containing templates. If None, templates must be registered manually.
        """
        self.templates_dir = templates_dir
        self._templates: dict[str, TemplateConfig] = {}
        self._default_groups: dict[str, str] = {}

    def register_template(self, template_config: TemplateConfig) -> None:
        """
        Register a template configuration.

        Args:
            template_config: The template configuration to register.
        """
        self._templates[template_config.location] = template_config
        logger.debug(f"Registered template: {template_config.name} ({template_config.location})")

    def register_template_from_path(self, template_path: pathlib.Path) -> TemplateConfig | None:
        """
        Register a template from a file path.

        Args:
            template_path: Path to the template directory containing template_config.py.

        Returns:
            The registered template configuration, or None if loading failed.
        """
        config_path = template_path / "template_config.py"
        if not config_path.exists():
            logger.warning(f"No template_config.py found at {template_path}")
            return None

        # Use importlib to safely load the module
        module_name = f"template_config_{template_path.name}"
        spec = importlib.util.spec_from_file_location(module_name, config_path)
        if spec is None or spec.loader is None:
            logger.error(f"Failed to load spec for {config_path}")
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
            # Look for a 'config' variable which should be an instance of TemplateConfig
            if hasattr(module, "config"):
                template_config = module.config
                self.register_template(template_config)
                return template_config
            else:
                logger.warning(f"No 'config' variable found in {config_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading template config from {config_path}: {e}")
            return None

    def discover_templates(self) -> None:
        """
        Discover and register all templates in the templates directory.
        """
        if not self.templates_dir or not self.templates_dir.exists():
            logger.warning(f"Templates directory does not exist: {self.templates_dir}")
            return

        for template_dir in self.templates_dir.iterdir():
            if template_dir.is_dir():
                self.register_template_from_path(template_dir)

    def get_template(self, location: str) -> TemplateConfig | None:
        """
        Get a template by its location.

        Args:
            location: The location (directory name) of the template.

        Returns:
            The template configuration, or None if not found.
        """
        return self._templates.get(location)

    def get_templates(self, group: str | None = None) -> list[TemplateConfig]:
        """
        Get all templates, optionally filtered by group.

        Args:
            group: The template group to filter by. If None, returns all templates.

        Returns:
            List of template configurations.
        """
        templates = list(self._templates.values())

        if group is not None:
            templates = [t for t in templates if t.template_group == group]

        return templates

    def get_groups(self) -> list[str]:
        """
        Get all unique template groups.

        Returns:
            List of unique template group names.
        """
        groups = set()
        for template in self._templates.values():
            groups.add(template.template_group)
        return sorted(list(groups))

    def set_default_template(self, group: str, template_location: str) -> None:
        """
        Set the default template for a group.

        Args:
            group: The template group.
            template_location: The location of the default template for this group.
        """
        if template_location not in self._templates:
            raise ValueError(f"Template '{template_location}' not found in registry")

        template = self._templates[template_location]
        if template.template_group != group:
            raise ValueError(
                f"Template '{template_location}' belongs to group '{template.template_group}', not '{group}'"
            )

        self._default_groups[group] = template_location

    def get_default_template(self, group: str) -> TemplateConfig | None:
        """
        Get the default template for a group.

        Args:
            group: The template group.

        Returns:
            The default template configuration for the group, or None if not set.
        """
        location = self._default_groups.get(group)
        if location:
            return self._templates.get(location)
        return None

    def clear(self) -> None:
        """Clear all registered templates."""
        self._templates.clear()
        self._default_groups.clear()
