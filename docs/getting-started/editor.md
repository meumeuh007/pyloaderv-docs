# Set up your editor

With the `pyloaderv` package, your editor knows the whole game API: it **autocompletes**
`gta.` and shows the parameters of every function, including all 6649 natives.

```text
pip install pyloaderv
```

Nothing else to configure: no stubs folder to copy, no settings to change.

## VS Code (recommended)

1. Install the **Python** extension by Microsoft (it includes Pylance).
2. Open your mod folder with **File → Open Folder...**.
3. Press **Ctrl+Shift+P**, run **Python: Select Interpreter**, and choose the Python
   where you ran `pip install pyloaderv`.
4. Type `from gta import ` in a file: the list of modules appears.

```{tip}
Hover a function to see its parameters. **Ctrl+click** a name to open its stub.
```

## PyCharm

1. Open your mod folder as a project.
2. **Settings → Project → Python Interpreter**: pick the Python where you installed `pyloaderv`
   (or install `pyloaderv` from that screen with the **+** button).

## Other editors

Any editor that understands Python type stubs (PEP 561) works: Neovim or Sublime Text with
Pyright, Zed, mypy on the command line...

## "Stub file found but no source" warning

Pylance may say *Import "gta" could not be resolved from source*. That is expected: the real
`gta` module only exists **inside the game**, your PC only has its description.

`pyloaderv new` creates a `pyrightconfig.json` that hides this warning. For an existing folder,
create that file yourself:

```json
{
    "pythonVersion": "3.12",
    "reportMissingModuleSource": "none"
}
```

## Can I run my script on my PC?

No. `import gta` only works inside GTA V. On your PC you **write** and **pack** the code,
the game **runs** it. Use the [log file](../guide/debugging.md) to see what your script does.

## Which Python version?

The game runs **Python 3.12**. On your PC any Python 3.9 or newer works for autocomplete,
but **use 3.12** so you do not use features the game does not have, and so that
`pyloaderv pack --bytecode` works.
