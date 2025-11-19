# Copyright 2025 Manuel Muth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
