# The pyloaderv command

```text
pip install pyloaderv
```

The `pyloaderv` package gives you autocomplete for `import gta` (see [](../getting-started/editor.md))
and the `pyloaderv` command below. If the command is "not recognized", use `py -m pyloaderv`
instead: it is the same.

```text
pyloaderv --help
pyloaderv --version
```

## Choosing the game folder

`install` and `pip` need [your GTA V folder](../getting-started/install.md#step-1-find-your-game-folder).
Give it with `--game`, or once and for all with the `PYLOADERV_GAME` environment variable:

```text
setx PYLOADERV_GAME "C:\Program Files\Rockstar Games\Grand Theft Auto V"
```

(Open a new terminal after `setx`.) You can also give the path to `GTA5.exe` or
`GTA5_Enhanced.exe` itself.

## pyloaderv new

```text
pyloaderv new <folder>
```

Create a mod folder with a starter `main.py` (all callbacks, commented) and a
`pyrightconfig.json` for the editor. The folder name is the mod name. Refuses to overwrite an
existing `main.py`.

## pyloaderv pack

```text
pyloaderv pack <folder> [-o <file.pyv>] [--bytecode]
```

Pack a mod folder (with `main.py` at its top) into one `.pyv` file.

`-o`, `--output`
: The `.pyv` to write. Default: `<folder>.pyv`, next to the folder.

`--bytecode`
: Ship compiled `.pyc` files instead of the source. Needs Python 3.12.
  See [](../guide/multi-file.md#hide-your-source-code).

Left out of the archive: `__pycache__`, `.pyc` and `.pyv` files, hidden files and folders,
`venv` / `.venv`, and `pyrightconfig.json`.

## pyloaderv install

```text
pyloaderv install <file.py or file.pyv>... [--game <GTA V folder>]
```

Copy one or more scripts into `<GTA V>\pyscript\` (replacing files with the same name).
PyloaderV must already be installed in that folder. Press F9 in game afterwards.

## pyloaderv pip

```text
pyloaderv pip <package>... [--game <GTA V folder>]
```

Install pip packages **for the game's Python** (into `shvpy_runtime\Lib\site-packages`).
Takes the same package arguments as `pip install`: `requests`, `numpy==2.1.0`...

It downloads Windows 64-bit wheels for CPython 3.12, whatever Python you run it with.
Packages that only exist as source archives cannot be installed this way.
See [](../guide/pip-packages.md).
