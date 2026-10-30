# How scripts work

This page explains what PyloaderV does with your files: which ones it runs, in what order,
and which of your functions it calls.

## Where scripts go

Scripts live in the **`pyscript`** folder of your GTA V folder. PyloaderV runs:

- every **`.py`** file directly inside `pyscript`,
- every **`.pyv`** file directly inside `pyscript` (a whole mod packed in one file,
  see [](multi-file.md)).

It does **not** run:

- files inside sub-folders (they are your helper modules, you `import` them),
- files whose name starts with two underscores, like `__init__.py`,
- anything inside a folder named `lib` or `Lib`.

```text
pyscript/
├── speedometer.py        ← runs
├── BankHeist.pyv         ← runs
├── __notes.py            ← ignored (starts with __)
└── mytools/              ← not run, but importable
    ├── __init__.py
    └── colors.py
```

Each script is its own module: its global variables are private, two scripts can both
have a variable called `count` without any problem.

## The callbacks

A script talks to the game through **callbacks**: functions with special names that
PyloaderV calls at the right moment. They are all optional: write only the ones you need.

| Callback | When it is called | Can it wait? |
|---|---|---|
| `on_start()` | Once, just after the script is loaded. | ✅ Yes |
| `on_tick()` | Again and again, as long as the script runs. | ✅ Yes |
| `on_key_down(vk, down, shift, ctrl, alt)` | When a key is pressed or released. | ❌ No |
| `on_aborted()` | Once, before the script stops (F9 reload, game closing). | ❌ No |

"Can it wait?" means: can you call `gta.wait()` (or a function that waits, like
`world.create_vehicle`) inside it. This is important, see [](waiting.md).

A complete script with every callback:

```python
import gta
from gta import player, ui

INTERVAL_MS = 1000        # on_tick runs every second
__priority__ = 100        # load order (lower loads first)


def on_start():
    ui.notify("script started")


def on_tick():
    if player.current().is_dead:
        gta.log("info", "the player is dead")


def on_key_down(vk, down, shift, ctrl, alt):
    if down and vk == 0x74:      # F5
        ui.notify("F5 pressed")


def on_aborted():
    gta.log("info", "script stopping")
```

## The life of a script

1. **Loading.** PyloaderV runs your file from top to bottom, like Python does with any module.
   Keep this part short: define variables and functions, do not touch the game yet.
2. **`on_start()`** runs once, at the next game frame.
3. **`on_tick()`** runs repeatedly. After each call, PyloaderV waits `INTERVAL_MS`
   milliseconds before calling it again.
4. Meanwhile, **`on_key_down()`** runs whenever you press or release a key.
5. **`on_aborted()`** runs when the script stops: you pressed F9, or the game is closing.

```{important}
All scripts run **one after the other on the game's thread**, not in parallel. While your
code runs, the game waits for it. So your code must always finish quickly or call
`gta.wait()`. **Never use `time.sleep()`**: it freezes the whole game.
```

## Script settings

Two optional variables at the top of your file change how the script runs.

`INTERVAL_MS` (default `0`)
: Milliseconds between two calls of `on_tick`. `0` means **every frame** (needed to draw
  on screen or to react instantly). Use a bigger value like `500` for checks that do not need
  to be instant: your mod then costs almost nothing.

`__priority__` (default `100`)
: Load order. Scripts with a lower number load and run first. Scripts with the same priority
  load in alphabetical order.

## Reloading with F9

Press **F9** in game to reload every script. PyloaderV:

1. calls `on_aborted()` on every script,
2. forgets the loaded modules,
3. loads all scripts again from disk (with your latest changes).

Global variables start over from their initial values. **But what you created in the world
stays there**: cars, peds, blips... Delete them in `on_aborted()` if you do not want
duplicates after each reload:

```python
spawned = []

def on_aborted():
    for e in spawned:
        e.delete()
```

You can change the reload key, or make PyloaderV reload by itself when you save a file
(`AutoReload`), in [](configuration.md).

## When something goes wrong

PyloaderV never lets a Python error crash the game. Errors go to **`PyloaderV.log`** in
your GTA V folder, with the full traceback.

| Problem | What happens |
|---|---|
| The file has a syntax error, or fails while loading | The script is not loaded. The others run normally. |
| `on_start` raises an error | The error is logged, then `on_tick` runs anyway. |
| `on_tick` raises an error | The error is logged and `on_tick` is called again next time. |
| `on_key_down` raises an error | The error is logged, the other scripts still get the key. |
| Your code runs more than 5 seconds without waiting | The game is frozen during that time, then the script is stopped (see `ScriptTimeoutMs` in [](configuration.md)). |

Read [](debugging.md) to find and fix errors quickly.
