# WIP - To be released soon

# Please - A New Tab Page for your Terminal

# Setup

To get started, first install poetry:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Clone this project
cd to the project directory and run virtual environment:

```bash
poetry shell

# OR THIS, IF 'poetry shell' doesn't work

. "$(dirname $(poetry run which python))/activate"
```

Install all dependencies:

```bash
poetry install
```

Finally, run the python script with:

```bash
python please/please.py
```
