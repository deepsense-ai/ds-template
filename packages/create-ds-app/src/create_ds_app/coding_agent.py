"""
Claude Code integration for create-ds-app.

This module provides integration with Claude Code to:
1. Generate follow-up questions about the project
2. Propose project structure based on user answers
3. Allow editing the structure via a tree editor
4. Generate packages and adapt them using Claude
"""

import json
import os
import pathlib
import re
import subprocess
import tempfile
from typing import Any

import yaml
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, TextBlock
from loguru import logger
from rich.console import Console
from rich.tree import Tree

from .package_generator import PackageGenerator

# Get templates directory relative to this file
TEMPLATES_DIR = pathlib.Path(__file__).parent.parent.parent / "templates"


def get_available_package_types() -> dict[str, str]:
    """
    Get available package types from the package generator.

    Returns:
        Dictionary mapping package type names to their descriptions
    """
    try:
        generator = PackageGenerator(TEMPLATES_DIR)
        generator.registry.discover_templates()
        package_templates = generator.registry.get_templates(group="package")

        result = {}
        for template in package_templates:
            result[template.location] = template.description
        return result
    except Exception as e:
        logger.warning(f"Could not get package types from registry: {e}")
        # Return fallback defaults
        return {
            "pkg_lib": "Shared library that may be used between one or more components, packaged as a Python module",
            "pkg_core": "Core logic, configuration and utilities used by every component in the project",
            "pkg_api": "RESTful API service that will be dockerized and deployed to server",
            "pkg_cli": "Developer tools, evaluation pipelines and similar utilities packaged as executable commands",
            "pkg_worker": "Dockerized background worker for processing tasks, running periodically or event-driven",
            "pkg_frontend_streamlit": "Interactive web application using Streamlit framework for rapid prototyping",
        }


def build_component_types_text() -> str:
    """Build the component types text for prompts."""
    package_types = get_available_package_types()
    lines = ["Possible component types are:", ""]
    for pkg_type, description in package_types.items():
        lines.append(f"{pkg_type}: {description}")
    return "\n".join(lines)


QUESTIONNAIRE_PROMPT_TEMPLATE = """
You will be provided with description of the project provided by the user.
Your task will be to generate follow-up questions to better understand the project requirements.

{component_types}

First you need to figure out if you need and what follow-up questions ask to the user.

Use following format:

{{
    "questions": [
      {{
        "type": "text",
        "name": "user_name",
        "message": "What is your name?",
        "default": "",
        "validate": {{
          "type": "length",
          "min": 1,
          "message": "Name cannot be empty"
        }}
      }},
      {{
        "type": "select",
        "name": "framework",
        "message": "Choose a framework:",
        "choices": [
          "React",
          "Vue",
          "Angular",
          {{"name": "Other", "value": "other"}}
        ],
        "default": "React"
      }},
      {{
        "type": "checkbox",
        "name": "features",
        "message": "Select features to include:",
        "choices": [
          {{"name": "Authentication", "value": "auth", "checked": true}},
          {{"name": "Database", "value": "db"}},
          {{"name": "API", "value": "api"}}
        ]
      }}
    ]
}}

Please respond only with JSON - no other comments.
"""

PROJECT_STRUCTURE_PROMPT_TEMPLATE = """
You will be provided with description of the project provided by the user.
Your task will be to generate tree-like structure with what components should be included into the project.

{component_types}

You will be also provided with user responses on the follow-up questions that you have previously prepared.

Please respond in following format:

{{"packages": [
    {{"type": "pkg_core", "name": "my-project", "functions": ["common configuration", "logging", "common data models and services"]}},
    {{"type": "pkg_api", "name": "my-project-api", "functions": ["REST endpoints", "authentication", "data validation"]}}
]}}

Please respond only with JSON - no other comments.
"""


