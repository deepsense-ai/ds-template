# CLI Package Rules

This package provides a command-line interface using **Typer** and **Rich** for modern, type-safe CLI development.

## Command Structure Rules

- **ALWAYS** use Typer: `import typer` then `app = typer.Typer()`
- **ALWAYS** use Rich Console for output: `from rich.console import Console` then `console = Console()`
- **NEVER** use `print()` - use `console.print()` or `typer.echo()`
- Main entry point must be `main()` function that calls `app()`

## Command Definition Rules

- Decorate commands with `@app.command()`
- **ALWAYS** use type hints for parameters (enables automatic validation)
- Commands must return `None` (they don't return values)
- **MUST** include docstrings (these become help text automatically)

## Options and Arguments Rules

- Use `typer.Option()` for flags and optional parameters
- Use `typer.Argument()` for positional arguments
- Provide help text for all options and arguments

## Output Rules

- **ALWAYS** use Rich components for enhanced UX (Panel, Table, Progress, etc.)
- Use Rich styling for colors and formatting
- Structure output with Rich tables for tabular data

## Subcommands Rules

- Create subcommands using separate `typer.Typer()` instances
- Add subcommands via `app.add_typer(subcommand_app, name="subcommand_name")`

## Error Handling Rules

- Use `from typer import Exit` for error exits
- **MUST** raise `Exit(code=1)` for error conditions
- Use `console.print()` with red styling for errors: `[red]Error:[/red]`

## File Structure Rules

- Main CLI logic in `cli.py` with `main()` entry point
- Console script configured in `pyproject.toml` under `[project.scripts]`
