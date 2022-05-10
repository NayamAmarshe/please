#!/usr/bin/env python
import datetime
import os
from os.path import expanduser

import art
import pyfiglet
import typer
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table

# INITIALIZE PACKAGES
app = typer.Typer()
console = Console()
state = {"verbose": False}

def write_config(data):
    with open(os.path.join(config_path, "config.json"), 'w') as of:
        of.write(json.dumps(data, indent=2))  # 'indent' formats json properly


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
    config["user_name"] = name
    write_config(config)
    typer.echo(f"Thanks for letting me know your name!")


@ app.command(short_help='Add a Task')
def add(task: str):
    new_task = {
        "name": task,
        "done": False
    }
    config["tasks"].append(new_task)
    write_config(config)
    typer.echo(f"Added \"{task}\" to the list")
    showtasks(config["tasks"])


@ app.command(short_help='Deletes a Task')
def delete(index: int):
    if index >= len(config["tasks"]):
        print("Are you sure you gave me the correct number?")
        return

    if len(config["tasks"]) > 0:
        deleted_task = config["tasks"][index]
        del config["tasks"][index]
        write_config(config)
        typer.echo(f"Deleted {deleted_task}")
        showtasks(config["tasks"])
    else:
        print("Sorry, I've got no tasks to delete")


@ app.command(short_help='Mark a task as done')
def done(index: int):
    if index >= len(config["tasks"]):
        print("Are you sure you gave me the correct number?")
        return

    if len(config["tasks"]) > 0:
        config["tasks"][index]["done"] = True
        write_config(config)
        typer.echo(f"Updated Task List")
        showtasks(config["tasks"])
    else:
        print("Sorry, I've got no tasks to mark as done")


@ app.command(short_help='Mark a task as undone')
def undone(index: int):
    if index >= len(config["tasks"]):
        print("Are you sure you gave me the correct number?")
        return

    if len(config["tasks"]) > 0:
        config["tasks"][index]["done"] = False
        write_config(config)
        typer.echo(f"Updated Task List")
        showtasks(config["tasks"])
    else:
        print("Sorry, I've got no tasks to mark as undone")


def showtasks(tasks_list):
    if len(tasks_list) > 0:
        table1 = Table(show_header=True, header_style='bold')
        table1.add_column('Number')
        table1.add_column('Task')
        table1.add_column('Status')
        for index, task in enumerate(tasks_list):
            task_name = task["name"]
            task_status = "✅" if task["done"] else "❌"
            table1.add_row(str(index), task_name, task_status)
        # PRINTING THE TABLE (COULD BE MADE PRETTIER)
        console.print(table1)
    else:
        print("Looking good, no tasks 😁")


@ app.command(short_help="Reset data and run Setup Wizard")
def setup():
    # SETUP WIZARD
    # ASK FOR USERNAME
    config = {}
    config["user_name"] = typer.prompt(typer.style(
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
    config["initial_setup_done"] = True
    config["tasks"] = []
    write_config(config)


@ app.callback(invoke_without_command=True) # Question: Why was this turned to false again?
def show(ctx: typer.Context): #THIS ARGUMENT IS NEEDED TO SEE THE DATA DURING EXECUTION
    dateNow = datetime.datetime.now()

    user_name = config["user_name"]
    time_of_day = get_time_of_day(int(dateNow.strftime("%H")))
    typer.secho(art.text2art(
        f"{time_of_day} {user_name}!", "tarty7"), fg=typer.colors.YELLOW)

    # TODO: POSSIBLY DELETE THIS AND REPLACE WITH BASH INSTEAD
    dateNow = datetime.datetime.now()
    typer.secho(art.text2art(
        dateNow.strftime("%d %b == %I:%M %p"), "thin3"), fg=typer.colors.MAGENTA)
    
    if ctx.invoked_subcommand is None: # CHECK IF THERE IS AN INVOKED COMMAND OR NOT
        showtasks(config["tasks"]) # IF THERE IS NO INVOKED COMMAND, PRINT THE TASK LIST


if __name__ == "__main__":
    # CREATE JSON STORE CONFIG IN ~/.config/please

    config_path = os.path.join(expanduser("~"), ".config", "please")
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    # IF CONFIG ALREADY HAS INITIAL_SETUP_DONE TO TRUE, FIRE THE APP
    try:  # Try reading the config.json file
        with open(os.path.join(config_path, "config.json")) as config_file:
            config = json.load(config_file)  # Set config variable to json data
    except:  # If it doesn't exist, create a new config.json file
        open(os.path.join(config_path, "config.json"), "w")
        typer.run(setup)
    else:   #if try block raises no exception
        if(config["initial_setup_done"] == True):
            app()
        else:
            typer.run(setup)