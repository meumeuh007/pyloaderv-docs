# Changelog

## 0.9.2

- Fixed crashes and freezes when two scripts wait (`gta.wait()`, `world.load_model()`...)
  inside a function at the same time. Each script now runs on its own Python thread state, so
  scripts no longer see or overwrite each other's state.
- A script stopped by `ScriptTimeoutMs` is now cleaned up properly at the next reload or when
  the game exits.

## 0.9.1

- Fixed scripts running twice after loading a save (menus like pytrainer could glitch or stop
  responding).
- Fixed a crash when ScriptHookV reloads its plugins with CTRL+R (ScriptHookV developer mode).
- If Python fails to start, the game no longer crashes on the next key press: a message points
  to `PyloaderV.log`.

## 0.9

- **`.pyv` single-file mods**: a whole mod in one file, just drop it into `pyscript/` (F9 reload
  and `AutoReload` supported). Mods get private module namespaces with relative imports, so two
  mods can ship modules with the same name.
- **Natives with out-params fixed** (`GET_SHAPE_TEST_RESULT`, `GET_GROUND_Z_FOR_3D_COORD`,
  `GET_CURRENT_PED_WEAPON`... about 175 natives): they now return the values the game writes,
  e.g. `status, hit, pos, normal, ent = GET_SHAPE_TEST_RESULT(handle)`.
- **New raycast helpers**: `world.raycast(start, end)` and `world.raycast_from_camera()`.
- Fixed `Entity` / `Ped` / `Vehicle` `.delete()` and `.dismiss()`.
- `gta.Vector3` is now available to scripts.
- For mod authors: `pip install pyloaderv` gives autocomplete for the `gta` module and the
  `pyloaderv` command (`new`, `pack`, `install`, `pip`).

## 0.8

- Performance improvements: 1.4× faster on average, up to 2.4× in some cases.

## 0.7

- Performance improvements: 2.5× faster on average, up to 3.3× in some cases.
- Blueprint editor updated for 0.7 (for devs).

## 0.6

- **Standalone**: ScriptHookVDotNet is no longer required.

## 0.5

- Blueprint editor (beta, for devs).
- 0.5.1: bug fix.

## 0.4

- `PyloaderV.log`.
- Script priority with `__priority__`.
- Files in `Lib/` are detected during reload.
- New settings `LogEnabled` and `LogMaxSizeKB`.
- 0.4.1: tutorial fix.

## 0.3

- 0.3.1: syntax guide.
- 0.3.2: "for devs" folder.
