# Using natives

**Natives** are the functions of the game engine. Rockstar's own missions use them to do
everything: spawn cars, change the weather, play sounds, give weapons... PyloaderV gives you
**all 6649** of them.

The helpers in `gta.player`, `gta.world`, `gta.ui`... are a small, friendly layer on top of
natives. When a helper does not exist for what you want, use the native directly.

## Calling a native

Natives are grouped by **namespace** (`player`, `vehicle`, `misc`...). Import the namespace,
then call the native by its name:

```python
from gta.natives import misc, clock

misc.SET_WEATHER_TYPE_NOW("THUNDER")
clock.SET_CLOCK_TIME(22, 0, 0)          # 10 PM
```

Native names are in CAPITALS, exactly as in the game files. Your editor autocompletes them
and shows their parameters.

## Finding the right native

1. **Search this site**: type a word (`WEATHER`, `HORN`, `RAGDOLL`...) in the search box.
2. **Browse a namespace** in the [natives reference](../reference/natives/index.md):
   vehicles are in `vehicle`, on-screen stuff in `hud` and `graphics`, AI in `task`...
3. **Use autocomplete**: type `vehicle.SET_VEHICLE_` and look at the list.

Each native in the reference shows its Python signature, its original C signature and, when
the community knows it, a description.

## Parameter types

| In the reference | What to pass in Python |
|---|---|
| `int`, `Hash` | an `int` |
| `float` | a `float` (`1.0`; an `int` like `1` works too) |
| `bool` / `BOOL` | `True` or `False` |
| `str` / `const char*` | a `str` |
| `Ped`, `Vehicle`, `Entity`, `Player`, `Blip`... | a handle (an `int`), e.g. `me.handle` |
| a position | three floats `x, y, z` (natives take them as three parameters) |
| `Any` | type unknown: usually an `int` (`0` if you do not know) |

Parameters named `p0`, `p1`... are ones nobody has figured out yet. Pass `0`, `False` or
`0.0` (or whatever the description says).

### Model and weapon names: hashes

Many natives want a **hash**: a number that stands for a name. Turn a name into a hash with
`GET_HASH_KEY`:

```python
from gta import player
from gta.natives import misc, weapon

me = player.current().ped
rifle = misc.GET_HASH_KEY("WEAPON_CARBINERIFLE")
weapon.GIVE_WEAPON_TO_PED(me.handle, rifle, 250, False, True)
```

Weapon names: [GTA V weapon models](https://docs.fivem.net/docs/game-references/weapon-models/).
The helpers in `gta.world` accept names directly: `world.create_vehicle("adder", ...)`.

## Natives that return several values

Some natives write their results into **pointers** (in C: `BOOL*`, `int*`, `float*`,
`Vector3*`, `Entity*`...). In Python, those values are simply **returned**, after the normal
result:

```python
from gta.natives import misc

# C: BOOL GET_GROUND_Z_FOR_3D_COORD(float x, float y, float z, float* groundZ, BOOL ignoreWater, BOOL p5)
found, ground_z = misc.GET_GROUND_Z_FOR_3D_COORD(x, y, 1000.0, 0.0, False, False)
if found:
    ...
```

The reference always shows what you get back, for example `-> tuple[bool, float]`.

- In the call, put any value for a pointer parameter (it is its starting value, usually `0`,
  `0.0`, `False` or the current handle).
- When pointer parameters are **at the end**, you can leave them out:

```python
from gta.natives import shapetest

status, hit, end, normal, entity = shapetest.GET_SHAPE_TEST_RESULT(handle)
```

- Natives that "delete and set to 0" (like `DELETE_ENTITY`) return the new handle value.
- Parameters of type `Any*` stay raw memory addresses: they are for advanced use.

## Calling a native by its hash

Every native has a unique **hash** (shown in the reference). `gta.invoke` calls any native
from its hash, which helps with natives that are not in the list yet:

```python
import gta

ped = gta.invoke(0xD80958FC74E988A6, return_type="handle")     # PLAYER_PED_ID
pos = gta.invoke(0x3FEF770D40960D5A, ped, True, return_type="vector3")
```

`return_type` tells PyloaderV how to read the result: `"int"` (default), `"uint"`,
`"handle"`, `"hash"`, `"float"`, `"bool"`, `"str"`, `"vector3"` or `"void"`.
The named natives (`gta.natives.*`) are faster and easier: use them whenever you can.

## Natives that only work every frame

Some natives only last **one frame**: drawing text and shapes, `DISABLE_CONTROL_ACTION`,
`SET_SUPER_JUMP_THIS_FRAME`... Call them in `on_tick` with `INTERVAL_MS = 0`. Their names often
end with `_THIS_FRAME`, or their description says "must be called every frame".

## Natives to avoid

- `NETWORK_*` and most `NETSHOPPING`, `SOCIALCLUB`, `MONEY` natives are for GTA Online.
  They do nothing useful in story mode, and PyloaderV is not for GTA Online.
- Natives with only `p0`, `p1`... parameters and no description can do anything,
  including crash the game. Test them carefully.
