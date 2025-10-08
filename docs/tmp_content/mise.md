# Mise - version manager for programming languages and development tools

For safe and convenient management of virtual environments, dependencies, and project setup, this project uses **[mise](https://mise.jdx.dev)**.

Below you'll find instructions on how to install, automate, and use `mise` effectively in your Bash environment.

## 1. Installation

To use `mise`, you need to install it globally on your system.

#### Step 1: Install `mise`
Run the official installation script or follow the [installation guide](https://mise.jdx.dev/installing-mise.html):
```bash
curl https://mise.run | sh
```

#### Step 2: Verify the installation
Make sure `mise` is available in your shell:
```bash
which mise # should output a path like: /usr/local/bin/mise
```

## 2. Enable Experimental Hooks
Mise hooks are experimental, so enable them globally once:
```bash
mise settings set experimental true
```
## 3. Automate Mise in Every Bash Session
Add the following line to your ~/.bashrc to activate mise automatically whenever you start a new terminal:
```bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
source ~/.bashrc
```
This allows mise to:
- Detect `mise.toml` in project directories
- Run configured hooks automatically (e.g. enter, cd, leave)
- Manage virtual environments and environment variables seamlessly

## 4. Set up Your Project with mise.toml
Place a mise.toml file in your project root, for example:
```toml
[env]
_.python.venv = ".venv"  # Automatically activate your Python virtual environment

[hooks.enter]
script = """
echo '[mise] Welcome to the project!'
uv sync                # Sync your Python dependencies automatically on entering the project
echo '[mise] Environment ready.'
"""
```
## 5. Trust Your Project with mise trust

Before mise can run hooks or activate environments defined in mise.toml, you must explicitly trust the project. 
This is a security feature to prevent untrusted scripts from running automatically.

Run the following inside your project directory:
```bash
mise trust
```

This will add the project path to your trusted list, enabling all configured hooks and features.
If you ever want to remove trust from a directory:
```bash
mise untrust
```

You can also list all trusted paths:
```bash
mise trust list
```

## 6. Using Mise in Your Workflow
- Open a new terminal (or reload your shell).
- cd into your project directory.
- if it is a new project, use command `mise trust`
- Mise will automatically activate your venv and run your enter hook (uv sync and welcome messages).
- You can add additional hooks (leave, cd, preinstall, postinstall) as needed in .mise.toml.
## 7. Optional: Define Custom Commands with just
To define reusable commands, consider adding a justfile:

```makefile
run-package:
    uv run path_to/run-package
```

Run commands easily via:

```bash
just run-package
```

Feel free to adapt this to your project structure! For details and additional functionalities, 
visit [https://mise.jdx.dev](https://mise.jdx.dev).
