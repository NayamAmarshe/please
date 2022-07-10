#!/usr/bin/env python
# from asyncore import write
import datetime
import json
import os
import random
import shutil
from os.path import expanduser
from re import L

import typer
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule
from rich.table import Table

app = typer.Typer()
console = Console()

COLOR_INFO = "cyan1 on purple3"
COLOR_SUCCESS = "black on green"
COLOR_WARNING = "bright_red on bright_white"
COLOR_ERROR = "black on bright_red"


def center_print(text, style: str = None, wrap: bool = False) -> None:
    """Print text with center alignment.

    Args:
        text (Union[str, Rule, Table]): object to center align
        style (str, optional): styling of the object. Defaults to None.
    """
    if wrap:
        width = shutil.get_terminal_size().columns // 2
    else:
        width = shutil.get_terminal_size().columns

    console.print(Align.center(text, style=style, width=width))


def write_config(data: dict) -> None:
    with open(os.path.join(config_path, "config.json"), "w") as of:
        of.write(json.dumps(data, indent=2))


def all_tasks_done() -> bool:
    return all(task["done"] for task in config["tasks"])


@app.command(short_help="Change name without resetting data")
def callme(name: str) -> None:
    config["user_name"] = name
    write_config(config)
    center_print("\nThanks for letting me know your name!\n", "black on green")


@app.command(short_help="Add a Task")
def add(task: str) -> None:
    new_task = {"name": task, "done": False}
    config["tasks"].append(new_task)
    write_config(config)
    center_print(f'Added "{task}" to the list', COLOR_SUCCESS)
    print_tasks()


@app.command(short_help="Deletes a Task")
def delete(index: int) -> None:
    index = index - 1
    if len(config["tasks"]) == 0:
        center_print(
            "Sorry, There are no tasks left to delete", COLOR_INFO, wrap=True
        )
        return

    if not 0 <= index < len(config["tasks"]):
        center_print(
            "Are you sure you gave me the correct number to delete?",
            COLOR_WARNING,
            wrap=True,
        )
    else:
        deleted_task = config["tasks"][index]
        del config["tasks"][index]
        write_config(config)
        center_print(f"Deleted '{deleted_task['name']}'", COLOR_SUCCESS)
        print_tasks(True)


@app.command(short_help="Mark a task as done")
def do(index: int) -> None:
    index = index - 1

    if not 0 <= index < len(config["tasks"]):
        center_print(
            "Are you sure you gave me the correct number to mark as done?",
            COLOR_WARNING,
            wrap=True,
        )
        return

    if len(config["tasks"]) == 0:
        center_print(
            "Sorry, There are no tasks to mark as done", COLOR_ERROR, wrap=True
        )
        return

    if (config["tasks"][index]["done"] == True):
        center_print("No Updates Made, Task Already Done",
                     COLOR_INFO)
        print_tasks()
        return

    if all_tasks_done():
        center_print("All tasks are already completed!", COLOR_SUCCESS)
        return

    config["tasks"][index]["done"] = True
    write_config(config)
    center_print("Updated Task List", COLOR_SUCCESS)
    print_tasks()


@app.command(short_help="Mark a task as undone")
def undo(index: int) -> None:
    index = index - 1

    if not 0 <= index < len(config["tasks"]):
        center_print(
            "Are you sure you gave me the correct number to mark as undone?",
            COLOR_WARNING,
            wrap=True,
        )
        return

    if len(config["tasks"]) == 0:
        center_print(
            "Sorry, There are no tasks to mark as undone", COLOR_INFO, wrap=True
        )
        return

    if (config["tasks"][index]["done"] == False):
        center_print("No Updates Made, Task Still Pending",
                     COLOR_INFO)
        print_tasks()
        return

    config["tasks"][index]["done"] = False
    write_config(config)
    center_print("Updated Task List", COLOR_SUCCESS)
    print_tasks()


@app.command(short_help="Change task order")
def move(old_index: int, new_index: int):
    if (len(config["tasks"]) == 0):
        center_print(
            "Sorry, cannot move tasks as the Task list is empty", COLOR_ERROR
        )
        return

    try:
        config["tasks"][old_index - 1], config["tasks"][new_index - 1] = (
            config["tasks"][new_index - 1],
            config["tasks"][old_index - 1],
        )
        write_config(config)
        if old_index != new_index:
            center_print("Updated Task List", COLOR_SUCCESS)
        else:
            center_print("No Updates Made", COLOR_INFO)
        print_tasks(config["tasks"])
    except:
        center_print(
            "Please check the entered index values", COLOR_WARNING
        )


