import json
import streamlit as st

from pathlib import Path
from typing import Optional

def load_branding_config() -> dict[str, Optional[str]]:
    """Load branding configuration from branding.json file."""
    branding_path = Path(__file__).parent.parent.parent.parent.parent.parent / "branding" / "branding.json"
    if branding_path.exists():
        with open(branding_path, 'r') as f:
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
        "primaryColor": "#1B54FF",
        "secondColor": "#1A1A1A",
        "thirdColor": "#FFFFFF",
        "logo_path": None
    }

