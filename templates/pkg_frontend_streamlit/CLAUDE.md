# Frontend Package Usage

This package provides a **Streamlit** web application with **branding integration** and **component-based architecture**.

## Key Features

- **Streamlit**: Rapid web app development for data science
- **Branding System**: Automatic integration with company branding
- **Component Architecture**: Reusable UI components
- **Configuration Management**: Environment-based settings
- **Docker Ready**: Pre-configured for containerization

## Branding Integration

### Automatic Branding
The app automatically loads branding from `branding/branding.json`:
```python
from .utils.branding import load_branding

branding = load_branding()
# Access: branding["name"], branding["colors"], branding["logo"]
```

### Branding Configuration
Update `branding/branding.json`:
```json
{
    "name": "Your Company Name",
    "colors": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e"
    },
    "logo": "path/to/logo.png"
}
```

## App Development

### Basic App Structure
```python
import streamlit as st
from .config import settings
from .utils.branding import load_branding

st.set_page_config(
    page_title=settings.app_title,
    page_icon="🚀",
    layout="wide"
)

branding = load_branding()
st.title(f"🚀 {branding['name']}")
```

### Component Usage
```python
from .components.sidebar import create_sidebar
from .components.charts import create_chart

# Use sidebar component
with create_sidebar():
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Analytics"])

# Use chart component
if page == "Analytics":
    create_chart(data)
```

### Running the App
```bash
# Development
uv run streamlit run packages/<frontend_package>/src/<package_name>/app.py

# With custom port
uv run streamlit run packages/<frontend_package>/src/<package_name>/app.py --server.port 8501
```

## Development
- Main app in `app.py`
- Components in `components/` directory
- Utilities in `utils/` directory
- Configuration in `config.py`
- Always use the branding system for consistent UI
- Leverage Streamlit's caching for performance