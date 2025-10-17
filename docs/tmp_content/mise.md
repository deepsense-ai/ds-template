# Development Environment Management

The ds-template uses **mise** for development environment management and tool versioning.

## What's Included

### mise Configuration
- **Automatic environment activation** when entering project directories
- **Tool version management** for consistent development environments
- **Hooks system** for automated setup tasks
- **Cross-platform support** for all major operating systems

### Generated mise.toml
```toml
[env]
_.python.venv = ".venv"  # Python virtual environment

[hooks.enter]
script = """
echo 'Welcome to the project!'
uv sync                # Install dependencies
echo 'Environment ready.'
"""
```

## Setup

### 1. Install mise
```bash
curl https://mise.run | sh
```

### 2. Enable in your shell
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
source ~/.bashrc  # or zsh
```

### 3. Trust the project
```bash
cd your-project
mise trust
```

## Usage

### Automatic Setup
When you `cd` into a project directory:
- **Virtual environment** is activated automatically
- **Dependencies** are synced with `uv sync`
- **Welcome message** confirms environment is ready


# Check environment status
mise status
```

## Benefits

- **Consistent environments** across team members
- **Automatic setup** reduces onboarding time
- **Tool versioning** prevents "works on my machine" issues
- **Hooks system** automates common tasks

## Customization

You can customize the environment by editing `mise.toml`:
- **Add tools** with specific versions
- **Configure hooks** for different events
- **Set environment variables** for the project
- **Define custom commands** for common tasks

For detailed configuration options, see the [mise documentation](https://mise.jdx.dev).