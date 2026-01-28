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

from pathlib import Path
import questionary
from typing import Any


from devc_cli_plugin_system.interactive_creation.interaction_provider import InteractionProvider


class QuestionaryInteractionProvider(InteractionProvider):

    def select_multiple(
        self,
        prompt: str,
        choices: list[dict[str, Any]],
        default: str | None = None,
        **kwargs: dict[str, Any]
    ) -> list[str]:
        try:
            return (
                questionary.checkbox(
                    prompt, choices=choices, default=default, **kwargs
                ).unsafe_ask()
                or []
            )
        except KeyboardInterrupt:
            raise

    def select_single(
        self,
        prompt: str,
        choices: list[dict[str, Any]],
        default: str | None = None,
        **kwargs: dict[str, Any]
    ) -> str:
        try:
            input = questionary.select(
                prompt, choices=choices, default=default, **kwargs
            ).unsafe_ask()
            if input is None and default is not None:
                return default
            if input is None:
                return ""
            return str(input)
        except KeyboardInterrupt:
            raise

    def input_text(self, prompt: str, default: str | None = None, **kwargs: dict[str, Any]) -> str:
        try:
            input = questionary.text(prompt, default=default or "", **kwargs).unsafe_ask()
            if input is None and default is not None:
                return default
            if input is None:
                return ""
            return str(input)
        except KeyboardInterrupt:
            raise

    def input_path(
        self, prompt: str, default: str | Path | None = None, **kwargs: dict[str, Any]
    ) -> Path:
        try:
            val = questionary.path(
                prompt, default=str(default) if default else "", **kwargs
            ).unsafe_ask()
            return Path(val)
        except KeyboardInterrupt:
            raise

    def confirm(self, prompt: str, default: bool = False, **kwargs: dict[str, Any]) -> bool:
        try:
            input = questionary.confirm(prompt, default=default, **kwargs).unsafe_ask()
            if input is None and default is not None:
                return default
            return bool(input)
        except KeyboardInterrupt:
            raise
