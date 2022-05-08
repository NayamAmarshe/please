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

# CREATE JSON STORE CONFIG IN ~/.config/please
config_path = os.path.join(expanduser("~"), ".config", "please")
if not os.path.exists(config_path):
    os.makedirs(config_path)
else: # ONLY ATTEMPT TO READ THE FILE OF THE FOLDER EXISTS
    try:
        cfile = open(os.path.join(config_path, "config.json"))
        config = json.load(cfile)
        cfile.close()
    except Exception:
        print("The setup was not complete, please do the setup again") # IF THE SETUP HAD COMPLETED FULLY, THE FILE SHOULD HAVE BEEN CREATED

# FUNCTION TO WRITE THE JSON DATA TO THE CONFIG FILE
def write_config(data):
    with open(os.path.join(config_path, "config.json"), 'w') as of:
        of.write(json.dumps(data, indent = 2)) #THIS IS DONE SO THE THE JSON DATA IS NOT WRITTEN AS A SINGLE LINE

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
    typer.echo(f"Thanks for letting me know your name!")

# TASK FUNCTIONS START

# FUNCTION TO ADD A TASK
@ app.command(short_help='Add a Task')
def add(task: str):
    config["tasks"][task] = "❌"
    write_config(config)
    typer.echo(f"Added => {task} <= to the list")
    show_table(config["tasks"]) # PRINTING THE TABLE TO SHOW UPDATED ENTRIES

# FUNCTION TO DELETE A TASK
@ app.command(short_help='Deletes a Task')
def delete(task: str):
    config["tasks"].pop(task)
    write_config(config)
    typer.echo(f"Deleted {task}")
    show_table(config["tasks"]) # PRINTING THE TABLE TO SHOW UPDATED ENTRIES

# FUNCTION TO MARK A TASK AS DONE
@ app.command(short_help='Marks a task as done')
def done(task: str):
    config["tasks"][task] = "✔️"
    write_config(config)
    typer.echo(f"Updated Task List")
    show_table(config["tasks"]) # PRINTING THE TABLE TO SHOW UPDATED ENTRIES

# FUNCTION TO PRINT THE TABLE
def show_table(task_dict):
    table1 = Table(show_header=True, header_style='bold')
    table1.add_column('Task')
    table1.add_column('Status')
    for task, status in task_dict.items():
        table1.add_row(task, status)
    # PRINTING THE TABLE (COULD BE MADE PRETTIER)
    console.print(table1)
# TASK FUNCTIONS END

@ app.command(short_help="First run setup wizard")
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
    config["tasks"] = {}
    write_config(config)

@ app.callback(invoke_without_command=True)
def show(date: bool = True, name: bool = True, tasks_list: bool = True):
    dateNow = datetime.datetime.now()

    if name == True:
        user_name = config["user_name"]
        time_of_day = get_time_of_day(int(dateNow.strftime("%H")))
        typer.secho(art.text2art(f"{time_of_day} {user_name}!", "tarty7"),
                    fg=typer.colors.YELLOW)

    if date == True:
        # TODO: POSSIBLY DELETE THIS AND REPLACE WITH BASH INSTEAD
        dateNow = datetime.datetime.now()
        typer.secho(art.text2art(
            dateNow.strftime("%d %b == %I:%M %p"), "thin3"), fg=typer.colors.MAGENTA)
    if tasks_list == True:
        show_table(config["tasks"])


if __name__ == "__main__":
    try:
        # IF CONFIG ALREADY HAS INITIAL_SETUP_DONE TO TRUE, FIRE THE APP
        with open(os.path.join(config_path, "config.json")) as cfile:
            store = json.load(cfile)
            if(store["initial_setup_done"] == True):
                app()
    except Exception:
        # IF CONFIG DOESN'T EXIST, CALL THE SETUP WIZARD
        typer.run(setup)
