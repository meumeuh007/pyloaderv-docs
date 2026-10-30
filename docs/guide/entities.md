# Peds, vehicles and entities

Everything that physically exists in the world is an **entity**:

- **peds**: people and animals (you are a ped too),
- **vehicles**: cars, bikes, boats, planes, helicopters...
- **objects**: props like barriers, boxes, ramps.

## Handles

The game identifies each entity by a number called a **handle**. Natives take and return
handles:

```python
from gta.natives import player, entity

handle = player.PLAYER_PED_ID()                  # your ped's handle, e.g. 2049
pos = entity.GET_ENTITY_COORDS(handle, True)
```

PyloaderV wraps handles in friendly classes: `Entity`, `Ped`, `Vehicle`. The handle is always
in `.handle`, so you can mix both styles:

```python
from gta import player
from gta.natives import entity

me = player.current().ped                      # a Ped object
print(me.position, me.health)                   # friendly properties
entity.SET_ENTITY_INVINCIBLE(me.handle, True, False)   # any native with .handle
```

To turn a handle you got from a native into an object, pass it to the class:

```python
from gta.ped import Ped
from gta.vehicle import Vehicle
from gta.natives import ped as ped_natives

car = Vehicle(ped_natives.GET_VEHICLE_PED_IS_IN(me.handle, False))
```

## The player

```python
from gta import player

p = player.current()      # the Player you control
me = p.ped                # the Ped you control (changes when you switch character!)

p.wanted_level = 0        # clear the stars
p.set_police_ignore(True)
if p.is_dead:
    ...
```

`Player` and `Ped` are different things: the **player** is "who plays" (wanted level, police...),
the **ped** is the body in the world (position, health, weapons...).

## Positions

Positions are `Vector3` values with `x`, `y`, `z` in metres (`z` is height).

```python
pos = me.position
print(pos.x, pos.y, pos.z)
x, y, z = pos                    # it unpacks like a tuple

me.position = (pos.x, pos.y, pos.z + 50.0)   # teleport 50 m up
me.heading = 90.0                            # face west (0 = north, 90 = west, 180 = south)
```

`gta.math` has helpers: `distance(a, b)`, `distance_2d(a, b)`, `add`, `sub`, `scale`...
See [](../reference/math.md).

A position "in front of" an entity:

```python
from gta.natives import entity

# Offsets are relative to the entity: x = to its right, y = forward, z = up.
front = entity.GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(me.handle, 0.0, 5.0, 0.0)
```

## Spawning

```python
from gta import world

car = world.create_vehicle("zentorno", front, heading=me.heading)
cop = world.create_ped("s_m_y_cop_01", front)
```

Both return the new `Vehicle` / `Ped`, or `None` if the model does not exist or did not load.
They **wait** for the model to load, so call them from `on_tick` or `on_start` only
(see [](waiting.md)).

The first argument is a **model name**. Lists of names:

- vehicles: [GTA V vehicle models](https://docs.fivem.net/docs/game-references/vehicle-models/)
- peds: [GTA V ped models](https://docs.fivem.net/docs/game-references/ped-models/)

## Is it still there?

Entities can disappear: the game removes far-away things, a car can explode, a ped can die.
Always check before using an entity you kept for a while:

```python
if car.exists:          # or simply: if car:
    car.set_engine(True)
```

An `Entity` is "true" only while it exists, so `if car:` works too.

## Cleaning up

When your mod does not need an entity anymore, tell the game. Two ways:

`entity.dismiss()`
: "I don't need it anymore": the game removes it later, when you are not looking.
  The most natural choice.

`entity.delete()`
: Removes it immediately, even in front of the player.

Entities you create are **not** removed when your script stops or reloads. Clean them up in
`on_aborted()`:

```python
spawned = []

def on_tick():
    ...
    car = world.create_vehicle("adder", pos)
    if car:
        spawned.append(car)

def on_aborted():
    for e in spawned:
        if e:
            e.delete()
```

## All peds and vehicles around

```python
from gta import world

for ped in world.get_all_peds():
    if not ped.is_dead and ped != me:
        ...

cars = world.get_all_vehicles()
```

These lists contain everything the game has loaded around you (usually a few hundred entities).
Avoid looping over them every frame if you can: `INTERVAL_MS = 500` is plenty for most uses.

## Going further

The classes only cover the most common things. Everything else is available as a native,
with the entity's `.handle`:

- [](../reference/natives/entity.md): any entity (speed, visibility, collisions, attach...)
- [](../reference/natives/ped.md): peds (armor, clothes, groups, ragdoll...)
- [](../reference/natives/vehicle.md): vehicles (colors, mods, doors, repair...)
- [](../reference/natives/task.md): AI orders (go to, drive, fight, flee, animations...)