@app.command(short_help="Clean up tasks marked as done from the task list")
def clean() -> None:
    res = []
    for i in config['tasks']:
        if i['done'] != True:
            res.append(i)
    if config['tasks'] != res:
        config['tasks'] = res
        write_config(config)
        center_print("Updated Task List", COLOR_SUCCESS)
        print_tasks(config["tasks"])
        return
    center_print("No Updates Made", COLOR_INFO)
    print_tasks(config["tasks"])


@app.command(short_help="Toggle Time Format from 24 Hours to 12 Hours")
def changetimeformat() -> None:
    try:
        if config["time_format_24h"] is (None or False):
            config["time_format_24h"] = True
            center_print("Changed Time Format from 12h to 24h",
                         COLOR_SUCCESS)
        else:
            config["time_format_24h"] = False
            center_print("Changed Time Format from 24h to 12h",
                         COLOR_SUCCESS)
    except:
        config["time_format_24h"] = True
        center_print("Changed Time Format from 24h to 12h",
                     COLOR_SUCCESS)
    write_config(config)


@app.command(short_help="Show all Tasks")
def showtasks() -> None:
    task_num = config["tasks"]
    table1 = Table(
        title="Tasks",
        title_style="grey39",
        header_style="#e85d04",
        style="#e85d04 bold",
    )
    table1.add_column("Number", style="#e85d04")
    table1.add_column("Task")
    table1.add_column("Status")

    if len(task_num) == 0:
        center_print(table1)
    else:
        for index, task in enumerate(task_num):
            if task["done"]:
                task_name = f"[#A0FF55] {task['name']}[/]"
                task_status = "✅"
                task_index = f"[#A0FF55] {str(index + 1)} [/]"
            else:
                task_name = f"[#FF5555] {task['name']}[/]"
                task_status = "❌"
                task_index = f"[#FF5555] {str(index + 1)} [/]"

            table1.add_row(task_index, task_name, task_status)
        center_print(table1)

    if(all_tasks_done()):
        center_print("[#61E294]Looking good, no pending tasks 😁[/]")


def print_tasks(forced_print: bool = False) -> None:
    if not all_tasks_done() or forced_print:
        showtasks()
    else:
        center_print("[#61E294]Looking good, no pending tasks 😁[/]")


def getquotes() -> dict:
    """Select a random quote.

    Returns:
        dict: quote with its metadata
    """
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(os.path.join(__location__, "quotes.json"), "r") as qf:
        quotes_file = json.load(qf)
    return quotes_file[random.randrange(0, 500)]


@app.command(short_help="Reset all data and run setup")
def setup() -> None:
    """Initialize the config file."""
    config = {}
    config["user_name"] = typer.prompt(
        typer.style("Hello! What can I call you?", fg=typer.colors.CYAN)
    )

    code_markdown = Markdown(
        """
        please callme <Your Name Goes Here>
    """
    )
    center_print("\nThanks for letting me know your name!")
    center_print("If you wanna change your name later, please use:", "red")
    console.print(code_markdown)

    config["initial_setup_done"] = True
    config["tasks"] = []
    write_config(config)


@app.callback(invoke_without_command=True)
def show(ctx: typer.Context) -> None:
    """Greets the user."""
    date_now = datetime.datetime.now()
    user_name = config["user_name"]

    if ctx.invoked_subcommand is None:
        date_text = ""
        try:
            if config["time_format_24h"] is (None or False):
                date_text = f"[#FFBF00] Hello {user_name}! It's {date_now.strftime('%d %b | %I:%M %p')}[/]"
            else:
                date_text = f"[#FFBF00] Hello {user_name}! It's {date_now.strftime('%d %b | %H:%M')}[/]"
        except:
            config["time_format_24h"] = True
            write_config(config)
            date_text = f"[#FFBF00] Hello {user_name}! It's {date_now.strftime('%d %b | %I:%M %p')}[/]"

        try:
            if config["disable_line"]:
                center_print(date_text)
            else:
                pass
        except:
            center_print(Rule(date_text, style="#FFBF00"))
        quote = getquotes()
        center_print(f'[#63D2FF]"{quote["content"]}[/]', wrap=True)
        center_print(f'[#F03A47][i]- {quote["author"]}[/i][/]\n', wrap=True)
        print_tasks()


def main() -> None:
    """Load config file and program initialization."""
    global config_path
    config_path = os.path.join(expanduser("~"), ".config", "please")
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    try:
        with open(os.path.join(config_path, "config.json")) as config_file:
            global config
            config = json.load(config_file)
    except FileNotFoundError:
        open(os.path.join(config_path, "config.json"), "w")
        typer.run(setup)
    except json.JSONDecodeError:
        console.print_exception(show_locals=True)
        center_print("Failed while loading configuration", COLOR_ERROR)
    else:
        if config["initial_setup_done"] is True:
            app()
        else:
            typer.run(setup)


main()
