# CLI Package Usage

This package provides a command-line interface using **Typer** for fast and modern CLI development.

## Key Features

- **Typer Integration**: Built on Typer for type-safe CLI development
- **Automatic Help**: Commands automatically generate help text
- **Type Validation**: Input validation based on Python type hints
- **Rich Output**: Beautiful terminal output with colors and formatting

## Usage Examples

### Basic Command Structure
```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str = typer.Argument(..., help="Name to greet")):
    typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

### Running Commands
```bash
# Install the package
uv pip install -e packages/<package_name>

# Run the CLI
<cli_command> --help
<cli_command> hello John
```

### Advanced Features
- **Subcommands**: Organize commands into groups
- **Options**: Add flags and options with validation
- **Callbacks**: Execute code before/after commands
- **Progress Bars**: Show progress for long operations
- **Confirmation**: Ask for user confirmation

## Development
- Main CLI logic in `cli.py`
- Add new commands by decorating functions with `@app.command()`
- Use `typer.echo()` for output instead of `print()`
- Leverage type hints for automatic validation