import shutil


def center(text: str):
    return text.center(shutil.get_terminal_size().columns)
