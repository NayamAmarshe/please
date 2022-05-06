#!/usr/bin/env python
import datetime
import os
from os.path import expanduser

import art
import pyfiglet
import typer
from jsonstore import JsonStore
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table

# INITIALIZE PACKAGES
app = typer.Typer()
console = Console()
state = {"verbose": False}

# CREATE JSON STORE CONFIG
home = expanduser('~')
config_path = os.path.join(expanduser("~"), ".config", "please")
print(f"Config Path: {config_path}")
if not os.path.exists(config_path):
    os.makedirs(config_path)
store = JsonStore(os.path.join(config_path, "config.json"))


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


@app.command()
def show(date: bool = True, name: bool = True, tasks_list: bool = True):
    if name == True:
        user_name = store["user_name"]
        typer.secho(art.text2art(f"Morning {user_name}!", "tarty2"),
                    fg=typer.colors.CYAN)

    if date == True:
        dateNow = datetime.datetime.now()
        typer.secho(art.text2art(
            dateNow.strftime("%d %b == %I:%M %p"), "thin3"), fg=typer.colors.MAGENTA)


def main(verbose: bool = False):
    # ASK FOR USERNAME
    store["user_name"] = typer.prompt(typer.style(
        "Hello! What can I call you?", fg=typer.colors.CYAN))

    # PRINT INFO AFTER USER ENTERS THEIR NAME
    codeMarkdown = Markdown("""
        please callme <Your Name Goes Here>
    """)
    typer.echo(typer.style(
        "\nThanks for letting me know your name!\n", fg=typer.colors.GREEN))
    typer.echo(typer.style(
        "\nIf you wanna change your name later, please use: \n", fg=typer.colors.RED))
    console.print(codeMarkdown)

    # SET DEFAULT VARIABLES IN JSON DATASTORE
    store["initial_setup_done"] = True
    store["tasks"] = []


if __name__ == "__main__":
    try:
        with store:
            if(store["initial_setup_done"]):
                app()
    except Exception:
        typer.run(main)
