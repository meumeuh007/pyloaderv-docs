# Cookbook

Ready-to-use scripts for common things. Each one is a **complete script**: save it as a `.py`
file in `pyscript`, press F9 in game, and try it. Then change it, combine them, make it yours.

```{tip}
Keys used here: F5, F6, F7, F8. If two recipes use the same key, change one: key codes are in
[](../guide/keyboard.md#key-codes).
```

## Teleport to the waypoint

Place a waypoint on the map, press **F5**. Works on foot and in a vehicle.

```python
import gta
from gta import player, ui
from gta.natives import entity, hud, misc, ped as ped_natives

INTERVAL_MS = 0
WAYPOINT_SPRITE = 8
requested = False


def teleport_to_waypoint():
    if not hud.IS_WAYPOINT_ACTIVE():
        ui.notify("~r~Place a waypoint on the map first")
        return
    x, y, _ = hud.GET_BLIP_INFO_ID_COORD(hud.GET_FIRST_BLIP_INFO_ID(WAYPOINT_SPRITE))

    me = player.current().ped
    target = me.handle
    if me.is_in_vehicle():
        target = ped_natives.GET_VEHICLE_PED_IS_IN(me.handle, False)

    # The ground height is only known once the area is loaded: go down step by step.
    for z in range(800, -100, -50):
        entity.SET_ENTITY_COORDS_NO_OFFSET(target, x, y, float(z), False, False, False)
        gta.wait(50)
        found, ground_z = misc.GET_GROUND_Z_FOR_3D_COORD(x, y, float(z), 0.0, False, False)
        if found:
            entity.SET_ENTITY_COORDS_NO_OFFSET(target, x, y, ground_z + 1.0, False, False, False)
            return
    ui.notify("~y~Ground not found, you may fall a bit")


def on_key_down(vk, down, shift, ctrl, alt):
    global requested
    if down and vk == 0x74:          # F5
        requested = True


def on_tick():
    global requested
    if requested:
        requested = False
        teleport_to_waypoint()
```

## God mode

**F6** toggles invincibility.

```python
from gta import player, ui
from gta.natives import player as player_natives

god = False


def set_god(on):
    player_natives.SET_PLAYER_INVINCIBLE(player.current().id, on)


def on_key_down(vk, down, shift, ctrl, alt):
    global god
    if down and vk == 0x75:          # F6
        god = not god
        set_god(god)
        ui.notify("God mode " + ("~g~ON" if god else "~r~OFF"))


def on_aborted():
    set_god(False)                   # do not stay invincible after a reload
```

## Never wanted

The police never chase you while this script runs.

```python
from gta import player
from gta.natives import player as player_natives

INTERVAL_MS = 1000


def on_start():
    player_natives.SET_MAX_WANTED_LEVEL(0)


def on_tick():
    me = player.current()
    if me.wanted_level > 0:
        me.wanted_level = 0


def on_aborted():
    player_natives.SET_MAX_WANTED_LEVEL(5)   # back to normal
```

## Spawn a car and get in

**F7** spawns a car in front of you and puts you in the driver's seat.

```python
from gta import player, ui, world
from gta.natives import entity

INTERVAL_MS = 0
MODEL = "zentorno"
requested = False


def on_key_down(vk, down, shift, ctrl, alt):
    global requested
    if down and vk == 0x76:          # F7
        requested = True


def on_tick():
    global requested
    if not requested:
        return
    requested = False

    me = player.current().ped
    pos = entity.GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(me.handle, 0.0, 4.0, 0.0)
    car = world.create_vehicle(MODEL, pos, heading=me.heading)
    if not car:
        ui.notify(f"~r~Cannot spawn {MODEL}")
        return
    car.place_on_ground()
    car.set_engine(True)
    me.set_into(car)                 # seat -1 = driver
    car.dismiss()                    # the game may clean it up when you leave it
```

## Repair and wash your vehicle

**F8** repairs and cleans the vehicle you are in.

```python
from gta import player, ui
from gta.natives import ped as ped_natives, vehicle as vehicle_natives


def on_key_down(vk, down, shift, ctrl, alt):
    if not (down and vk == 0x77):    # F8
        return
    me = player.current().ped
    if not me.is_in_vehicle():
        ui.notify("~r~You are not in a vehicle")
        return
    car = ped_natives.GET_VEHICLE_PED_IS_IN(me.handle, False)
    vehicle_natives.SET_VEHICLE_FIXED(car)
    vehicle_natives.SET_VEHICLE_DIRT_LEVEL(car, 0.0)
    ui.notify("~g~Good as new")
```

