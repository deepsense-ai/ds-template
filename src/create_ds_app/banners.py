import random

# ANSI color codes
GREEN = "\033[92m"
BLUE = "\033[38;2;0;114;206m"  # DeepSense blue RGB(0, 114, 206)
RESET = "\033[0m"

PEPE_1 = """⠀⣠⠔⠋⠉⠀⠀⣀⣀⣉⣙⣄⠀⠀⢀⣉⣙⣦⠀⠀⠀⠀⠀⠀⠀⠀
⠞⠁⠀⢀⠴⠋⠁⠀⠀⠀⠀⠀⠙⢯⠀⠀⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀
⠀⠀⠠⠃⠀⠀⠀⠀⣐⣀⣉⣉⣉⣐⣣⡠⠥⠤⠬⢭⣝⣲⠀⠀⠀⠀
⠀⠀⠀⢀⡤⠒⠋⢁⠠⠀⠐⣂⣉⣉⣉⣢⣤⠤⢶⣶⣶⡾⠳⣄⠀⠀
⠀⠀⠔⠉⠀⣐⡩⠔⠲⣿⣯⣽⣿⡿⠟⣉⣽⣛⢛⣉⣉⣠⣴⠇⠀⠀
⠀⢠⠠⡯⢒⣒⠒⠒⣒⣒⣒⣒⣉⠭⠕⡞⠁⠉⠻⣍⢉⣼⡁⠀⠀⠀
⠀⠈⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠁⠀⣩⠒⠲⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠐⠊⠀⠀⠀⠀⣀⣀⠤⠒⠊⠁⢀⣠⠼⡁
⠀⠀⠀⠀⠀⠀⣀⠤⠤⠐⠒⠒⠀⠉⠉⠁⣀⣀⠠⠤⠖⠚⠉⠀⣠⠇
⠀⠀⠀⠀⠀⢸⡁⠀⠠⠒⠒⠒⠉⠉⠉⠀⠀⣀⣀⡠⠤⠔⢒⠟⠁⠀"""

PEPE_2 = """  ⢛⢛⣛⣛⣛⣛⣛⣛⣛⣛⡛⢋⣉⣭⣭⣥⣬⣤⣤⣀
 ⣴⣵⣿⣟⡉⣥⣶⣶⠶⠶⠬⣉⡂⠹⣟⡫⠽⠟⢒⣒⠒⠆
.⣼⣿⣿⣿⣿⣿⣶⣭⣃⡈⠄⠄⠘⠃⡰⢶⣶⣿⠏⠄⠄⠙⡛
⢰⣿⣿⣿⣿⣿⣿⣿⣯⣉⣉⣩⣭⣶⣿⡿⠶⠶⠶⠶⠶⠾⣋⠄
⢾⣿⣿⣿⣿⣿⣿⣿⢩⣶⣒⠒⠶⢖⣒⣚⡛⠭⠭⠭⠍⠉⠁
⠘⢿⣿⣿⣿⣿⣿⣿⣧⣬⣭⣭⣭⣤⡤⠤⠶⠟⣋⣀⣀⡀⢀⣤⣾⠟⠋⠈⢳⠄
⣴⣦⡒⠬⠭⣭⣭⣭⣙⣛⠋⠭⡍⠁⠈⠙⠛⠛⠛⠛⢻⠛⠉⢻⠁⠄⠄⠄⢸⡀
⣿⣿⣿⣿⣷⣦⣤⠤⢬⢍⣼⣦⡾⠛⠄⠄⠄⠄⠄⠄⠈⡇⠄⢸⠄⠄⠄⢦⣄⣇
⣿⣿⡿⣋⣭⣭⣶⣿⣶⣿⣿⣿⠟⠛⠃⠄⠄⠄⠄⠄⢠⠃⠄⡜⠄⠄⠄⠔⣿⣿"""

