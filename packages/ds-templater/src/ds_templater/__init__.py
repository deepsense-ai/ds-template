"""
DS Templater - Template management system for data science projects.
"""

from loguru import logger

from .cli import CLICommands, ParameterHandler, TemplateSelector, create_app
from .config import (
    ConfirmQuestion,
    ListQuestion,
    MultiSelectQuestion,
    Question,
    SimpleTypes,
    TemplateConfig,
    TextQuestion,
    WrappedOption,
)
from .hooks import HookConfig
from .registry import TemplateRegistry
from .renderer import TemplateRenderer

__all__ = [
    "CLICommands",
    "ConfirmQuestion",
    "HookConfig",
    "ListQuestion",
    "MultiSelectQuestion",
    "ParameterHandler",
    "Question",
    "SimpleTypes",
    "TemplateConfig",
    "TemplateRegistry",
    "TemplateRenderer",
    "TemplateSelector",
    "TextQuestion",
    "WrappedOption",
    "create_app",
]

__version__ = "0.1.0"
logger.disable("ds_templater")
