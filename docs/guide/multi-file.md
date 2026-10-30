# Bigger mods and .pyv files

A small mod fits in one `.py` file. When it grows, split it into several files and ship it
as a single **`.pyv`** file.

## What is a .pyv?

A `.pyv` is a **whole mod packed in one file** (it is a zip archive inside). Players copy it
into `pyscript`, exactly like a `.py`. F9 and `AutoReload` work the same way.

Inside, there must be a **`main.py`** at the top: it is the script PyloaderV runs, with your
callbacks (`on_start`, `on_tick`...). Every other file is yours to organise.

```text
BankHeist/                 ← your project folder
├── main.py                ← entry point: on_start, on_tick...
├── crew.py                ← your own module
├── settings.json          ← a data file (optional)
└── missions/              ← a sub-package
    ├── __init__.py
    └── vault.py
```

## Importing your own files: use a dot

In `main.py` (and in your other files), import your own modules with a **relative import**,
starting with a dot:

```python
from . import crew                  # your crew.py
from .missions import vault         # your missions/vault.py
from .crew import hire, fire        # functions from crew.py
```

```{important}
**Always use the dot** for your own modules. Each `.pyv` gets its own private namespace, so
two mods can both have a `crew.py` without mixing them up. Without the dot (`import crew`),
the names are shared with every other mod and can clash.
```

Imports of the game API and the standard library do not change: `from gta import world`,
`import json`...

## Pack it

With the `pyloaderv` command ([install it](../getting-started/first-mod.md#1-set-up-your-computer)):

```text
pyloaderv pack BankHeist
```

This writes `BankHeist.pyv` next to the folder. Choose another name with `-o`:

```text
pyloaderv pack BankHeist -o BankHeist-v2.pyv
```

What goes inside: every file of the folder, **except** `__pycache__`, `.pyc` files, hidden files
and folders (`.git`, `.vscode`...), `venv` folders and `pyrightconfig.json`.

Without the `pyloaderv` command, the PyloaderV zip has the same tool in
`for devs (only)/make_pyv.py`:

```text
python "for devs (only)/make_pyv.py" BankHeist BankHeist.pyv
```

## Install and test it

```text
pyloaderv install BankHeist.pyv --game "C:\path\to\Grand Theft Auto V"
```

Then press **F9** in game. Repeat `pack` + `install` + F9 after each change.

## Hide your source code

```text
pyloaderv pack BankHeist --bytecode
```

The `.pyv` then contains compiled Python (`.pyc`) instead of your source code.

- You need **Python 3.12** to do this (the game runs 3.12, and compiled files only work on
  the version that made them). If you have several Pythons: `py -3.12 -m pyloaderv pack BankHeist --bytecode`.
- It makes your code **harder to read, not impossible**: tools exist to decompile Python.
  Do not put secrets in a mod.
- Keep your source folder! You cannot get it back from the `.pyv`.

## Data files

### Read a file shipped inside the .pyv

Files inside a `.pyv` are not normal files on disk, so `open()` does not work on them. Read
them with `pkgutil`:

```python
import json
import pkgutil

# settings.json sits next to main.py in the project folder
settings = json.loads(pkgutil.get_data(__name__, "settings.json"))
```

This also works when the mod is a plain folder or `.py`, so you can test both ways.

### Save files (settings, progress)

A `.pyv` is read-only. To save things, write a file **next to it** in `pyscript`:

```python
import json
import os

# .pyv: __file__ is "...\pyscript\BankHeist.pyv\main.py"
PYSCRIPT = os.path.dirname(os.path.dirname(__file__))
SAVE_FILE = os.path.join(PYSCRIPT, "BankHeist_save.json")


def save(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load():
    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

For a plain `.py` script, the folder is simply `os.path.dirname(__file__)`.

## Without .pyv: helper folders

You can also keep a mod as files in `pyscript`. Only `.py` files **directly** in `pyscript` are
run as scripts; files in sub-folders are only imported:

```text
pyscript/
├── bankheist.py           ← runs (has the callbacks)
└── bankheist_lib/         ← not run, imported by bankheist.py
    ├── __init__.py
    └── crew.py
```

```python
# bankheist.py
from bankheist_lib import crew
```

Give the folder a unique name: it is shared with every other script. For mods you share,
prefer a `.pyv`.
