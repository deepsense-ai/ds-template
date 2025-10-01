"""
Main entry point for create-ds-app CLI.
"""

import pathlib

from ds_templater import create_app

# Get templates directory relative to this file
TEMPLATES_DIR = pathlib.Path(__file__).parent.parent.parent / "templates"


def entrypoint() -> None:
    """Main entry point for the CLI."""
    app = create_app(templates_dir=TEMPLATES_DIR)
    app()


if __name__ == "__main__":
    entrypoint()