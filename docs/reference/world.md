# gta.world

```python
from gta import world
```

Spawning, models, lists of entities and raycasts.

```{py:module} gta.world
```

## Spawning

```{py:function} create_vehicle(model, pos, heading=0.0, release_model_after=True)

Create a vehicle and return it as a [`Vehicle`](vehicle.md), or `None` if it failed.

- `model`: a model name (`"adder"`) or its hash.
- `pos`: where, as `(x, y, z)` or a `Vector3`.
- `heading`: the direction it faces, in degrees (`0` = north).
- `release_model_after`: let the game unload the model afterwards (keep `True`).

**Waits** for the model to load: only from `on_start` / `on_tick`.
```

```{py:function} create_ped(model, pos, heading=0.0, ped_type=26, release_model_after=True)

Create a ped and return it as a [`Ped`](ped.md), or `None` if it failed.
`ped_type` is the ped category used by the game (`4` = civilian male, `5` = civilian female,
`6` = cop, `26` = "special", the default, `28` = SWAT, `30` = army). Usually keep the default.

**Waits** for the model to load: only from `on_start` / `on_tick`.
```

## Models

You only need these to create things with natives yourself (`CREATE_OBJECT`...):
`create_vehicle` and `create_ped` already load and release the model.

```{py:function} load_model(model, timeout_ms=2500)

Ask the game to load a model and wait until it is ready. Returns the model hash, or `0` if the
model does not exist or did not load in time. **Waits**: only from `on_start` / `on_tick`.
```

```{py:function} release_model(model)

Tell the game you no longer need the model, after you created your entities.
```

```python
from gta import player, world
from gta.natives import entity, object as object_natives

def on_start():
    me = player.current().ped
    x, y, z = entity.GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(me.handle, 0.0, 3.0, 0.0)
    h = world.load_model("prop_mp_ramp_03")
    if h:
        object_natives.CREATE_OBJECT(h, x, y, z - 1.0, False, False, False)
        world.release_model(h)
```

## Entities around you

```{py:function} get_all_peds()

Every ped loaded in the world, as a list of [`Ped`](ped.md) (you included).
```

```{py:function} get_all_vehicles()

Every vehicle loaded in the world, as a list of [`Vehicle`](vehicle.md).
```

## Raycasts

A raycast traces an invisible line and tells you what it hits first. They do **not** wait, so
you can use them anywhere.

```{py:function} raycast(start, end, flags=HIT_EVERYTHING, ignore_entity=0)

Trace a line from `start` to `end`. Returns a [`RaycastResult`](#gta.world.RaycastResult).
`ignore_entity` is a handle the ray goes through (for example yourself).
```

```{py:function} raycast_from_camera(distance=1000.0, flags=HIT_EVERYTHING, ignore_entity=None)

What is in the middle of the screen, up to `distance` metres. No need to aim.
Ignores the player by default.
```

```{py:function} camera_direction()

The direction the camera looks at, as a unit vector `(x, y, z)`.
```

```{py:class} RaycastResult

The result of a raycast (a named tuple).

- `hit` (`bool`): `True` if the ray hit something.
- `position` (`Vector3`): where it hit.
- `normal` (`Vector3`): the direction the hit surface faces.
- `entity` (`int`): the handle of the entity hit, `0` for the map (ground, buildings).
```

### Flags

Choose what the ray can hit by adding flags with `|`:

| Flag | Hits |
|---|---|
| `HIT_MAP` | ground and buildings |
| `HIT_VEHICLES` | vehicles |
| `HIT_PEDS` | peds |
| `HIT_OBJECTS` | props |
| `HIT_WATER` | water |
| `HIT_VEGETATION` | trees and plants |
| `HIT_EVERYTHING` | all of the above (default) |

```python
from gta import world

hit = world.raycast_from_camera(flags=world.HIT_PEDS | world.HIT_VEHICLES)
if hit.hit:
    print("looking at entity", hit.entity)
```
