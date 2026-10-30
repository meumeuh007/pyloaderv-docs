# Settings (PyloaderV.ini)

`PyloaderV.ini`, in your GTA V folder, holds PyloaderV's settings. Open it with any text
editor (Notepad works). Changes apply the next time you start the game.

```ini
[PyloaderV]
ScriptsDir=pyscript
PythonHome=
ReloadKey=F9
AutoReload=false
HotReloadInterval=2
DebugMode=false
LogEnabled=true
LogMaxSizeKB=1024
ScriptTimeoutMs=5000
```

## All settings

`ScriptsDir` (default `pyscript`)
: The folder where your scripts live, relative to the GTA V folder.

`ReloadKey` (default `F9`)
: The key that reloads every script. Accepted values: `F1` to `F12`, `A` to `Z`, `0` to `9`,
  `Enter`, `Space`, `Tab`, `Escape`, `Insert`, `Delete`, `Home`, `End`, `PageUp`,
  `PageDown`, the arrows, and `Numpad0` to `Numpad9`. Scripts never see this key pressed.

`AutoReload` (default `false`)
: Set to `true` and PyloaderV reloads the scripts **by itself** as soon as a `.py` or `.pyv`
  file changes or appears in `ScriptsDir`. Very handy while you write a mod: save the file,
  look at the game. Turn it off for normal play.

`HotReloadInterval` (default `2`)
: With `AutoReload`, how often (in seconds) PyloaderV checks the files.

`DebugMode` (default `false`)
: Reserved for future use: it currently changes nothing.

`LogEnabled` (default `true`)
: Writes `PyloaderV.log` in the GTA V folder. Keep it on: it is where errors go.
  The log starts empty at each game launch.

`LogMaxSizeKB` (default `1024`)
: Maximum size of the log, in KB. When it is bigger, it is renamed `PyloaderV.log.old`
  and a new log starts.

`ScriptTimeoutMs` (default `5000`)
: If a script runs longer than this (in milliseconds) without waiting, PyloaderV stops it
  once it gives control back. `0` turns the check off. See [](waiting.md).

`PythonHome` (default empty)
: Advanced: use another Python 3.12 runtime instead of `shvpy_runtime`. Leave it empty.

## A good setup for writing mods

```ini
AutoReload=true
HotReloadInterval=1
```

Then, while the game runs: edit your script, save, and the change is live a second later.
With `.pyv` mods, `pyloaderv pack` + `pyloaderv install` triggers the reload too.
