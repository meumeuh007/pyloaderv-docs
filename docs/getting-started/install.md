# Install PyloaderV

This page installs PyloaderV in your game. It takes about five minutes, and you
**do not need to install Python**: PyloaderV brings its own.

## What you need

- **GTA V** on PC, the Legacy or the Enhanced edition (Steam, Epic or Rockstar launcher).
- **ScriptHookV**, the tool that lets mods run inside the game.
  Download it from [dev-c.com/gtav/scripthookv](http://www.dev-c.com/gtav/scripthookv/).
- **PyloaderV**, from its [gta5-mods page](https://www.gta5-mods.com/tools/pyloader-python-scripts-for-gta-v-enhanced).

## Step 1: find your game folder

Your game folder is the folder that contains **`GTA5.exe`** (Legacy) or
**`GTA5_Enhanced.exe`** (Enhanced). Common places:

| Launcher | Usual folder |
|---|---|
| Steam | `C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V` |
| Epic Games | `C:\Program Files\Epic Games\GTAV` |
| Rockstar Games Launcher | `C:\Program Files\Rockstar Games\Grand Theft Auto V` |

```{tip}
On Steam: right-click GTA V in your library, then **Manage → Browse local files**.
```

In this documentation, **"your GTA V folder"** always means this folder.

## Step 2: install ScriptHookV

Open the ScriptHookV zip and copy these two files from its `bin` folder into your GTA V folder:

- `ScriptHookV.dll`
- `dinput8.dll`

If ScriptHookV is already installed for other mods, skip this step.

## Step 3: install PyloaderV

Open the PyloaderV zip. Copy **only these four items** into your GTA V folder:

| Item | What it is |
|---|---|
| `PyloaderV.asi` | The mod itself. |
| `PyloaderV.ini` | Its settings (reload key, logs...). |
| `pyscript/` | The folder where Python scripts and mods go. |
| `shvpy_runtime/` | The Python 3.12 that runs inside the game. Do not rename it. |

Your GTA V folder now looks like this:

```text
Grand Theft Auto V/
├── GTA5.exe              (or GTA5_Enhanced.exe)
├── ScriptHookV.dll
├── dinput8.dll
├── PyloaderV.asi
├── PyloaderV.ini
├── pyscript/
│   ├── hello.py
│   └── vehicle_demo.py
└── shvpy_runtime/
```

```{note}
The zip also has a folder called `for devs (only)`. **Do not copy it** into the game:
it holds tools for people who write mods.
```

## Step 4: check that it works

1. Start GTA V and load **story mode**.
2. A notification appears at the top left: **"PyloaderV loaded (2 script(s))"**.
3. You also see **"hello.py loaded"**: that is the example script talking.

That's it: PyloaderV works. 🎉

Nothing appears? See [](../faq.md#nothing-happens-when-the-game-starts).

## Install a Python mod

Python mods are `.py` or `.pyv` files. To install one, **copy it into the `pyscript` folder**
and load the game (or press **F9** in game to reload the scripts).

To remove a mod, delete its file from `pyscript`. The two examples (`hello.py` and
`vehicle_demo.py`) can be deleted too.

## Uninstall PyloaderV

Delete these from your GTA V folder: `PyloaderV.asi`, `PyloaderV.ini`, `PyloaderV.log`,
`pyscript/` and `shvpy_runtime/`.

## Next step

Want to write your own mod? Continue with [](first-mod.md).
