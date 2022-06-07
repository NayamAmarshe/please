import shutil
from rich.console import Console
from rich.align import Align

console = Console()


def center(text: str):
    return text.center(shutil.get_terminal_size().columns)


def center_print(text: str, style: str = None):
    return console.print(Align.center(text), style=style)


def center_print_wrap(text: str, style: str):
    return console.print(Align.center(text, style=style, width=shutil.get_terminal_size().columns//2))
