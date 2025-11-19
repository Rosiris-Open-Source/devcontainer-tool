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
