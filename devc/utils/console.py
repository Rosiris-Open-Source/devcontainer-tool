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
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_error(title: str, message: str) -> None:
    color = "red"
    console.print(
        Panel.fit(
            Text(message),
            title=f"[{color}]{title}[/{color}]",
            border_style=color,
        )
    )


def print_warning(title: str, message: str) -> None:
    color = "yellow"
    console.print(
        Panel.fit(
            Text(message),
            title=f"[{color}]{title}[/{color}]",
            border_style=color,
        )
    )
