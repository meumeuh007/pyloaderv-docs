# gta.vehicle

```python
from gta.vehicle import Vehicle
```

Cars, bikes, boats, planes and helicopters. Get vehicles from `world.create_vehicle(...)`,
`world.get_all_vehicles()`, or wrap a handle with `Vehicle(handle)`.

```{py:module} gta.vehicle
```

````{py:class} Vehicle(handle)

Has everything [`Entity`](entity.md) has (`position`, `heading`, `health`, `exists`,
`delete()`...), plus:

```{py:method} set_engine(on, instantly=True)

Turn the engine on or off.
```

```{py:method} place_on_ground()

Put the vehicle back on its wheels, on the ground. Returns `True` if it worked.
Useful right after spawning.
```

```{py:method} ped_in_seat(seat)

The [`Ped`](ped.md) in `seat` (`-1` = driver, `0` = front passenger, `1`, `2`... rear),
or `None` if the seat is empty.
```

```{py:property} is_driveable
:type: bool

`False` once the vehicle is destroyed or its engine is dead.
```

```{py:property} passenger_count
:type: int

How many passengers are in it (the driver not included).
```

```{py:property} max_passengers
:type: int

How many passenger seats it has.
```

```{py:method} delete()

Remove the vehicle now.
```
````

## The vehicle the player is in

```python
from gta import player
from gta.vehicle import Vehicle
from gta.natives import ped as ped_natives

me = player.current().ped
if me.is_in_vehicle():
    car = Vehicle(ped_natives.GET_VEHICLE_PED_IS_IN(me.handle, False))
    driver = car.ped_in_seat(-1)
```

## Example: tune it up

```python
from gta.natives import vehicle as vehicle_natives

def max_upgrade(car):
    h = car.handle
    vehicle_natives.SET_VEHICLE_MOD_KIT(h, 0)          # needed before any mod
    for mod_type in (11, 12, 13, 15, 16):             # engine, brakes, gearbox, suspension, armor
        count = vehicle_natives.GET_NUM_VEHICLE_MODS(h, mod_type)
        if count > 0:
            vehicle_natives.SET_VEHICLE_MOD(h, mod_type, count - 1, False)
    vehicle_natives.TOGGLE_VEHICLE_MOD(h, 18, True)    # turbo
    vehicle_natives.SET_VEHICLE_CUSTOM_PRIMARY_COLOUR(h, 20, 20, 20)
    vehicle_natives.SET_VEHICLE_NUMBER_PLATE_TEXT(h, "PYTHON")
```

More vehicle natives (colors, doors, lights, damage, speed...): [](natives/vehicle.md).