def clean_and_parse_json(response_text: str) -> dict:
    """
    Clean and parse JSON from response text, handling common formatting issues.

    Args:
        response_text: Raw response text that may contain JSON

    Returns:
        Parsed JSON as dictionary

    Raises:
        json.JSONDecodeError: If JSON parsing fails after all cleaning attempts
    """
    # Remove markdown code blocks (```json, ```JSON, or just ```)
    cleaned_text = re.sub(r'```(?:json|JSON)?\s*\n?', '', response_text)
    cleaned_text = re.sub(r'```\s*$', '', cleaned_text)

    # Remove single-line comments (// comment)
    cleaned_text = re.sub(r'//[^\n]*', '', cleaned_text)

    # Remove multi-line comments (/* comment */)
    cleaned_text = re.sub(r'/\*.*?\*/', '', cleaned_text, flags=re.DOTALL)

    # Remove any text before the first { or [
    json_start = cleaned_text.find('{')
    array_start = cleaned_text.find('[')

    if json_start == -1 and array_start == -1:
        raise json.JSONDecodeError("No JSON object or array found", cleaned_text, 0)

    if json_start == -1:
        start_pos = array_start
    elif array_start == -1:
        start_pos = json_start
    else:
        start_pos = min(json_start, array_start)

    cleaned_text = cleaned_text[start_pos:]

    # Remove any text after the last } or ]
    # Find the matching closing bracket/brace
    stack = []
    end_pos = -1
    in_string = False
    escape_next = False

    for i, char in enumerate(cleaned_text):
        if escape_next:
            escape_next = False
            continue

        if char == '\\' and in_string:
            escape_next = True
            continue

        if char == '"' and not in_string:
            in_string = True
        elif char == '"' and in_string:
            in_string = False
        elif not in_string:
            if char in '{[':
                stack.append(char)
            elif char in '}]':
                if stack:
                    opening = stack.pop()
                    if (char == '}' and opening != '{') or (char == ']' and opening != '['):
                        # Mismatched brackets
                        break
                if not stack:
                    end_pos = i + 1
                    break

    if end_pos > 0:
        cleaned_text = cleaned_text[:end_pos]

    # Strip whitespace
    cleaned_text = cleaned_text.strip()

    # Try to parse the cleaned JSON
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        # If it still fails, log the cleaned text for debugging
        logger.debug(f"Failed to parse cleaned JSON: {cleaned_text[:500]}...")
        raise e


async def get_follow_up_questions(user_provided_instructions: str) -> list[dict]:
    """
    Get follow-up questions from the user provided instructions using Claude.

    Args:
        user_provided_instructions: Initial project description from the user

    Returns:
        List of question dictionaries for the questionnaire
    """
    async with ClaudeSDKClient() as client:
        # Build prompt with dynamic component types
        component_types = build_component_types_text()
        prompt = QUESTIONNAIRE_PROMPT_TEMPLATE.format(component_types=component_types)
        prompt += f"\n\nUser's project description:\n{user_provided_instructions}"
        await client.query(prompt)

        response_text = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        try:
            # Parse JSON response using robust parser
            response_json = clean_and_parse_json(response_text)
            return response_json.get("questions", [])
        except json.JSONDecodeError as e:
            logger.info(f"Raw response text: {response_text}")
            logger.exception(f"Could not parse JSON for follow-up questions: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Could not generate follow-up questions: {e}")
            raise e


