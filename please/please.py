import pyfiglet
import typer
from jsonstore import JsonStore
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.markdown import Markdown


app = typer.Typer()
console = Console()

#

# JSONSTORE CONFIG
store = JsonStore('config.json')

try:
    with store:
        title = pyfiglet.figlet_format(
            f'Hello {store["user_name"]}!', font="slant")
        console.print(f"{title}", style="magenta")
except Exception:
    markdownCode = Markdown("""
        please callme <Your Name Goes Here>
    """)
    console.print(
        "Sorry, I don't know your name yet. Please use: ", style="bold cyan")
    console.print(markdownCode)


@app.command(short_help="Setup Wizard for First Time Run")
def callme(name: str):
    store["user_name"] = name
    typer.echo(f"Thanks for letting me know your name!")


@app.command(short_help='Add a Task')
def add(task: str):
    typer.echo(f"Added => {task} <= to the list")


@app.command(short_help='Deletes a Task')
def delete(task_number: str):
    typer.echo(f"Deleted {task_number}")


if __name__ == "__main__":
    app()