These natives do not wait, so they can run directly in `on_key_down`.

## Weather and time

**F5** cycles the weather, **F6** jumps forward 3 hours.

```python
from gta import ui
from gta.natives import clock, misc

WEATHERS = ["EXTRASUNNY", "CLEAR", "CLOUDS", "OVERCAST", "RAIN",
            "THUNDER", "FOGGY", "SMOG", "SNOW", "XMAS", "HALLOWEEN"]
index = 0


def on_key_down(vk, down, shift, ctrl, alt):
    global index
    if not down:
        return
    if vk == 0x74:                   # F5
        index = (index + 1) % len(WEATHERS)
        misc.SET_WEATHER_TYPE_NOW_PERSIST(WEATHERS[index])
        ui.notify(f"Weather: ~b~{WEATHERS[index]}")
    elif vk == 0x75:                 # F6
        hour = (clock.GET_CLOCK_HOURS() + 3) % 24
        clock.SET_CLOCK_TIME(hour, 0, 0)
        ui.notify(f"Time: ~y~{hour:02d}:00")


def on_aborted():
    misc.CLEAR_WEATHER_TYPE_PERSIST()
```

## Give weapons

**F7** gives a set of weapons with ammo.

```python
from gta import player, ui
from gta.natives import misc

WEAPONS = ["WEAPON_KNIFE", "WEAPON_PISTOL", "WEAPON_SMG", "WEAPON_PUMPSHOTGUN",
           "WEAPON_CARBINERIFLE", "WEAPON_SNIPERRIFLE", "WEAPON_RPG", "WEAPON_GRENADE"]


def on_key_down(vk, down, shift, ctrl, alt):
    if down and vk == 0x76:          # F7
        me = player.current().ped
        for name in WEAPONS:
            me.give_weapon(misc.GET_HASH_KEY(name), ammo=500, equip_now=False)
        ui.notify("~g~Armed and ready")
```