async def generate_project_structure(
    user_provided_instructions: str, questionnaire_answers: dict[str, Any]
) -> dict[str, Any]:
    """
    Generate project structure based on user instructions and questionnaire answers.

    Args:
        user_provided_instructions: Initial project description
        questionnaire_answers: User's answers to follow-up questions

    Returns:
        Project structure dictionary
    """
    async with ClaudeSDKClient() as client:
        # Build prompt with dynamic component types
        component_types = build_component_types_text()
        prompt = PROJECT_STRUCTURE_PROMPT_TEMPLATE.format(component_types=component_types)
        prompt += "\n\n"
        prompt += f"User's project description:\n{user_provided_instructions}\n\n"
        prompt += f"User's answers to follow-up questions:\n{json.dumps(questionnaire_answers, indent=2)}"

        await client.query(prompt)

        response_text = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        try:
            # Parse JSON response using robust parser
            response_json = clean_and_parse_json(response_text)
            # Convert packages format to project structure format
            packages = response_json.get("packages", [])

            # Extract project name from the first core package or use default
            project_name = "my-project"
            for pkg in packages:
                if pkg.get("type") == "pkg_core":
                    project_name = pkg.get("name", "my-project")
                    break

            return {"project_name": project_name, "packages": packages}
        except json.JSONDecodeError as e:
            logger.info(f"Raw response text: {response_text}")
            logger.exception(f"Could not parse JSON for project structure: {e}")
            # Return a basic default structure on parse error
            return {
                "project_name": "my-project",
                "packages": [
                    {"name": "my-project", "type": "pkg_core", "functions": ["common configuration", "logging"]},
                    {"name": "my-project-api", "type": "pkg_api", "functions": ["REST endpoints"]}
                ]
            }
        except Exception as e:
            logger.exception(f"Could not generate project structure: {e}")
            raise e


def get_default_questions() -> list[dict]:
    """
    Get default questions if Claude fails to generate them.

    Returns:
        List of default question dictionaries
    """
    return [
        {"type": "text", "name": "project_name", "message": "What is your project name?", "default": "my-ds-project"},
        {"type": "confirm", "name": "needs_api", "message": "Will your project need an API?", "default": True},
        {
            "type": "select",
            "name": "frontend_type",
            "message": "What type of frontend do you need?",
            "choices": [
                {"name": "Streamlit (simpler)", "value": "streamlit"},
                {"name": "React (full-featured)", "value": "react"},
                {"name": "None", "value": "none"},
            ],
            "default": "streamlit",
        },
        {
            "type": "checkbox",
            "name": "additional_components",
            "message": "Select additional components:",
            "choices": [
                {"name": "Worker (background jobs)", "value": "worker"},
                {"name": "CLI tools", "value": "cli"},
                {"name": "Additional libraries", "value": "lib"},
            ],
        },
    ]


def display_project_tree(project_structure: dict[str, Any], console: Console) -> str:
    """
    Display project structure as a tree and return it as text.

    Args:
        project_structure: Project structure dictionary
        console: Rich console for output

    Returns:
        Text representation of the tree
    """
    tree = Tree(f"[bold cyan]{project_structure['project_name']}[/bold cyan]")

    # Group packages by type for better visualization
    packages_by_type = {}
    packages = project_structure.get("packages", project_structure.get("components", []))

    for package in packages:
        pkg_type = package["type"]
        if pkg_type not in packages_by_type:
            packages_by_type[pkg_type] = []
        packages_by_type[pkg_type].append(package)

    # Add packages to tree
    for pkg_type, packages in packages_by_type.items():
        type_branch = tree.add(f"[bold yellow]{pkg_type}[/bold yellow]")
        for package in packages:
            pkg_text = f"[green]{package['name']}[/green]"

            # Add functions if available
            functions = package.get("functions", [])
            if functions:
                for func in functions:
                    type_branch.add(f"  • {func}")
            else:
                type_branch.add(pkg_text)

    console.print("\n[bold]Proposed Project Structure:[/bold]")
    console.print(tree)

    # Generate text representation
    text_lines = [f"{project_structure['project_name']}/"]
    for pkg_type, packages in packages_by_type.items():
        text_lines.append(f"  {pkg_type}/")
        for package in packages:
            functions_str = ", ".join(package.get("functions", []))
            text_lines.append(f"    - {package['name']}: {functions_str}")

    return "\n".join(text_lines)


