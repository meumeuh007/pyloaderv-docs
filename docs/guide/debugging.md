# Finding and fixing errors

Your script does nothing, or stops working? This page shows where to look.

## The log file

Everything goes to **`PyloaderV.log`**, in your GTA V folder:

- which scripts were loaded,
- every Python error, with the **full traceback** (file, line, message),
- what your script writes with `print()` and `gta.log()`.

Open it with Notepad (or VS Code) while the game runs; reopen it to see new lines.
It starts empty at each game launch.

A typical error looks like this:

```text
[2026-10-29 18:59:37] [INFO] Loaded script C:\...\Grand Theft Auto V\pyscript\speedometer.py
[2026-10-29 19:02:11] [ERROR] Traceback (most recent call last):
[2026-10-29 19:02:11] [ERROR]   File "C:\...\pyscript\speedometer.py", line 12, in on_tick
[2026-10-29 19:02:11] [ERROR]     speed = car.speed * 3.6
[2026-10-29 19:02:11] [ERROR]             ^^^^^^^^^
[2026-10-29 19:02:11] [ERROR] AttributeError: 'Vehicle' object has no attribute 'speed'
[2026-10-29 19:02:11] [ERROR] on_tick failed for speedometer.py
```

Read it from the bottom: **what** went wrong (`AttributeError...`), then **where** (line 12 of
`speedometer.py`, in `on_tick`).

## Print and log

`print()` works: its output goes to the log. `gta.log()` lets you pick a level:

```python
import gta

print("hello")                         # level info
gta.log("debug", "value is 42")
gta.log("info", "mod started")
gta.log("warn", "model not found, using default")
gta.log("error", "this should not happen")
```

For a quick look without opening the log, show it in game:

```python
from gta import ui
ui.notify(f"speed: {speed:.1f}")
```

`f"{value!r}"` shows the exact value, quotes included: handy to spot `None` or empty strings.

## Fast edit-test loop

1. Turn on `AutoReload=true` in [PyloaderV.ini](configuration.md).
2. Play in **windowed** or **borderless** mode (game settings → Graphics) so you can switch
   to your editor easily.
3. Edit, save, look at the game. Errors? Look at the end of the log.

Or keep `AutoReload` off and press **F9** after each save.

## Catch errors yourself

To keep going after an error and log a clear message:

```python
import traceback
import gta

def on_tick():
    try:
        do_the_thing()
    except Exception:
        gta.log("error", traceback.format_exc())
```

Do not use a bare `except:` (it would also catch PyloaderV's own "stop" signal, see
[](waiting.md#something-to-keep-in-mind-except)).

## Check your code before the game does

- Your editor underlines mistakes in red: a wrong name, a missing argument, a typo in a
  native name. Fix them before testing ([](../getting-started/editor.md)).
- Syntax errors stop the whole script from loading: the log says `Failed to load ...` with
  the line.

## Common mistakes

| What you see | Likely cause |
|---|---|
| The script never runs | The file is not **directly** in `pyscript`, its name starts with `__`, or it is in a `lib` folder. Check the log for `Loaded script ...`. |
| Nothing happens when you press a key | Wrong key code, or F9/your `ReloadKey` (reserved). Log `vk` to see what you get. |
| Spawning in `on_key_down` does nothing or freezes | `on_key_down` cannot wait: use the [flag pattern](waiting.md#the-flag-pattern-keys-that-need-to-wait). |
| Text or a marker flickers or does not show | Drawing natives last one frame: call them every frame with `INTERVAL_MS = 0`. |
| The game freezes for a moment | Something blocks: `time.sleep()`, a long loop without `gta.wait()`, a network call. |
| Two cars after each F9 | Entities stay in the world after a reload: delete them in `on_aborted()`. |
| `ModuleNotFoundError` for your own file in a `.pyv` | Use a relative import: `from . import mymodule`. |
| `ModuleNotFoundError` for a pip package | Install it **for the game**: [](pip-packages.md). |
| `TypeError: ... argument` on a native | Wrong number or type of arguments: check the native in the [reference](../reference/natives/index.md). |

More answers in the [](../faq.md).
