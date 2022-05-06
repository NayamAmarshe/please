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

# CREATE JSON STORE CONFIG IN ~/.config/please
config_path = os.path.join(expanduser("~"), ".config", "please")
if not os.path.exists(config_path):
    os.makedirs(config_path)
store = JsonStore(os.path.join(config_path, "config.json"))


def get_time_of_day(x):
    if (x > 4) and (x <= 12):
        return 'Morning'
    elif (x > 12) and (x <= 16):
        return 'Afternoon'
    elif (x > 16) and (x <= 20):
        return 'Evening'
    elif (x > 20) and (x <= 24) or (x <= 4):
        return'Night'


@ app.command(short_help="Setup Wizard for First Time Run")
def callme(name: str):
    store["user_name"] = name
    typer.echo(f"Thanks for letting me know your name!")


@ app.command(short_help='Add a Task')
def add(task: str):
    typer.echo(f"Added => {task} <= to the list")


@ app.command(short_help='Deletes a Task')
def delete(task_number: str):
    typer.echo(f"Deleted {task_number}")


@ app.command(short_help="First run setup wizard")
def setup():
    # SETUP WIZARD
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


@ app.callback(invoke_without_command=True)
def show(date: bool = True, name: bool = True, tasks_list: bool = True):
    dateNow = datetime.datetime.now()

    if name == True:
        user_name = store["user_name"]
        time_of_day = get_time_of_day(int(dateNow.strftime("%H")))
        print(dateNow.strftime("%H"))
        typer.secho(art.text2art(f"{time_of_day} {user_name}!", "tarty7"),
                    fg=typer.colors.YELLOW)

    if date == True:
        # TODO: POSSIBLY DELETE THIS AND REPLACE WITH BASH INSTEAD
        dateNow = datetime.datetime.now()
        typer.secho(art.text2art(
            dateNow.strftime("%d %b == %I:%M %p"), "thin3"), fg=typer.colors.MAGENTA)


if __name__ == "__main__":
    try:
        # IF CONFIG ALREADY HAS INITIAL_SETUP_DONE TO TRUE, FIRE THE APP
        with store:
            if(store["initial_setup_done"]):
                app()
    except Exception:
        # IF CONFIG DOESN'T EXIST, CALL THE SETUP WIZARD
        typer.run(setup)
