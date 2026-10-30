# Your first mod

In this tutorial you write a small mod that:

1. says hello when the game loads,
2. spawns a sports car in front of you when you press **F7**.

You only need to know the basics of Python (variables, `if`, functions).
Never modded GTA V before? Perfect, this page is for you.

```{note}
Install PyloaderV in your game first: [](install.md).
```

## 1. Set up your computer

You write mods on your PC with a normal Python and an editor. The game uses its own
Python, so this one is only for writing and packing your code.

1. Install **Python 3.12** from [python.org](https://www.python.org/downloads/).
   During the install, tick **"Add python.exe to PATH"**.
2. Install **Visual Studio Code** from [code.visualstudio.com](https://code.visualstudio.com/),
   then the **Python** extension (by Microsoft) from the Extensions tab.
3. Open a terminal (in VS Code: **Terminal → New Terminal**) and run:

```text
pip install pyloaderv
```

This gives you **autocomplete** for everything in the game API and the **`pyloaderv`** command.

```{tip}
If `pip` or `pyloaderv` is "not recognized", use `py -m pip install pyloaderv`
and `py -m pyloaderv` instead. They do the same thing.
```

## 2. Create the mod

In the terminal, go to a folder where you keep your projects (for example your Documents)
and run:

```text
pyloaderv new MyFirstMod
```

This creates a folder `MyFirstMod` with a ready-to-run `main.py`. Open the folder in
VS Code (**File → Open Folder...**).

```{tip}
If autocomplete does not work, press **Ctrl+Shift+P**, type **Python: Select Interpreter**
and pick the Python where you installed `pyloaderv`. More in [](editor.md).
```

## 3. Say hello

Replace everything in `main.py` with this:

```python
from gta import ui


def on_start():
    ui.notify("~g~MyFirstMod ~w~is running!")
```

What this means:

- `on_start` is a **callback**: a function with a special name that PyloaderV calls for you.
  `on_start` is called once, when the script is loaded.
- `ui.notify(...)` shows a message at the top left of the screen.
- `~g~` makes the text green and `~w~` white again. See [](../guide/screen.md#colors-and-formatting).

## 4. Try it in the game

Pack your folder into one `.pyv` file and copy it into the game, in one go
(replace the path with [your GTA V folder](install.md#step-1-find-your-game-folder)):

```text
pyloaderv pack MyFirstMod
pyloaderv install MyFirstMod.pyv --game "C:\Program Files\Rockstar Games\Grand Theft Auto V"
```

Start the game and load story mode. You see **"MyFirstMod is running!"** 🎉

```{tip}
Tired of typing `--game`? Set the `PYLOADERV_GAME` environment variable once:

    setx PYLOADERV_GAME "C:\Program Files\Rockstar Games\Grand Theft Auto V"

then open a new terminal. Now `pyloaderv install MyFirstMod.pyv` is enough.
```

**After each change**, run the two commands again, then press **F9** in game. F9 reloads
every Python script without restarting the game.

## 5. Spawn a car with a key

Now the fun part. Replace `main.py` with:

```python
from gta import player, ui, world
from gta.natives import entity

INTERVAL_MS = 0          # run on_tick every frame

spawn_requested = False


def on_start():
    ui.notify("~g~MyFirstMod: ~w~press ~y~F7 ~w~for a car")


def on_key_down(vk, down, shift, ctrl, alt):
    global spawn_requested
    if down and vk == 0x76:      # 0x76 is the F7 key
        spawn_requested = True   # just remember it, on_tick does the work


def on_tick():
    global spawn_requested
    if not spawn_requested:
        return
    spawn_requested = False

    me = player.current().ped
    # A point 5 metres in front of the player.
    pos = entity.GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(me.handle, 0.0, 5.0, 0.0)
    car = world.create_vehicle("adder", pos, heading=me.heading)
    if car:
        car.place_on_ground()
        ui.notify("~b~Here is your Adder!")
    else:
        ui.notify("~r~Could not spawn the car")
```

Pack, install, press **F9**, then **F7**: a car appears in front of you. 🚗

Let's read it piece by piece.

`INTERVAL_MS = 0`
: How often `on_tick` runs, in milliseconds. `0` means every frame.

`on_key_down(vk, down, shift, ctrl, alt)`
: Called when you press or release a key. `vk` is the key code (`0x76` = F7) and `down`
  is `True` when the key is pressed. See [](../guide/keyboard.md) for all key codes.

`spawn_requested = True`
: Why not spawn the car directly in `on_key_down`? Because spawning has to **wait** for the
  game to load the car model, and `on_key_down` is not allowed to wait. So the key only sets
  a flag, and `on_tick` (which can wait) does the work. This is the most important rule of
  PyloaderV, explained in [](../guide/waiting.md).

`player.current().ped`
: Your character. A "ped" is any person in the game, including you.

`entity.GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(...)`
: A **native**: a function of the game engine. There are 6649 of them, all listed in the
  [natives reference](../reference/natives/index.md).

`world.create_vehicle("adder", pos, heading=me.heading)`
: Loads the model, creates the car and returns a `Vehicle`, or `None` if it failed.
  `"adder"` is the model name. Try `"zentorno"`, `"t20"` or `"bati"`!

## 6. Share it

You already have it: `MyFirstMod.pyv` is your whole mod in one file. Send it to your friends
or upload it to gta5-mods or GTVault. Players copy it into their `pyscript` folder, done.

Want to hide your source code? Pack with `--bytecode` (see [](../guide/multi-file.md#hide-your-source-code)).

## What next?

- Learn how scripts really work: [](../guide/scripts.md).
- Grab ready-made snippets in the [](../cookbook/index.md).
- Browse what you can do with the [API reference](../reference/gta.md).
