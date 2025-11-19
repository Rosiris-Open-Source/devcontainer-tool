"""Helpers ro allow ${VAR} substitutions in strings."""

from string import Template
from typing import Any


def substitute_placeholders(obj: Any, env: dict) -> Any:
    """Recursively replace ${VAR} placeholders in strings within nested structures."""
    if isinstance(obj, str):
        return Template(obj).safe_substitute(env)
    elif isinstance(obj, list):
        return [substitute_placeholders(item, env) for item in obj]
    elif isinstance(obj, dict):
        return {k: substitute_placeholders(v, env) for k, v in obj.items()}
    elif hasattr(obj, "__dataclass_fields__"):
        # Handle dataclasses
        for field_name, field_value in obj.__dict__.items():
            setattr(obj, field_name, substitute_placeholders(field_value, env))
        return obj
    return obj
