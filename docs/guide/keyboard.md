# Keyboard and controller

## `on_key_down`

```python
def on_key_down(vk, down, shift, ctrl, alt):
    ...
```

PyloaderV calls it for **every key event**, pressed or released:

| Argument | Meaning |
|---|---|
| `vk` | The key code (a number, see the table below). |
| `down` | `True` when the key is pressed, `False` when it is released. |
| `shift`, `ctrl`, `alt` | `True` if that modifier key is held at the same time. |

```python
from gta import ui

def on_key_down(vk, down, shift, ctrl, alt):
    if not down:
        return                       # ignore key releases
    if vk == 0x74 and ctrl:          # Ctrl+F5 (test the combination first)
        ui.notify("Ctrl+F5")
    elif vk == 0x74:                 # F5 alone
        ui.notify("F5")
```

```{warning}
`on_key_down` cannot wait: no `gta.wait()`, no `world.create_vehicle()` in it.
Set a flag and do the work in `on_tick`, see [](waiting.md#the-flag-pattern-keys-that-need-to-wait).
```

### Holding a key

When you hold a key, Windows repeats it: `on_key_down` gets `down=True` many times.
To react only once per press, remember which keys are held:

```python
held = set()

def on_key_down(vk, down, shift, ctrl, alt):
    if not down:
        held.discard(vk)
        return
    if vk in held:
        return                       # still the same press
    held.add(vk)
    ...                              # first press only
```

### Is a key held right now?

To check a key at any moment (for example in `on_tick`), use Windows directly:

```python
import ctypes

def is_key_held(vk):
    return ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000 != 0
```

### The reload key

PyloaderV keeps **F9** (or your `ReloadKey`) for itself: scripts never receive it.
Avoid keys other popular mods use too, like F4 (often a trainer) or F10/F11.

## Key codes

Key codes are Windows "virtual-key codes". The most useful ones:

| Key | Code | Key | Code |
|---|---|---|---|
| F1 ... F12 | `0x70` ... `0x7B` | A ... Z | `0x41` ... `0x5A` |
| 0 ... 9 (top row) | `0x30` ... `0x39` | Numpad 0 ... 9 | `0x60` ... `0x69` |
| Enter | `0x0D` | Space | `0x20` |
| Backspace | `0x08` | Tab | `0x09` |
| Escape | `0x1B` | Shift / Ctrl / Alt | `0x10` / `0x11` / `0x12` |
| Left / Up / Right / Down arrow | `0x25` / `0x26` / `0x27` / `0x28` | Page Up / Page Down | `0x21` / `0x22` |
| Insert / Delete | `0x2D` / `0x2E` | Home / End | `0x24` / `0x23` |
| Numpad + / - / * / / | `0x6B` / `0x6D` / `0x6A` / `0x6F` | Numpad . | `0x6E` |

F5 is `0x74`, F6 `0x75`, F7 `0x76`, F8 `0x77`. For letters and digits you can write
`ord("K")` (= `0x4B`) instead of the number. The full list is on
[Microsoft's page](https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes).

## Game controls (works with a controller)

Keys only work on the keyboard. To react to **game actions** (jump, aim, horn...) on both
keyboard and controller, ask the game with the `pad` natives in `on_tick`:

```python
from gta.natives import pad
from gta import ui

INTERVAL_MS = 0
INPUT_VEH_HORN = 86


def on_tick():
    if pad.IS_CONTROL_JUST_PRESSED(0, INPUT_VEH_HORN):
        ui.notify("Beep beep!")
```

- `IS_CONTROL_PRESSED(0, control)`: held right now.
- `IS_CONTROL_JUST_PRESSED(0, control)`: pressed during this frame (once per press).
- `DISABLE_CONTROL_ACTION(0, control, True)`: block a control for this frame
  (call it every frame).

`INTERVAL_MS` must be `0`, or you will miss presses. The list of control numbers is on the
[FiveM controls page](https://docs.fivem.net/docs/game-references/controls/) (the numbers are the same in story mode).
