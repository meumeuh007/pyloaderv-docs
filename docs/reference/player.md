# gta.player

```python
from gta import player

me = player.current()
```

```{py:module} gta.player
```

```{py:function} current()

Return the [`Player`](#gta.player.Player) you control.
```

````{py:class} Player(player_id)

The player: who plays, as opposed to the [`Ped`](ped.md) (the body in the world).
You normally get it from `player.current()`.

```{py:attribute} id
:type: int

The player index, used by natives of the `player` namespace (`player_natives.SET_PLAYER_INVINCIBLE(me.id, True)`).
```

```{py:property} ped
:type: gta.ped.Ped

The ped you control right now. It changes when you switch character
(Michael, Franklin, Trevor) or change model, so read it again instead of keeping it forever.
```

```{py:property} wanted_level
:type: int

Number of police stars, `0` to `5`. Set it to change it immediately:
`me.wanted_level = 0`.
```

```{py:property} is_dead
:type: bool

`True` while the player is dead (wasted).
```

```{py:method} set_police_ignore(ignore)

`True`: the police ignore you, even with stars. `False`: back to normal.
```
````

## Example

```python
from gta import player, ui

INTERVAL_MS = 1000


def on_tick():
    me = player.current()
    if me.wanted_level >= 3:
        ui.notify("~r~Too hot! Clearing your stars.")
        me.wanted_level = 0
```

More player natives: [](natives/player.md).
