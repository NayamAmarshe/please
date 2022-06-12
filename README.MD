<center><h1>Please - New Tab Page for your Terminal</h1>
</center>

<p align="center"><img src="please.gif"></img></center>

<center>
<h1>Installation</h1>
</center>

### Method 1:

1. Make sure you have Python 3 installed on your computer.
2. Open your terminal and enter this command to install please:
   ```bash
    pip install please
   ```
   - If you get an error about **'pip not found'**, just type **pip3** instead of **pip**.

Having trouble with installation or have any ideas? Please create an issue ticket :)

### Method 2:

1. Go to the releases section.
2. Download the latest release WHL file.
3. Open terminal and type:

   ```bash
   pip install --user ~/Downloads/please_cli*
   ```

   - If you get an error about **'pip not found'**, just type **pip3** instead of **pip**
   - Change the path of the file if you downloaded it somewhere else.

<center>
<h1>Local Development</h1>
</center>

1. To get started, first install poetry:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

2. Clone this project
3. `cd` to the project directory and run virtual environment:

```bash
poetry shell

# OR THIS, IF 'poetry shell' doesn't work

. "$(dirname $(poetry run which python))/activate"
```

4. Install all dependencies:

```bash
poetry install
```

- `please` will be available to use as a command in the virtual environment after using `poetry install`.

5. Finally, run the python script with:

```bash
python please/please.py
```

6. To build a WHL package:

```bash
poetry build
```

- The package will be generated in **dist** folder, you can then use pip to install the WHL file.
