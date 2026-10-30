# gta (core module)

```python
import gta
```

The `gta` module is built into PyloaderV. It only exists inside the game.
It contains the core functions below, and the friendlier modules:

| Module | For |
|---|---|
| [`gta.player`](player.md) | The player you control. |
| [`gta.world`](world.md) | Spawning, models, all peds/vehicles, raycasts. |
| [`gta.entity`](entity.md) | `Entity`: what peds and vehicles have in common. |
| [`gta.ped`](ped.md) | `Ped`: people. |
| [`gta.vehicle`](vehicle.md) | `Vehicle`: cars, bikes, boats, aircraft. |
| [`gta.ui`](ui.md) | Notifications, subtitles, help text. |
| [`gta.math`](math.md) | Distances and vector maths. |
| [`gta.natives`](natives/index.md) | All 6649 game natives. |

```{py:module} gta
```

## Scripts

```{py:function} wait(ms=0)

Pause the current script for `ms` milliseconds. The game and other scripts keep running.
`wait(0)` waits until the next frame.

Works in `on_start`, `on_tick` and the functions they call. Does nothing in `on_key_down`,
`on_aborted` and at the top of the file. See [](../guide/waiting.md).
```

```{py:function} log(level, message)

Write `message` to `PyloaderV.log`. `level` is `"debug"`, `"info"`, `"warn"` (or `"warning"`)
or `"error"`. See [](../guide/debugging.md).
```

```{py:function} notify(message)

Show a notification at the top left of the screen. Same as [`ui.notify`](ui.md).
Supports the [color codes](../guide/screen.md#colors-and-formatting).
```

```{py:data} __version__
The PyloaderV version, as a string (for example `"0.9.2"`).
```

## World lists

These return **handles** (numbers). The [`gta.world`](world.md) versions return objects instead.

```{py:function} get_all_peds()

Handles of every ped currently loaded in the world (including you). Returns `list[int]`.
```

```{py:function} get_all_vehicles()

Handles of every vehicle currently loaded in the world. Returns `list[int]`.
```

```{py:function} get_all_objects()

Handles of every object (prop) currently loaded in the world. Returns `list[int]`.
```

```{py:function} get_all_pickups()

Handles of every pickup currently in the world. Returns `list[int]`.
```

## Natives

```{py:function} invoke(hash, *args, return_type="int")

Call any native from its 64-bit hash (an `int`, or a string like `"0xD80958FC74E988A6"`).
`args` can be `int`, `float`, `bool`, `str` or `None`.

`return_type` says how to read the result: `"int"`, `"uint"`, `"handle"`, `"hash"`,
`"float"`, `"bool"`, `"str"`, `"vector3"` or `"void"`.

Prefer the named natives in [`gta.natives`](natives/index.md): they are faster and checked by
your editor. See [](../guide/natives.md#calling-a-native-by-its-hash).
```

```{py:class} Vector3(x, y, z)

A position or direction: three floats `x`, `y`, `z`. It is a named tuple, so you can write
`pos.x` or unpack it: `x, y, z = pos`. Natives that return a position return a `Vector3`.
```

## Game info

```{py:function} game_version()

The game build number used by ScriptHookV (`eGameVersion`), as an `int`.
```

## Memory access (advanced)

Reading game memory directly. Only for experienced modders: wrong addresses crash the game.

```{py:function} get_global_ptr(id)

Address (an `int`) of the script global `id`.
```

```{py:function} entity_address(handle)

Address in memory of the entity behind `handle`.
```

```{py:function} read_int(addr)

Read a 32-bit integer at `addr`. Raises `OSError` if the address cannot be read.
```

```{py:function} read_float(addr)

Read a 32-bit float at `addr`. Raises `OSError` if the address cannot be read.
```