PEPE_3 = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠶⠒⠒⠲⢤⣀⢀⣀⡤⠤⠦⢤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⢀⣠⣤⠤⢤⣄⣈⢿⠁⠀⠀⠀⠀⠙⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⠏⠀⠘⠋⠀⠀⢀⣀⣤⣬⣿⣿⡛⠉⣉⣭⣽⣿⣶⣤⣀⠀
⠀⠀⠀⠀⣠⡴⠋⠀⠀⢀⡠⣶⣾⠿⠒⠋⣉⣉⣛⣻⣶⠞⣚⣻⣯⣍⣓⣾⣇
⠀⠀⠀⡾⠁⠀⠀⠀⠀⠻⠿⣭⣤⠖⢺⣿⣻⠻⣄⢠⡟⠉⠁⣼⢭⡛⣷⢀⣹
⠀⢠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠙⠺⠿⣾⣿⣿⣿⣿⠿⢋⠉⠛⠛⠛⠛⣻⠟⠁
⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠶⠚⠉⠀⠀⠈⠙⠶⡒⠛⠻⣅⠀⠀
⢾⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣆⠀
⠸⡆⠀⠀⠀⠀⠀⠀⢠⡞⠩⢭⣬⣭⣉⣙⡓⠒⠶⠶⠶⠶⠒⠒⠛⠉⣉⣽⠀
⠀⠹⣄⠀⠀⠀⠀⠀⣆⡳⠶⠒⠒⠒⠶⠭⢭⣭⣉⣙⣛⣛⣛⡋⢉⣉⡿⠀⠀
⠀⠀⠈⠿⣶⣤⣀⣀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣉⡭⠟⠉⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠙⠛⠻⠽⢿⣿⣖⣒⣒⣒⣒⣺⡿⠟⠉⠉⠀⠀"""

PEPE_4 = """⠀⠀⠀⠀⠀⠀⣤⠖⠒⠒⠢⣤⡀⠀⠀⣀⣤⠤⠤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡰⠋⠀⠀⠀⠀⠀⠀⠉⢖⠋⠁⠀⠀⠀⠀⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡞⠁⠀⣉⣥⣬⣭⣍⡒⠦⣜⡤⠐⠂⣤⠤⣄⡀⠹⡄⠀⠀⠀⠀⠀⠀⠀
⠀⢠⡏⢀⡠⠊⠀⢀⣶⣶⢦⡍⠑⢬⡧⠞⠉⠉⣉⣍⡙⠳⣿⡄⠀⠀⠀⠀⠀⠀
⠠⡾⠻⣏⠀⠀⠀⠈⢿⣿⣿⠟⠀⠀⢱⡀⠀⠀⣿⣿⣽⡆⠈⢿⠀⠀⠀⠀⠀⠀
⠀⠃⠀⠈⠲⢄⣀⠀⠀⠀⠀⠀⠀⠀⣸⠇⠀⠀⠈⠉⠉⠀⢀⣾⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠒⠒⠒⠒⠒⠚⠑⠤⣀⣀⣀⣀⡠⠖⠻⡎⠀⠀⠀⠀⠀⠀
⡀⠀⠀⠀⠀⠀⢀⣠⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄⠀⠀⠀⠀⠀
⣷⠀⠀⠀⠀⠀⠘⣇⠀⠀⠉⠛⠲⠶⠤⣄⣤⣤⣤⣀⣠⠤⠴⠞⣻⡆⠀⠀⠀⠀
⠙⢧⡀⠀⠀⠀⠀⠈⠓⠤⣄⣉⣱⡒⠂⠀⠀⠀⠀⠀⠀⠀⢀⣾⢏⣶⠤⠀⠀⠀
⠀⠈⣳⣄⠀⢀⣀⣀⣀⣀⣠⠟⠁⠳⠞⠛⡟⠛⠛⠓⣚⣿⣿⣯⠏⠈⠣⠟⢳⠀
⠀⠀⠵⠚⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⢼⣥⣤⠶⠛⠉⡇⠀⠀⠀⠀⠀⠀⢾⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣹⡇⠀⠀⢰⡇⠀⠀⠀⠀⠀⢀⠀⣹
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣟⣉⣁⣀⣀⠀⢺⡄⠀⠀⠀⢀⡴⠋⠀⠀"""

PEPES = [PEPE_1, PEPE_2, PEPE_3, PEPE_4]


def get_random_pepe() -> str:
    """Select a random Pepe from the collection."""
    return random.choice(PEPES)


def colorize_pepe(pepe: str) -> str:
    """Apply green color to Pepe ASCII art."""
    return f"{GREEN}{pepe}{RESET}"


def join_multiline_texts(left: str, right: str, spacing: int = 2) -> str:
    """
    Join two multi-line texts side by side.

    Args:
        left: Left text block
        right: Right text block
        spacing: Number of spaces between the two blocks

    Returns:
        Combined text with both blocks side by side
    """
    left_lines = left.split("\n")
    right_lines = right.split("\n")

    # Get max width of left block (accounting for ANSI codes)
    def visible_length(line: str) -> int:
        """Calculate visible length without ANSI escape codes."""
        import re

        return len(re.sub(r"\033\[[0-9;]+m", "", line))

    left_width = max(visible_length(line) for line in left_lines) if left_lines else 0

    # Pad to same height
    max_height = max(len(left_lines), len(right_lines))
    left_lines += [""] * (max_height - len(left_lines))
    right_lines += [""] * (max_height - len(right_lines))

    # Join line by line
    result = []
    for left_line, right_line in zip(left_lines, right_lines, strict=False):
        # Calculate padding needed (account for invisible ANSI codes)
        padding = left_width - visible_length(left_line) + spacing
        result.append(f"{left_line}{' ' * padding}{right_line}")

    return "\n".join(result)


def create_divider(width: int) -> str:
    """Create a horizontal divider in DeepSense blue."""
    return f"{BLUE}{'═' * width}{RESET}"


def wrap_with_dividers(content: str, width: int = 80) -> str:
    """
    Wrap content with top and bottom dividers.

    Args:
        content: The content to wrap
        width: Width of the dividers

    Returns:
        Content wrapped with blue dividers
    """
    divider = create_divider(width)
    return f"{divider}\n{content}\n{divider}"


def create_banner(project_info: str = "create-ds-app") -> str:
    """
    Create a banner with a random Pepe and project info side by side.

    Args:
        project_info: Multi-line text with project information

    Returns:
        Complete banner with Pepe, project info, and dividers
    """
    pepe = get_random_pepe()
    colored_pepe = colorize_pepe(pepe)
    combined = join_multiline_texts(colored_pepe, project_info)
    return wrap_with_dividers(combined)