Weapon names: [weapon list](https://docs.fivem.net/docs/game-references/weapon-models/).

## Bodyguards

**F8** adds an armed bodyguard who follows you and fights your enemies.

```python
from gta import player, ui, world
from gta.natives import entity, misc, ped as ped_natives, player as player_natives

INTERVAL_MS = 0
requested = False
guards = []


def spawn_guard():
    me = player.current()
    pos = entity.GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(me.ped.handle, 1.5, -1.5, 0.0)
    guard = world.create_ped("s_m_y_blackops_01", pos, heading=me.ped.heading)
    if not guard:
        return
    group = player_natives.GET_PLAYER_GROUP(me.id)
    ped_natives.SET_PED_AS_GROUP_MEMBER(guard.handle, group)
    ped_natives.SET_PED_NEVER_LEAVES_GROUP(guard.handle, True)
    ped_natives.SET_PED_RELATIONSHIP_GROUP_HASH(
        guard.handle, ped_natives.GET_PED_RELATIONSHIP_GROUP_HASH(me.ped.handle))
    ped_natives.SET_PED_ACCURACY(guard.handle, 70)
    guard.give_weapon(misc.GET_HASH_KEY("WEAPON_CARBINERIFLE"), ammo=9999)
    guards.append(guard)
    ui.notify(f"~b~Bodyguard {len(guards)} ready")


def on_key_down(vk, down, shift, ctrl, alt):
    global requested
    if down and vk == 0x77:          # F8
        requested = True


def on_tick():
    global requested
    if requested:
        requested = False
        spawn_guard()


def on_aborted():
    for g in guards:
        if g:
            g.delete()
```

A player group holds up to 7 members.

## Speedometer

Shows your speed at the bottom right while you drive.

```python
from gta import player
from gta.natives import entity, hud

INTERVAL_MS = 0                      # draw every frame


def draw_text(text, x, y, scale=0.6):
    hud.SET_TEXT_FONT(4)
    hud.SET_TEXT_SCALE(scale, scale)
    hud.SET_TEXT_COLOUR(255, 255, 255, 255)
    hud.SET_TEXT_OUTLINE()
    hud.BEGIN_TEXT_COMMAND_DISPLAY_TEXT("STRING")
    hud.ADD_TEXT_COMPONENT_SUBSTRING_PLAYER_NAME(text)
    hud.END_TEXT_COMMAND_DISPLAY_TEXT(x, y, 0)


def on_tick():
    me = player.current().ped
    if not me.is_in_vehicle():
        return
    kmh = entity.GET_ENTITY_SPEED(me.handle) * 3.6     # m/s → km/h (× 2.237 for mph)
    draw_text(f"{kmh:.0f} km/h", 0.88, 0.90)
```

## What am I looking at?

**F5** tells you what is in the middle of the screen, no need to aim.

```python
from gta import ui, world
from gta.natives import entity, vehicle


def on_key_down(vk, down, shift, ctrl, alt):
    if not (down and vk == 0x74):    # F5
        return
    hit = world.raycast_from_camera(distance=300.0)
    if not hit.hit:
        ui.notify("Nothing (sky?)")
    elif hit.entity and entity.IS_ENTITY_A_VEHICLE(hit.entity):
        model = entity.GET_ENTITY_MODEL(hit.entity)
        ui.notify(f"A vehicle: ~b~{vehicle.GET_DISPLAY_NAME_FROM_VEHICLE_MODEL(model)}")
    elif hit.entity and entity.IS_ENTITY_A_PED(hit.entity):
        ui.notify("A person")
    else:
        x, y, z = hit.position
        ui.notify(f"The map at ~y~{x:.0f}, {y:.0f}, {z:.0f}")
```

Raycasts do not wait, so `on_key_down` is fine here.

## Explosion where you look

**F6** makes an explosion at the point in the middle of the screen. Careful. 💥

```python
from gta import world
from gta.natives import fire

EXPLOSION_GRENADE = 0


def on_key_down(vk, down, shift, ctrl, alt):
    if down and vk == 0x75:          # F6
        hit = world.raycast_from_camera(distance=500.0)
        if hit.hit:
            x, y, z = hit.position
            fire.ADD_EXPLOSION(x, y, z, EXPLOSION_GRENADE, 1.0, True, False, 1.0, False)
```

## Super jump and fast run

```python
from gta import player
from gta.natives import misc, player as player_natives

INTERVAL_MS = 0


def on_start():
    player_natives.SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER(player.current().id, 1.49)  # 1.49 is the max


def on_tick():
    misc.SET_SUPER_JUMP_THIS_FRAME(player.current().id)   # must be called every frame


def on_aborted():
    player_natives.SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER(player.current().id, 1.0)
```

## Slow motion

**F7** toggles slow motion.

```python
from gta.natives import misc

slow = False


def on_key_down(vk, down, shift, ctrl, alt):
    global slow
    if down and vk == 0x76:          # F7
        slow = not slow
        misc.SET_TIME_SCALE(0.3 if slow else 1.0)


def on_aborted():
    misc.SET_TIME_SCALE(1.0)
```

## Save and load a position

**F5** saves where you stand to a file, **F6** brings you back there, even after restarting the game.

```python
import json
import os

from gta import player, ui

SAVE_FILE = os.path.join(os.path.dirname(__file__), "saved_position.json")


def on_key_down(vk, down, shift, ctrl, alt):
    if not down:
        return
    me = player.current().ped
    if vk == 0x74:                   # F5: save
        x, y, z = me.position
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"x": x, "y": y, "z": z, "heading": me.heading}, f)
        ui.notify("~g~Position saved")
    elif vk == 0x75:                 # F6: load
        if not os.path.exists(SAVE_FILE):
            ui.notify("~r~Nothing saved yet")
            return
        with open(SAVE_FILE, encoding="utf-8") as f:
            data = json.load(f)
        me.position = (data["x"], data["y"], data["z"])
        me.heading = data["heading"]
```

In a `.pyv` mod, build the path as shown in [](../guide/multi-file.md#save-files-settings-progress).

## A map blip with a GPS route

```python
from gta.natives import hud

blip = 0


def on_start():
    global blip
    blip = hud.ADD_BLIP_FOR_COORD(-1037.0, -2737.0, 20.0)   # the airport
    hud.SET_BLIP_SPRITE(blip, 90)                           # plane icon
    hud.SET_BLIP_COLOUR(blip, 3)                            # blue
    hud.SET_BLIP_ROUTE(blip, True)


def on_aborted():
    hud.REMOVE_BLIP(blip)
```

More about blips, markers and text: [](../guide/screen.md).
