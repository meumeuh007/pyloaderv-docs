# Waiting and timing

Games run frame by frame. Your script gets a short turn every frame, then must give control
back to the game. This page shows how to wait without freezing the game.

## `gta.wait(ms)`

`gta.wait(ms)` pauses **your script only** for `ms` milliseconds. The game, and the other
scripts, keep running meanwhile.

```python
import gta
from gta import ui

def on_start():
    ui.notify("3...")
    gta.wait(1000)
    ui.notify("2...")
    gta.wait(1000)
    ui.notify("1...")
    gta.wait(1000)
    ui.notify("~g~GO!")
```

`gta.wait(0)` (or `gta.wait()`) waits for the **next frame**. Use it inside loops that must
run once per frame.

## Where you can wait

| Callback | `gta.wait()` |
|---|---|
| `on_start` | ✅ works |
| `on_tick` | ✅ works |
| functions called from `on_start` / `on_tick` | ✅ works |
| `on_key_down` | ❌ does nothing |
| `on_aborted` | ❌ does nothing |
| top of the file (while loading) | ❌ does nothing |

Some helpers wait **internally** because the game needs time to load a model.
They follow the same rule, so only use them from `on_start` or `on_tick`:

- `world.load_model()`
- `world.create_ped()`
- `world.create_vehicle()`

## The flag pattern: keys that need to wait

You will want a key that spawns something. Spawning waits, and `on_key_down` cannot wait.
The solution: **the key sets a flag, `on_tick` does the job.**

```python
from gta import player, world

INTERVAL_MS = 0
want_bodyguard = False


def on_key_down(vk, down, shift, ctrl, alt):
    global want_bodyguard
    if down and vk == 0x77:          # F8
        want_bodyguard = True


def on_tick():
    global want_bodyguard
    if want_bodyguard:
        want_bodyguard = False
        me = player.current().ped
        world.create_ped("s_m_y_marine_01", me.position)
```

Every example in this documentation that reacts to a key uses this pattern.

## Long loops

A loop inside `on_tick` is fine **as long as it waits** at each turn:

```python
import gta
from gta import ui

def on_start():
    for i in range(10, 0, -1):
        ui.show_subtitle(f"Bomb in {i}...", 900)
        gta.wait(1000)
```

A loop that never waits freezes the game. If it runs more than 5 seconds, PyloaderV stops
the script (setting `ScriptTimeoutMs` in [](configuration.md)).

## Do not use `time.sleep()`

`time.sleep()` pauses the **whole game**, not only your script. Always use `gta.wait()`.
The same goes for anything that blocks: `input()`, a slow network request, reading a huge file...

## Doing something every N seconds

The simplest way is `INTERVAL_MS`:

```python
INTERVAL_MS = 5000      # every 5 seconds

def on_tick():
    ...
```

To have several timers in one script, compare times yourself with the game timer
(milliseconds since the game started, it stops when the game is paused):

```python
from gta.natives import misc

INTERVAL_MS = 0
next_heal = 0


def on_tick():
    global next_heal
    now = misc.GET_GAME_TIMER()
    if now >= next_heal:
        next_heal = now + 10_000          # again in 10 seconds
        ...                               # heal the player
```

`time.monotonic()` works too, but it keeps counting while the game is paused.

## Something to keep in mind: `except:`

When you press F9 while a script is waiting, PyloaderV stops it by raising `SystemExit`
inside `gta.wait()`. `except Exception:` lets it through, which is what you want.
A bare `except:` would catch it and keep your script alive, so avoid it:

```python
try:
    risky()
    gta.wait(100)
except Exception as e:       # good
    gta.log("error", f"oops: {e}")
```
