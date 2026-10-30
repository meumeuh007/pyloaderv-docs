# gta.entity

```python
from gta.entity import Entity
```

`Entity` is what peds, vehicles and objects have in common. You use it through
[`Ped`](ped.md) and [`Vehicle`](vehicle.md), which have everything below too.
See [](../guide/entities.md) for a gentle introduction.

```{py:module} gta.entity
```

````{py:class} Entity(handle)

Wrap a handle. `Entity(h)` does not create anything: it is just a friendly view of an
entity that already exists.

An entity is **true** while it exists (`if car:`), and two entities are equal when they have
the same handle.

```{py:attribute} handle
:type: int

The game handle. Pass it to natives: `entity.SET_ENTITY_VISIBLE(e.handle, False, False)`.
```

```{py:property} exists
:type: bool

`True` while the entity is still in the world.
```

```{py:property} position
:type: gta.Vector3

Where it is (`x`, `y`, `z` in metres). Set it to teleport: `e.position = (x, y, z)`.
```

```{py:property} heading
:type: float

The direction it faces, in degrees: `0` north, `90` west, `180` south, `270` east.
```

```{py:property} health
:type: int

Current health. Peds usually have `200` at full health (`100` and below means dead),
vehicles `1000`.
```

```{py:property} is_dead
:type: bool

`True` if the entity is dead or destroyed.
```

```{py:method} dismiss()

Tell the game you no longer need this entity: it will remove it later, out of sight.
```

```{py:method} delete()

Remove the entity now. After this, `handle` is `0`.
```
````

## Example

```python
from gta import world

for ped in world.get_all_peds():
    if ped.is_dead:
        ped.delete()          # clean up bodies
```

More entity natives (speed, velocity, visibility, collisions, attaching...):
[](natives/entity.md).
