#!/usr/bin/env python
import datetime
import json
import os
import random
import shutil
from os.path import expanduser

import typer
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule
from rich.table import Table

app = typer.Typer()
console = Console()


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
    """Save the config file.

    Args:
        data (dict): config file
    """
    with open(os.path.join(config_path, "config.json"), "w") as of:
        of.write(json.dumps(data, indent=2))


def all_tasks_done() -> bool:
    """Check if all listed tasks are marked "done".

    Returns:
        bool: True if all are marked "done", else False
    """
    return all(task["done"] for task in config["tasks"])


@app.command(short_help="Change name without resetting data")
def callme(name: str) -> None:
    """Update the name.
    Args:
        name (str): new name
    """
    config["user_name"] = name
    write_config(config)
    center_print("\nThanks for letting me know your name!\n", "black on green")


@app.command(short_help="Add a Task")
def add(task: str) -> None:
    """Add new task to the list.

    Args:
        task (str): task name
    """
    new_task = {"name": task, "done": False}
    config["tasks"].append(new_task)
    write_config(config)
    center_print(f'Added "{task}" to the list', "cyan1 on purple3")
    print_tasks()


@app.command(short_help="Deletes a Task")
def delete(index: int) -> None:
    """Delete an existing task.

    Args:
        index (int): task index (1-based)
    """
    index = index - 1
    if len(config["tasks"]) == 0:
        center_print(
            "Sorry, There are no tasks left to delete", style="bright_red on white", wrap=True
        )
        return

    if not 0 <= index < len(config["tasks"]):
        center_print(
            "Are you sure you gave me the correct number to delete?",
            "bright_red on bright_white",
            wrap=True,
        )
    else:
        deleted_task = config["tasks"][index]
        del config["tasks"][index]
        write_config(config)
        center_print(f"Deleted '{deleted_task['name']}'", "cyan1 on purple3")
        print_tasks(True)


@app.command(short_help="Mark a task as done")
def done(index: int) -> None:
    """Mark a task as "done".

    Args:
        index (int): task index (1-based)
    """
    index = index - 1
    if len(config["tasks"]) == 0:
        center_print(
            "Sorry, There are no tasks to mark as done", style="bright_red on white", wrap=True
        )
        return

    if (config["tasks"][index]["done"] == True):
        center_print("No Updates Made, Task Already Done",
                     style="black on yellow")
        print_tasks()
        return

    if all_tasks_done():
        center_print("All tasks are already completed!", "black on green")
        return
    if not 0 <= index < len(config["tasks"]):
        center_print(
            "Are you sure you gave me the correct number to mark as done?",
            "bright_red on bright_white",
            wrap=True,
        )
    else:
        config["tasks"][index]["done"] = True
        write_config(config)
        center_print("Updated Task List", "black on green")
        print_tasks()


@app.command(short_help="Mark a task as undone")
def undone(index: int) -> None:
    """Unmark a task as "done".

    Args:
        index (int): task index (1-based)
    """
    index = index - 1

    if len(config["tasks"]) == 0:
        center_print(
            "Sorry, There are no tasks to mark as undone", style="bright_red on white", wrap=True
        )
        return

    if (config["tasks"][index]["done"] == False):
        center_print("No Updates Made, Task Still Pending",
                     style="black on yellow")
        print_tasks()
        return

    if not 0 <= index < len(config["tasks"]):
        center_print(
            "Are you sure you gave me the correct number to mark as undone?",
            "bright_red on bright_white",
            wrap=True,
        )
    else:
        config["tasks"][index]["done"] = False
        write_config(config)
        center_print("Updated Task List", "black on green")
        print_tasks()


@app.command(short_help="Change task order")
def move(old_index: int, new_index: int):
    """Change the order of task.

    Args:
        old_index (int): current task index
        new_index (int): new task index
    """
    if (len(config["tasks"]) == 0):
        center_print(
            "Sorry, cannot move tasks as the Task list is empty", style="black on bright_red"
        )
    try:
        config["tasks"][old_index - 1], config["tasks"][new_index - 1] = (
            config["tasks"][new_index - 1],
            config["tasks"][old_index - 1],
        )
        write_config(config)
        if old_index != new_index:
            center_print("Updated Task List", style="black on green")
        else:
            center_print("No Updates Made", style="black on yellow")
        print_tasks(config["tasks"])
    except:
        center_print(
            "Please check the entered index values", style="black on bright_red"
        )


@app.command(short_help="Show all Tasks")
def showtasks() -> None:
    """Display the list of tasks."""
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
    """Logic for displaying the task list."""
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
        center_print("Failed while loading configuration", "bold red on white")
    else:
        if config["initial_setup_done"] is True:
            app()
        else:
            typer.run(setup)


main()
