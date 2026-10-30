# FAQ and troubleshooting

## For players

### Nothing happens when the game starts

No "PyloaderV loaded" notification? Check, in your GTA V folder:

1. **ScriptHookV is installed**: `ScriptHookV.dll` and `dinput8.dll` are there.
2. **ScriptHookV is up to date.** After each GTA V update, ScriptHookV stops working until
   it is updated too. Get the latest one from [dev-c.com](http://www.dev-c.com/gtav/scripthookv/).
3. **The PyloaderV files are in the right place**: `PyloaderV.asi` sits **next to** `GTA5.exe`
   (or `GTA5_Enhanced.exe`), not in a sub-folder. Same for `shvpy_runtime` and `pyscript`.
4. **You are in story mode.** Mods do not load in GTA Online.
5. If `PyloaderV.log` exists, open it: it says what went wrong.

### "PyloaderV: Python failed to start, see PyloaderV.log"

PyloaderV is loaded, but its Python runtime is broken. Usually the `shvpy_runtime` folder is
missing, renamed or incomplete: copy it again from the zip. The log has the details.

### A mod does not work

- Make sure its `.py` or `.pyv` file is **directly** in `pyscript`, not in a sub-folder.
- Read its description: some mods need [pip packages](guide/pip-packages.md).
- Look at the end of `PyloaderV.log`: an `[ERROR]` line names the mod and the problem.
  Send it to the mod author.

### Does PyloaderV work with ScriptHookVDotNet, LemonUI, other mods?

Yes. PyloaderV is independent: it does not need ScriptHookVDotNet and does not conflict with it.
Avoid mods that use the same key as PyloaderV's reload key (F9 by default, configurable).

### Legacy or Enhanced?

Both. The same files work for GTA V Legacy and GTA V Enhanced.

### Can I get banned?

PyloaderV is for **story mode only**, like every ScriptHookV mod. ScriptHookV itself refuses
to run in GTA Online. Do not try to use mods online.

## For mod makers

### Do I need to know C# or C++?

No. Only Python. PyloaderV, the game API and all natives are in Python.

### Which Python version does the game use?

CPython **3.12**, bundled in `shvpy_runtime`. Write code for 3.12.

### How do I make my script run every frame?

`INTERVAL_MS = 0` at the top of the file (it is also the default).

### `gta.wait()` does nothing / the game freezes when I press my key

You are waiting inside `on_key_down`. Use the [flag pattern](guide/waiting.md#the-flag-pattern-keys-that-need-to-wait).

### Can my two scripts share data?

Yes, through a module both import (a helper folder in `pyscript` or a pip package): both get
the same module object. For mods you publish, keep things private instead (see [](guide/multi-file.md)).

### Can I use threads or asyncio?

Python threads work for Python-only work (network, files). **Never call the game from a
thread**: see [](guide/pip-packages.md#slow-work-use-a-thread). `asyncio` works if you run
its loop step by step from `on_tick`, but `gta.wait()` is usually simpler.

### How do I find the native I need?

Search this site (top left), browse the [natives reference](reference/natives/index.md), or
start typing in your editor. The [](guide/natives.md) page has tips.

### Where are the examples?

- The [](cookbook/index.md) on this site.
- The PyloaderV zip: `pyscript/hello.py`, `pyscript/vehicle_demo.py`, and
  `for devs (only)/pyv-example/`.

### Is there a visual editor?

Yes: the PyloaderV zip has a **blueprint editor** in `for devs (only)/pyloader_blueprint_editor.html`.
Open it in your browser to build scripts with blocks.

### How do I report a bug or ask for a feature?

Comment on the [gta5-mods page](https://www.gta5-mods.com/tools/pyloader-python-scripts-for-gta-v-enhanced),
with your `PyloaderV.log` and, if you can, a small script that shows the problem.
