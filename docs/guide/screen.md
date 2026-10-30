# Text, HUD and map

How to show things to the player: messages, text on screen, markers and map blips.

## Messages

`gta.ui` has the three classic GTA messages:

```python
from gta import ui

ui.notify("~g~Saved!")                         # top left, above the map
ui.show_subtitle("Get in the car.", 3000)      # bottom of the screen, 3 seconds
ui.show_help_text("Press ~INPUT_CONTEXT~ to open the trunk")   # black box, top left
```

| Function | Where | How long |
|---|---|---|
| `ui.notify(text)` | Top left, in the feed above the minimap. | A few seconds. |
| `ui.show_subtitle(text, ms)` | Bottom center, like mission dialogue. | `ms` milliseconds (default 2500). |
| `ui.show_help_text(text, beep=False)` | Top left, black box. | About one frame: call it **every frame** to keep it visible. |

### Colors and formatting

Put these codes inside your text:

| Code | Effect | Code | Effect |
|---|---|---|---|
| `~r~` | red | `~g~` | green |
| `~b~` | blue | `~y~` | yellow |
| `~o~` | orange | `~p~` | purple |
| `~c~` | grey | `~m~` | dark grey |
| `~u~` | black | `~w~` | white |
| `~s~` | back to the default color | `~h~` | **bold** |
| `~n~` | new line | | |

```python
ui.notify("~r~Wanted! ~w~Lose the cops.~n~~y~Reward: ~g~$500")
```

In help text and subtitles, `~INPUT_...~` shows the matching button for the player's keyboard
or controller: `~INPUT_CONTEXT~` (E), `~INPUT_JUMP~`, `~INPUT_ATTACK~`...

## Text on screen

To draw your own text (a speedometer, a counter...), call these natives **every frame**
(`INTERVAL_MS = 0`):

```python
from gta.natives import hud

INTERVAL_MS = 0


def draw_text(text, x, y, scale=0.5, r=255, g=255, b=255, font=4, center=False):
    hud.SET_TEXT_FONT(font)
    hud.SET_TEXT_SCALE(scale, scale)
    hud.SET_TEXT_COLOUR(r, g, b, 255)
    hud.SET_TEXT_OUTLINE()
    hud.SET_TEXT_CENTRE(center)
    hud.BEGIN_TEXT_COMMAND_DISPLAY_TEXT("STRING")
    hud.ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(text)
    hud.END_TEXT_COMMAND_DISPLAY_TEXT(x, y, 0)


def on_tick():
    draw_text("Hello!", 0.5, 0.05, center=True)
```

- `x` and `y` go from `0.0` to `1.0`: `(0, 0)` is the top left corner, `(1, 1)` the bottom right.
  This works on every screen resolution.
- `font`: `0` normal, `1` handwritten, `2` and `4` condensed, `7` "Pricedown" (the GTA logo font).
- One call shows at most 99 characters: split longer text.

### Boxes

```python
from gta.natives import graphics

# Center at (0.5, 0.1), 30% wide, 6% high, black at 60% opacity.
graphics.DRAW_RECT(0.5, 0.1, 0.3, 0.06, 0, 0, 0, 150, False)
```

Draw the box first, then the text, so the text is on top.

## Markers in the world

Markers are the 3D shapes from missions (cylinders, arrows, rings). Draw them every frame:

```python
from gta import player
from gta.natives import graphics

INTERVAL_MS = 0
SPOT = (-75.0, -818.0, 326.0)      # top of the Maze Bank tower


def on_tick():
    x, y, z = SPOT
    graphics.DRAW_MARKER(
        1, x, y, z - 1.0,          # type 1 = cylinder, on the ground
        0.0, 0.0, 0.0,             # direction
        0.0, 0.0, 0.0,             # rotation
        2.0, 2.0, 1.0,             # size
        255, 200, 0, 150,          # color (r, g, b, alpha)
        False, False, 2, False,
        None, None,                # no texture: must be None, "" crashes the native
        False,
    )
```

Your editor may underline the two `None`: ignore it, `None` is what the game expects here.

Marker types: [FiveM marker list](https://docs.fivem.net/docs/game-references/markers/).

## Blips on the map

Blips are the icons on the minimap and pause map.

```python
from gta.natives import hud

blip = hud.ADD_BLIP_FOR_COORD(-75.0, -818.0, 326.0)
hud.SET_BLIP_SPRITE(blip, 1)          # icon (1 = circle)
hud.SET_BLIP_COLOUR(blip, 5)          # color (5 = yellow)
hud.SET_BLIP_ROUTE(blip, True)        # GPS route to it

hud.BEGIN_TEXT_COMMAND_SET_BLIP_NAME("STRING")
hud.ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME("Maze Bank roof")
hud.END_TEXT_COMMAND_SET_BLIP_NAME(blip)
```

- `ADD_BLIP_FOR_ENTITY(handle)` puts a blip on a ped or vehicle; it follows it.
- Remove a blip with `blip = hud.REMOVE_BLIP(blip)` (it returns `0`).
- Remove your blips in `on_aborted()`, or you get a new one after each F9.
- Icons and colors: [FiveM blip list](https://docs.fivem.net/docs/game-references/blips/).

## Hide the HUD or the radar

These last one frame, so call them in `on_tick` with `INTERVAL_MS = 0`:

```python
from gta.natives import hud

def on_tick():
    hud.HIDE_HUD_AND_RADAR_THIS_FRAME()
```

To toggle them permanently: `hud.DISPLAY_RADAR(False)` and `hud.DISPLAY_HUD(False)`.

## Sounds

```python
from gta.natives import audio

audio.PLAY_SOUND_FRONTEND(-1, "SELECT", "HUD_FRONTEND_DEFAULT_SOUNDSET", True)
```

A few useful ones: `"SELECT"`, `"BACK"`, `"NAV_UP_DOWN"`, `"ERROR"` from
`"HUD_FRONTEND_DEFAULT_SOUNDSET"`, and `"CHECKPOINT_PERFECT"` from `"HUD_MINI_GAME_SOUNDSET"`.
