import base64
import json
from pathlib import Path


def image_to_base64(path: Path) -> str:
    """Convert image to base64 encoded string"""
    with open(path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{encoded}"


def load_branding_config() -> dict[str, str | None]:
    """Load branding configuration from branding.json file."""
    branding_path = Path(__file__).parent.parent.parent.parent.parent.parent / "branding" / "branding.json"
    if branding_path.exists():
        with open(branding_path) as f:
            branding_config = json.load(f)
        if branding_config.get("logo_path", None):
            logo_path = branding_config["logo_path"]
            if Path(logo_path).exists():
                return branding_config
            else:
                logo_path = Path(branding_path).parent / branding_config["logo_path"]
                branding_config["logo_path"] = logo_path if Path(logo_path).exists() else None
                return branding_config

    # Return default branding if file not found
    return {
        "name": "My App",
        "primary_color": "#1B54FF",
        "second_color": "#1A1A1A",
        "third_color": "#FFFFFF",
        "logo_path": None
    }