def edit_project_structure(project_structure: dict[str, Any], console: Console) -> dict[str, Any] | None:
    """
    Open project structure in editor for user modification using YAML format.

    Args:
        project_structure: Project structure dictionary
        console: Rich console for output

    Returns:
        Updated project structure or None if cancelled
    """
    editor = os.environ.get("EDITOR")
    if not editor:
        console.print(
            "[yellow]Warning: The $EDITOR environment variable is not set. Skipping structure editing.[/yellow]"
        )
        return None

    # Convert project structure to YAML
    yaml_content = yaml.dump(project_structure, default_flow_style=False, sort_keys=False, indent=2)

    # Create a temporary file with instructions and YAML content
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as tf:
        temp_file_path = tf.name
        tf.write("# Edit your project structure below in YAML format.\n")
        tf.write("# You can modify the project_name, and add/remove/edit packages.\n")
        tf.write("# Each package should have: name, type, and functions (list).\n\n")
        tf.write(yaml_content)

    try:
        # Open the editor
        subprocess.run([editor, temp_file_path], check=True)

        # Read and parse the edited structure
        with open(temp_file_path) as f:
            content = f.read()

        # Remove comment lines for parsing
        lines = [line for line in content.split("\n") if not line.strip().startswith("#")]
        clean_content = "\n".join(lines)

        # Parse YAML
        edited_structure = yaml.safe_load(clean_content)

        if edited_structure and "project_name" in edited_structure and "packages" in edited_structure:
            return edited_structure

        console.print("[yellow]Invalid structure format. Using original structure.[/yellow]")
        return None

    except subprocess.CalledProcessError:
        console.print("[yellow]Editor exited. Using original structure.[/yellow]")
        return None
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing YAML: {e}. Using original structure.[/red]")
        return None

    finally:
        os.unlink(temp_file_path)


