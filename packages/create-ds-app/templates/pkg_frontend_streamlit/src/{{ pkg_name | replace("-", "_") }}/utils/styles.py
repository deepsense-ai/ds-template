"""CSS styles for the chatbot interface."""


def get_chatbot_styles(
    primary_color: str,
    secondary_color: str = "#1A1A1A",
    third_color: str = "#FFFFFF",
    dark_mode: bool = False
) -> str:
    """
    Generate CSS styles for the chatbot interface.

    Args:
        primary_color: Primary brand color for accents
        secondary_color: Secondary brand color (used for dark text/backgrounds)
        third_color: Third brand color (used for light backgrounds)
        dark_mode: Whether to use dark mode theme

    Returns:
        CSS string to be injected into the app
    """
    # Theme colors based on mode
    if dark_mode:
        # Dark mode: use secondary color for backgrounds
        bg_primary = secondary_color
        bg_secondary = "#2d2d2d"
        text_primary = "#e0e0e0"
        text_secondary = "#b0b0b0"
        border_color = "#404040"
        message_user_bg = primary_color
        message_user_text = third_color
        message_assistant_bg = third_color
        message_assistant_text = secondary_color
        message_assistant_border = "#404040"
        sidebar_bg = secondary_color
    else:
        # Light mode: use third color for backgrounds
        bg_primary = third_color
        bg_secondary = "#f8f9fa"
        text_primary = secondary_color
        text_secondary = "#666666"
        border_color = "#e0e0e0"
        message_user_bg = primary_color
        message_user_text = third_color
        message_assistant_bg = secondary_color
        message_assistant_text = third_color
        message_assistant_border = "#e9ecef"
        sidebar_bg = "#fafafa"

    return f"""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Main container */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background-color: {bg_primary};
    }}

    /* Overall background */
    .stApp {{
        background-color: {bg_primary};
    }}

    /* Header styling */
    .header-container {{
        background-color: {bg_primary};
        padding: 1rem 1.5rem;
        border-bottom: 2px solid {primary_color};
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .header-left {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}

    .header-logo {{
        height: 45px;
        width: 45px;
        border-radius: 8px;
    }}

    .header-title {{
        color: {text_primary};
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
    }}

    .header-subtitle {{
        color: {text_secondary};
        font-size: 0.9rem;
        margin: 0;
    }}

    /* Message bubbles */
    .message {{
        margin-bottom: 1.5rem;
        display: flex;
        gap: 1rem;
        animation: fadeIn 0.4s ease-in;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .message-avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
        margin-top: 4px;
    }}

    .user-avatar {{
        background-color: {message_user_bg};
        color: {message_user_text};
    }}

    .assistant-avatar {{
        background-color: {bg_secondary};
        color: {text_primary};
    }}

    .message-content {{
        flex: 1;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        line-height: 1.6;
    }}

    .user-message .message-content {{
        background-color: {message_user_bg};
        color: {message_user_text};
    }}

    .assistant-message .message-content {{
        background-color: {message_assistant_bg};
        color: {message_assistant_text};
        border: 1px solid {message_assistant_border};
    }}

    .message-time {{
        font-size: 0.75rem;
        color: {text_secondary};
        margin-top: 0.5rem;
    }}

    /* Button styling */
    .stButton > button {{
        background-color: {primary_color};
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        opacity: 0.85;
        border: none;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: {text_primary};
    }}

    [data-testid="stSidebar"] h1 {{
        color: {text_primary};
    }}

    [data-testid="stSidebar"] .stButton > button {{
        background-color: {bg_primary};
        color: {text_primary};
        border: 1px solid {border_color};
        text-align: left;
        font-weight: normal;
    }}

    [data-testid="stSidebar"] .stButton > button:hover {{
        background-color: {primary_color};
        color: #ffffff;
        border: 1px solid {primary_color};
    }}

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background-color: {primary_color};
        color: #ffffff;
        border: 1px solid {primary_color};
    }}

    /* Info boxes */
    .welcome-box {{
        background-color: {bg_secondary};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }}

    .welcome-box h2 {{
        color: {text_primary};
        margin-bottom: 1rem;
    }}

    .welcome-box p {{
        color: {text_secondary};
    }}

    /* Chat input */
    .stChatInput {{
        background-color: {bg_primary};
    }}

    .stChatInput > div {{
        background-color: {bg_secondary};
        border: 1px solid {border_color};
    }}

    .stChatInput input {{
        color: {text_primary};
    }}

    /* Divider */
    hr {{
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid {border_color};
    }}

    /* Download button */
    .stDownloadButton > button {{
        background-color: {primary_color};
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }}

    .stDownloadButton > button:hover {{
        opacity: 0.85;
    }}

    /* Checkbox */
    .stCheckbox {{
        color: {text_primary};
    }}

    /* Expander */
    [data-testid="stExpander"] {{
        background-color: {bg_primary};
        border: 1px solid {border_color};
    }}

    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {{
        color: {text_primary};
    }}
    </style>
    """
