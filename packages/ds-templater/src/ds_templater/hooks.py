"""
Hook system for template post-generation actions.
"""

import pathlib
from dataclasses import dataclass
from typing import Any, Callable

from rich.console import Console


@dataclass
class HookConfig:
    """Configuration for a post-generation hook with filter criteria."""

    # The hook function to execute
    hook: Callable[[pathlib.Path, dict[str, Any], Console], None]

    # Name of the hook for logging
    name: str

    # Filter criteria - if specified, hook only runs for matching templates
    template_names: list[str] | None = None  # Only run for specific template names
    template_groups: list[str] | None = None  # Only run for specific template groups
    exclude_names: list[str] | None = None  # Don't run for these template names
    exclude_groups: list[str] | None = None  # Don't run for these template groups

    def should_run(self, template_name: str, template_group: str) -> bool:
        """
        Check if this hook should run for the given template.

        Args:
            template_name: Name/location of the template
            template_group: Group of the template

        Returns:
            True if the hook should run, False otherwise
        """
        # Check exclusions first
        if self.exclude_names and template_name in self.exclude_names:
            return False
        if self.exclude_groups and template_group in self.exclude_groups:
            return False

        # Check inclusions (if specified, template must match)
        if self.template_names and template_name not in self.template_names:
            return False
        if self.template_groups and template_group not in self.template_groups:
            return False

        return True