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
import inspect

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from collections.abc import Sequence
from collections.abc import Callable
from functools import wraps


class InteractionProvider(ABC):
    @abstractmethod
    def select_multiple(
        self,
        prompt: str,
        choices: Sequence[str | dict[str, Any]],
        default: str | None = None,
        **kwargs: Any
    ) -> list[str]:
        """
        Ask the user to select multiple items. Raises KeyboardInterrupt if cancelled.
        Returns selected choices of value of choices as list[str].
        """

    @abstractmethod
    def select_single(
        self,
        prompt: str,
        choices: Sequence[str | dict[str, Any]],
        default: str | None = None,
        **kwargs: Any
    ) -> str:
        """Ask the user to select a single item. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def input_text(self, prompt: str, default: str | None = None, **kwargs: Any) -> str:
        """Ask the user to input text. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def input_path(self, prompt: str, default: str | Path | None = None, **kwargs: Any) -> Path:
        """Ask the user to input a filesystem path. Raises KeyboardInterrupt if cancelled."""

    @abstractmethod
    def confirm(self, prompt: str, default: bool = False, **kwargs: Any) -> bool:
        """Ask the user to confirm yes/no. Raises KeyboardInterrupt if cancelled."""

    @staticmethod
    def supported_kwargs(*names: str) -> Callable:
        """
        Use this decorator to define supported kwargs for your implementation of the interface.


        Calls function with filtered kwargs defined by passed names
        """
        allowed = set(names)

        def decorator(fn: Callable) -> Callable:
            # get signature of the passed function
            sig = inspect.signature(fn)

            @wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                # get args that are part of the functions signature
                # we need this because we want to allow the following:
                # lets say we have function with signature f(a,b) and supported_kwargs("c")
                # we want to allow the function to be either called with position only:
                # be called with fn(a,b) or fn(a,b,c="banana")
                # or with kwargs as well like:
                # f(a=a, b=b) or fn(a=a,b=b,c="banana"), and so we don't filter in this case a&b
                # we need to bind first and then filter rest and then pass what's allowed
                bound = sig.bind_partial(*args, **kwargs)
                # determine which extra kwargs are passed then
                # filter them with the given names -> allowed
                extra = bound.arguments.get("kwargs", {})
                filtered = {k: v for k, v in extra.items() if k in allowed}
                bound.arguments["kwargs"] = filtered

                return fn(*bound.args, **bound.kwargs)

            return wrapper

        return decorator
