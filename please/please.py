import pyfiglet
import typer
from rich.console import Console
from rich.style import Style
from rich.table import Table

app = typer.Typer()
console = Console()

user_name = ""
title = pyfiglet.figlet_format(f'Hello {user_name}!', font='slant')
console.print(f"{title}", style=Style(blink=True))


@app.command(short_help="Setup Wizard for First Time Run")
def name(name: str):
    user_name = name
    typer.echo(f"Thanks for letting me know your name!")


@app.command(short_help='Add a Task')
def add(task: str):
    typer.echo(f"Added => {task} <= to the list")


@app.command(short_help='Deletes a Task')
def delete(task_number: str):
    typer.echo(f"Deleted {task_number}")


if __name__ == "__main__":
    app()