async def generate_packages(project_structure: dict[str, Any], project_path: pathlib.Path, console: Console) -> bool:
    """
    Generate packages using create-ds-app.

    Args:
        project_structure: Project structure dictionary
        project_path: Path where to create the project
        console: Rich console for output

    Returns:
        True if generation succeeded
    """
    console.print("\n[bold cyan]Generating packages with create-ds-app...[/bold cyan]")

    # Build create-ds-app command
    # This assumes create-ds-app CLI is available
    cmd = ["create-ds-app", "create", str(project_path)]

    # Add packages as arguments (handle both 'packages' and 'components' for compatibility)
    packages = project_structure.get("packages", project_structure.get("components", []))
    for package in packages:
        cmd.extend(["--component", f"{package['type']}:{package['name']}"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        console.print("[green]✓ Packages generated successfully![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error generating packages: {e.stderr}[/red]")
        return False
    except FileNotFoundError:
        console.print("[red]Error: create-ds-app command not found.[/red]")
        return False


async def adapt_with_claude(
    project_path: pathlib.Path, user_instructions: str, project_structure: dict[str, Any], console: Console
) -> None:
    """
    Adapt the generated project using Claude in interactive mode.

    Args:
        project_path: Path to the generated project
        user_instructions: Original user instructions
        project_structure: Project structure that was generated
        console: Rich console for output
    """
    console.print("\n[bold cyan]Starting Claude Code interactive session...[/bold cyan]")
    console.print("[dim]Claude will now help you adapt the generated project.[/dim]")

    # Create options for Claude with the project directory as working directory
    options = ClaudeAgentOptions(
        system_prompt=(
            "You are helping the user adapt their newly generated data science project. "
            "The project structure has been created using create-ds-app. "
            "Help them customize and implement their specific requirements. "
            "Be helpful and proactive in suggesting improvements."
        ),
        permission_mode="acceptEdits",
        cwd=str(project_path),
    )

    async with ClaudeSDKClient(options=options) as client:
        # Provide context about the project
        packages = project_structure.get("packages", project_structure.get("components", []))
        context_message = f"""
I've just generated a new data science project with the following structure:

Project: {project_structure["project_name"]}
Packages:
{json.dumps(packages, indent=2)}

Original requirements:
{user_instructions}

The project has been created at: {project_path}

Please help me adapt and customize this project according to my requirements.
You can edit files, add new functionality, and help me implement the specific features I need.
        """

        await client.query(context_message)

        # Process initial response
        console.print("\n[bold]Claude:[/bold]")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        console.print(block.text)

        # Interactive loop
        console.print("\n[dim]You can now interact with Claude. Type 'exit' to finish.[/dim]\n")

        while True:
            try:
                user_input = input("[bold cyan]You:[/bold cyan] ")
                if user_input.lower() in ["exit", "quit", "done"]:
                    break

                await client.query(user_input)

                console.print("\n[bold]Claude:[/bold]")
                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                console.print(block.text)
                console.print()

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Exiting Claude session.[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue


async def run_claude_code_workflow(user_instructions: str, project_path: pathlib.Path, console: Console) -> None:
    """
    Run the complete Claude Code workflow for project generation.

    This is the main entry point that orchestrates:
    1. Generating follow-up questions
    2. Getting user answers (handled by hooks.py)
    3. Generating project structure
    4. Allowing structure editing
    5. Generating packages
    6. Adapting with Claude

    Args:
        user_instructions: Initial project description from user
        project_path: Path where to create the project
        console: Rich console for output
    """
    console.print("[bold cyan]Starting Claude Code project generation workflow...[/bold cyan]\n")

    try:
        # Step 1: Generate follow-up questions
        console.print("[bold]Step 1:[/bold] Generating follow-up questions...")
        questions = await get_follow_up_questions(user_instructions)

        # Note: The actual questionnaire presentation will be handled by hooks.py
        # which will call the next steps with the answers

        return questions

    except Exception as e:
        console.print(f"[red]Error in Claude Code workflow: {e}[/red]")
        raise


async def continue_workflow_with_answers(
    user_instructions: str, questionnaire_answers: dict[str, Any], project_path: pathlib.Path, console: Console
) -> None:
    """
    Continue the workflow after getting questionnaire answers.

    This function is called by hooks.py after presenting the questionnaire.

    Args:
        user_instructions: Initial project description
        questionnaire_answers: User's answers to the questionnaire
        project_path: Path where to create the project
        console: Rich console for output
    """
    try:
        # Step 2: Generate project structure
        console.print("\n[bold]Step 2:[/bold] Generating project structure...")
        project_structure = await generate_project_structure(user_instructions, questionnaire_answers)

        # Step 3: Display and allow editing of structure
        console.print("\n[bold]Step 3:[/bold] Review project structure")
        display_project_tree(project_structure, console)

        # Ask if user wants to edit
        edit_response = input("\n[bold cyan]Would you like to edit the structure? (y/N):[/bold cyan] ")
        if edit_response.lower() == "y":
            edited_structure = edit_project_structure(project_structure, console)
            if edited_structure:
                project_structure = edited_structure
                console.print("[green]✓ Structure updated![/green]")
                display_project_tree(project_structure, console)

        # Step 4: Ask if we should generate packages
        generate_response = input("\n[bold cyan]Generate the project packages? (Y/n):[/bold cyan] ")
        if generate_response.lower() != "n":
            # Step 5: Generate packages
            console.print("\n[bold]Step 4:[/bold] Generating packages...")
            success = await generate_packages(project_structure, project_path, console)

            if success:
                # Step 6: Adapt with Claude in interactive mode
                console.print("\n[bold]Step 5:[/bold] Adapting project with Claude...")
                await adapt_with_claude(project_path, user_instructions, project_structure, console)
            else:
                console.print("[yellow]Package generation failed. Skipping Claude adaptation.[/yellow]")
        else:
            console.print("[yellow]Skipping package generation.[/yellow]")

        console.print("\n[bold green]✓ Claude Code workflow completed![/bold green]")

    except Exception as e:
        console.print(f"[red]Error continuing workflow: {e}[/red]")
        raise
