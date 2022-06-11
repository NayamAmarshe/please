#!/usr/bin/env python
import datetime
import json
import os
import random
import shutil
from os.path import expanduser

import rich
import typer
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table

# INITIALIZE PACKAGES
app = typer.Typer()
console = Console()


def center(text: str):
    return text.center(shutil.get_terminal_size().columns)


def center_print(text: str, style: str = None):
    return console.print(Align.center(text), style=style)


def center_print_wrap(text: str, style: str):
    return console.print(Align.center(text, style=style, width=shutil.get_terminal_size().columns//2))


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


def all_tasks_done():
    completed_all_tasks = True
    for task in config["tasks"]:
        if task["done"] == False:
            completed_all_tasks = False
    return completed_all_tasks


@ app.command(short_help="Change name without resetting data")
def callme(name: str):
    config["user_name"] = name
    write_config(config)
    center_print("\nThanks for letting me know your name!\n", "black on green")


@ app.command(short_help='Add a Task')
def add(task: str):
    new_task = {
        "name": task,
        "done": False
    }
    config["tasks"].append(new_task)
    write_config(config)
    print("\n")
    center_print(f"Added \"{task}\" to the list",
                 "cyan1 on purple3")
    print_tasks(config["tasks"])


@ app.command(short_help='Deletes a Task')
def delete(index: int):
    index = index - 1
    if index >= len(config["tasks"]):
        center_print_wrap(
            "Are you sure you gave me the correct number to delete?", "bright_red on bright_white")
        print("\n")
        return

    if len(config["tasks"]) > 0:
        deleted_task = config["tasks"][index]
        del config["tasks"][index]
        write_config(config)
        print("\n")
        center_print(f"Deleted '{deleted_task['name']}'", "cyan1 on purple3")
        print_tasks(config["tasks"], True)
    else:
        center_print_wrap(
            "Sorry, I've got no tasks to delete", style="bright_red on bright_white")
        print("\n")


@ app.command(short_help='Mark a task as done')
def done(index: int):
    index = index - 1
    if index >= len(config["tasks"]):
        center_print_wrap(
            "Are you sure you gave me the correct number to mark as done?", "bright_red on bright_white")
        print("\n")
        return

    if len(config["tasks"]) > 0 and not all_tasks_done():
        config["tasks"][index]["done"] = True
        write_config(config)
        center_print("Updated Task List", "black on green")
        print_tasks(config["tasks"])
    else:
        center_print_wrap(
            "Sorry, I've got no tasks to mark as done", style="bright_red on bright_white")
        print("\n")


@app.command(short_help='Mark a task as undone')
def undone(index: int):
    index = index - 1
    if index >= len(config["tasks"]):
        center_print_wrap(
            "Are you sure you gave me the correct number to mark as undone?", "bright_red on bright_white")
        print("\n")
        return

    if len(config["tasks"]) > 0:
        config["tasks"][index]["done"] = False
        write_config(config)
        center_print("Updated Task List", "black on green")
        print_tasks(config["tasks"])
    else:
        center_print_wrap(
            "Sorry, I've got no tasks to mark as undone", style="bright_red on bright_white")
        print("\n")


@app.command(short_help="Show all Tasks")
def showtasks():
    tasks_list = config["tasks"]
    if len(tasks_list) > 0:
        table1 = Table(title="Tasks", title_style="grey39",
                       header_style="#e85d04",  style="#e85d04 bold")
        table1.add_column('Number', style="#e85d04")
        table1.add_column('Task')
        table1.add_column('Status')

        for index, task in enumerate(tasks_list):
            task_name = f"""[#A0FF55]{task["name"]}[/]""" if task["done"] else f"""[#FF5555]{task["name"]}[/]"""
            task_status = "✅" if task["done"] else "❌"
            task_index = "[#A0FF55]" + str(
                index + 1) + "[/]" if task["done"] else "[#FF5555]" + str(index + 1) + "[/]"
            table1.add_row(task_index, task_name, task_status)
        center_print(table1)


def print_tasks(tasks_list, forced_print=False):
    if len(tasks_list) > 0 and not all_tasks_done() or forced_print:
        showtasks()
    else:
        center_print("[#61E294]Looking good, no pending tasks 😁[/]")


def getquotes():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "quotes.json"), 'r') as qf:
        quotes_file = json.load(qf)
    return(quotes_file[random.randrange(0, 500)])


@ app.command(short_help="Reset all data and run setup")
def setup():
    config = {}
    config["user_name"] = typer.prompt(typer.style(
        "Hello! What can I call you?", fg=typer.colors.CYAN))

    codeMarkdown = Markdown("""
        please callme <Your Name Goes Here>
    """)
    center_print("\nThanks for letting me know your name!")
    center_print("If you wanna change your name later, please use:", "red")
    console.print(codeMarkdown)

    # SET DEFAULT VARIABLES IN JSON DATASTORE
    config["initial_setup_done"] = True
    config["tasks"] = []
    write_config(config)


@app.callback(invoke_without_command=True)
def show(ctx: typer.Context):
    dateNow = datetime.datetime.now()
    user_name = config["user_name"]
    dateNow = datetime.datetime.now()

    # PRINT TASKS
    if ctx.invoked_subcommand is None:
        center_print(rich.rule.Rule("[#FFBF00] Hello " + config["user_name"] +
                                    "! It's " + dateNow.strftime("%d %b | %I:%M %p") + "[/]", style="#FFBF00"))
        # IF THERE IS NO INVOKED COMMAND, PRINT THE TASK LIST
        # PRINT QUOTE
        quote = getquotes()
        center_print_wrap("[#63D2FF]\"" + quote["content"] + "\"[/]", "italic")
        center_print_wrap("[#F03A47]- " + quote['author'] + "[/]\n", "italic")
        print_tasks(config["tasks"])


def main():
    # CREATE JSON STORE CONFIG IN ~/.config/please
    global config_path
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
