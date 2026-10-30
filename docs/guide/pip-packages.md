# Using pip packages

The game runs a real CPython 3.12, so packages from [PyPI](https://pypi.org) work too:
`requests`, `numpy`, `pillow`, `pyyaml`...

The whole standard library is already there: `json`, `random`, `math`, `datetime`,
`sqlite3`, `urllib`, `asyncio`, `ctypes`... You only need pip for extra packages.

## Install a package for the game

The game's Python is separate from the one on your PC: install packages **into the game**:

```text
pyloaderv pip requests --game "C:\path\to\Grand Theft Auto V"
```

Several at once:

```text
pyloaderv pip numpy pyyaml --game "C:\path\to\Grand Theft Auto V"
```

Packages go to `shvpy_runtime\Lib\site-packages` in your GTA V folder, where the game finds
them. Press F9 (or restart the game), then `import requests` in your script.

### Without the pyloaderv command

The same thing with plain pip (Python 3.12 on your PC):

```text
py -3.12 -m pip install --target "C:\path\to\Grand Theft Auto V\shvpy_runtime\Lib\site-packages" requests
```

## What can and cannot work

- Packages written in pure Python always work.
- Packages with compiled parts (`numpy`, `pillow`...) work when they publish a **Windows
  64-bit wheel for Python 3.12**. Most popular packages do. `pyloaderv pip` only downloads
  those, so it fails cleanly instead of installing something broken.
- GUI toolkits (`tkinter`, `PyQt`, `pygame` windows) do not belong inside a game: they would
  open windows or block the game.
- Anything slow (network requests, big computations) **freezes the game while it runs**.
  See the next section.

## Slow work: use a thread

A web request can take a second, which would freeze the game for a second. Run it in a
background thread, and only touch the game from your callbacks:

```python
import threading
import requests
from gta import ui

INTERVAL_MS = 200
result = None


def fetch():
    global result
    r = requests.get("https://api.github.com/zen", timeout=10)
    result = r.text                    # no game functions in the thread!


def on_start():
    threading.Thread(target=fetch, daemon=True).start()


def on_tick():
    global result
    if result is not None:
        ui.notify(result)              # back in a callback: talking to the game is safe
        result = None
```

```{warning}
**Never call `gta` functions or natives from a thread.** The game only accepts them from its
own script thread, i.e. from your callbacks. Threads may do Python work only (network, files,
maths) and hand the result over through a variable.
```

## Sharing a mod that needs packages

Players also have to install the packages. Tell them in your mod's description, with the
exact command, for example:

```text
pyloaderv pip requests --game "<your GTA V folder>"
```

If your mod only needs a small pure-Python package, you can instead copy it inside your
`.pyv` and import it with a dot (see [](multi-file.md)).
