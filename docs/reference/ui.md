# gta.ui

```python
from gta import ui
```

The three classic GTA messages. Text can use the
[color codes](../guide/screen.md#colors-and-formatting) (`~r~`, `~g~`, `~n~`...).

```{py:module} gta.ui
```

```{py:function} notify(message)

A notification at the top left, above the minimap.
```

```{py:function} show_subtitle(message, duration_ms=2500)

A subtitle at the bottom of the screen, for `duration_ms` milliseconds.
```

```{py:function} show_help_text(message, beep=False)

The black help box at the top left. It disappears almost at once: call it every frame
(`INTERVAL_MS = 0`) for as long as it should stay. `~INPUT_CONTEXT~` and the other
`~INPUT_...~` codes show the matching key or button.
```

## Example

```python
from gta import ui

INTERVAL_MS = 0


def on_start():
    ui.notify("~g~Mod loaded")
    ui.show_subtitle("Find the ~y~briefcase~s~.", 5000)


def on_tick():
    ui.show_help_text("Press ~INPUT_CONTEXT~ to search")
```

For your own text, boxes, markers and blips, see [](../guide/screen.md).
