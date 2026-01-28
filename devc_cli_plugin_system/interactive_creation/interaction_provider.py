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

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class InteractionProvider(ABC):
    @abstractmethod
    def select_multiple(
        self,
        prompt: str,
        choices: list[dict[str, Any]],
        default: str | None = None,
        **kwargs: dict[str, Any]
    ) -> list[str]:
        """Ask the user to select multiple items. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def select_single(
        self,
        prompt: str,
        choices: list[dict[str, Any]],
        default: str | None = None,
        **kwargs: dict[str, Any]
    ) -> str:
        """Ask the user to select a single item. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def input_text(self, prompt: str, default: str | None = None, **kwargs: dict[str, Any]) -> str:
        """Ask the user to input text. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def input_path(
        self, prompt: str, default: str | Path | None = None, **kwargs: dict[str, Any]
    ) -> Path:
        """Ask the user to input a filesystem path. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def confirm(self, prompt: str, default: bool = False, **kwargs: dict[str, Any]) -> bool:
        """Ask the user to confirm yes/no. Raises KeyboardInterrupt if cancelled."""
