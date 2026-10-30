# PyloaderV

<p class="hero-tagline">Write GTA V mods in real Python.</p>

PyloaderV runs **Python 3.12 inside GTA V** (story mode). Put a `.py` file in a folder,
start the game, and your code runs. You can use everything Python has: f-strings,
classes, the standard library, and packages from pip like `numpy` or `requests`.

```python
from gta import ui

def on_start():
    ui.notify("~g~Hello from Python!")
```

You do not need C#, Visual Studio or any compiler. If you can write a few lines of
Python, you can make a mod.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🚀 Install
:link: getting-started/install
:link-type: doc

Install PyloaderV in your game and check that it works.
:::

:::{grid-item-card} 🧩 Your first mod
:link: getting-started/first-mod
:link-type: doc

A step-by-step tutorial: from an empty file to a mod that spawns a car.
:::

:::{grid-item-card} 📖 Guide
:link: guide/scripts
:link-type: doc

How scripts work: callbacks, waiting, keys, entities, natives, packaging.
:::

:::{grid-item-card} 🍳 Cookbook
:link: cookbook/index
:link-type: doc

Copy-paste recipes: teleport, god mode, weather, bodyguards, on-screen text...
:::

:::{grid-item-card} 🔎 API reference
:link: reference/gta
:link-type: doc

Every function of the `gta` module and its helpers.
:::

:::{grid-item-card} ⚙️ All 6649 natives
:link: reference/natives/index
:link-type: doc

The full list of game functions, with parameters and descriptions.
:::
::::

## Who is this for?

- **Players** who want to install a Python mod: read [](getting-started/install.md), that is all you need.
- **Beginners** who want to make their first mod: follow [](getting-started/install.md),
  then [](getting-started/first-mod.md). No GTA modding experience needed.
- **Experienced modders** coming from ScriptHookVDotNet or Lua: jump to [](guide/scripts.md)
  and the [natives reference](reference/natives/index.md).

```{note}
PyloaderV is for **story mode only**. Mods are not allowed in GTA Online and will not work there.
```

```{toctree}
:hidden:
:caption: Getting started

getting-started/install
getting-started/first-mod
getting-started/editor
```

```{toctree}
:hidden:
:caption: Guide

guide/scripts
guide/waiting
guide/keyboard
guide/entities
guide/natives
guide/screen
guide/multi-file
guide/pip-packages
guide/configuration
guide/debugging
```

```{toctree}
:hidden:
:caption: Cookbook

cookbook/index
```

```{toctree}
:hidden:
:caption: Reference

reference/gta
reference/player
reference/world
reference/entity
reference/ped
reference/vehicle
reference/ui
reference/math
reference/cli
reference/natives/index
```

```{toctree}
:hidden:
:caption: Help

faq
changelog
```
