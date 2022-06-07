#!/usr/bin/env python
import datetime
import json
import os
import random
import shutil
from os.path import expanduser

import art
import imgrender
import pyfiglet
import typer
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table
import rich

from please.utils import center, center_print, center_print_wrap

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
        typer.echo(f"Deleted '{deleted_task['name']}'")
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
    completed_all_tasks = True
    for task in config["tasks"]:
        if task["done"] == False:
            completed_all_tasks = False

    if len(tasks_list) > 0 and not completed_all_tasks:
        table1 = Table(show_header=True, header_style='bold')
        table1.add_column('Number')
        table1.add_column('Task')
        table1.add_column('Status')

        for index, task in enumerate(tasks_list):
            task_name = f"""[#A0FF55]{task["name"]}[/]""" if task["done"] else f"""[#FF5555]{task["name"]}[/]"""
            task_status = "✅" if task["done"] else "❌"
            table1.add_row(str(index), task_name, task_status)
        # PRINTING THE TABLE (COULD BE MADE PRETTIER)
        center_print(table1)
    else:
        center_print("[green]Looking good, no pending tasks 😁[/]")


def getquotes():
    with open("./please/quotes.json", 'r') as qf:
        quotes_file = json.load(qf)
    return(quotes_file[random.randrange(0, len(quotes_file))])


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


# Question: Why was this turned to false again?
@ app.callback(invoke_without_command=True)
def show(ctx: typer.Context):  # THIS ARGUMENT IS NEEDED TO SEE THE DATA DURING EXECUTION
    dateNow = datetime.datetime.now()

    user_name = config["user_name"]
    quote = getquotes()

    # PRINT ART
    # print(imgrender.get_image("please/images/pixil-layer-Background.png"))

    # TODO: POSSIBLY DELETE THIS AND REPLACE WITH BASH INSTEAD
    dateNow = datetime.datetime.now()
    center_print(rich.rule.Rule(
        "[yellow1]" + dateNow.strftime("%d %b | %I:%M %p") + "[/]", style="yellow1"))

    # PRINT QUOTE
    center_print_wrap("[#00F3FF]" + quote["content"] + "[/]", "italic")
    center_print_wrap("[red]- " + quote['author'] + "[/]\n", "italic")

    # PRINT TASKS
    if ctx.invoked_subcommand is None:  # CHECK IF THERE IS AN INVOKED COMMAND OR NOT
        # IF THERE IS NO INVOKED COMMAND, PRINT THE TASK LIST
        showtasks(config["tasks"])


def main():
    # CREATE JSON STORE CONFIG IN ~/.config/please
    config_path = os.path.join(expanduser("~"), ".config", "please")
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    # IF CONFIG ALREADY HAS INITIAL_SETUP_DONE TO TRUE, FIRE THE APP
    try:  # Try reading the config.json file
        with open(os.path.join(config_path, "config.json")) as config_file:
            global config
            config = json.load(config_file)  # Set config variable to json data
    except:  # If it doesn't exist, create a new config.json file
        open(os.path.join(config_path, "config.json"), "w")
        typer.run(setup)
    else:  # if try block raises no exception
        if(config["initial_setup_done"] == True):
            app()
        else:
            typer.run(setup)


main()
