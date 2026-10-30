# gta.ped

```python
from gta.ped import Ped
```

A **ped** is any person (or animal) in the game, you included. Get peds from
`player.current().ped`, `world.create_ped(...)`, `world.get_all_peds()`, or wrap a handle
with `Ped(handle)`.

```{py:module} gta.ped
```

````{py:class} Ped(handle)

Has everything [`Entity`](entity.md) has (`position`, `heading`, `health`, `exists`,
`delete()`...), plus:

```{py:method} give_weapon(weapon_hash, ammo=999, hidden=False, equip_now=True)

Give a weapon. Get the hash from its name: `misc.GET_HASH_KEY("WEAPON_PISTOL")`.
`hidden=True` keeps it holstered, `equip_now=True` puts it in hand.
```

```{py:method} set_into(vehicle, seat=-1)

Put the ped in a seat of `vehicle`, instantly. `-1` is the driver, `0` the front passenger,
`1` and `2` the rear seats.
```

```{py:method} is_in_vehicle(vehicle=None)

`True` if the ped is in `vehicle`, or in any vehicle when `vehicle` is not given.
```

```{py:method} task_combat(target, combat_flags=0, threat_flags=16)

Order the ped to attack `target` (another `Ped`).
```

```{py:method} clear_tasks()

Cancel what the ped is doing (walking somewhere, fighting...).
```

```{py:method} set_as_cop(is_cop=True)

Make the ped act as a police officer.
```

```{py:method} set_relationship_group(group_hash)

Put the ped in a relationship group (who they like, who they hate). See the `ped` natives
`ADD_RELATIONSHIP_GROUP` and `SET_RELATIONSHIP_BETWEEN_GROUPS`.
```

```{py:property} is_shooting
:type: bool

`True` while the ped is firing a weapon.
```

```{py:property} is_jacking
:type: bool

`True` while the ped is stealing a vehicle.
```

```{py:method} delete()

Remove the ped now.
```
````

## Example

```python
from gta import player, world
from gta.natives import misc

INTERVAL_MS = 0
done = False


def on_tick():
    global done
    if done:
        return
    done = True
    me = player.current().ped
    x, y, z = me.position
    enemy = world.create_ped("g_m_y_ballaorig_01", (x + 10.0, y, z))
    if enemy:
        enemy.give_weapon(misc.GET_HASH_KEY("WEAPON_PISTOL"))
        enemy.task_combat(me)
```

More ped natives: [](natives/ped.md). AI orders: [](natives/task.md).
