"""
Generate the natives reference pages of the documentation from natives.json.

Output (overwritten on every run, not edited by hand):
    docs/reference/natives/index.md
    docs/reference/natives/<namespace>.md

Signatures come from tools/shvdn2py/gen_natives.py, so the docs always show
exactly what the shipped gta.natives wrappers accept and return. Called
automatically by docs/conf.py at the start of every Sphinx build; can also be
run by hand:
    python tools/gen_docs_natives.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "shvdn2py"))

from gen_natives import NATIVES_JSON, emit_native  # noqa: E402

OUT_DIR = ROOT / "docs" / "reference" / "natives"

# One line per namespace for the index page, written for beginners.
NAMESPACE_INFO = {
    "APP": "Data used by the in-game phone apps.",
    "AUDIO": "Sounds, music, radio stations, speech and police scanner.",
    "BRAIN": "Script brains attached to world objects (advanced).",
    "BUILTIN": "Core script functions: waiting, timers, maths (sin, cos, sqrt...).",
    "CAM": "Cameras: create your own camera, shake, zoom, gameplay camera info.",
    "CLOCK": "In-game time and date.",
    "CUTSCENE": "Load and play cutscenes.",
    "DATAFILE": "Read and write JSON-like data files (mostly online).",
    "DECORATOR": "Attach small named values to entities.",
    "DLC": "Check which DLC content is present.",
    "ENTITY": "Anything that exists in the world (peds, vehicles, objects): position, health, speed, visibility...",
    "EVENT": "Game events and AI reactions.",
    "EXTRAMETADATA": "Shop and clothing metadata.",
    "FIRE": "Fires and explosions.",
    "GRAPHICS": "Drawing on screen and in the world: lines, boxes, sprites, particles, timecycles.",
    "HUD": "Interface: notifications, text, help messages, blips on the map, radar, waypoint.",
    "INTERIOR": "Interiors (buildings you can enter).",
    "ITEMSET": "Sets of items (advanced).",
    "LOBBY": "Lobby and session state.",
    "LOCALIZATION": "Game language.",
    "MISC": "A bit of everything: weather, hashes (GET_HASH_KEY), ground height, cheats, random numbers.",
    "MOBILE": "The player's phone.",
    "MONEY": "Money and transactions (mostly online).",
    "NETSHOPPING": "Online shopping (GTA Online only).",
    "NETWORK": "Multiplayer functions (GTA Online only, not useful in story mode).",
    "OBJECT": "Props and objects: create, move, doors, pickups.",
    "PAD": "Controller and keyboard input (controls, vibration).",
    "PATHFIND": "Roads and navigation: closest road, vehicle nodes, paths.",
    "PED": "Characters (peds): create, health, armor, clothes, groups, relationships.",
    "PHYSICS": "Ropes and physics.",
    "PLAYER": "The player: wanted level, invincibility, controls, model, money in story mode.",
    "RECORDING": "Rockstar Editor recording.",
    "REPLAY": "Replay system.",
    "SAVEMIGRATION": "Save migration (advanced).",
    "SCRIPT": "Game scripts: start, stop and check other scripts.",
    "SECURITY": "Security checks (advanced).",
    "SHAPETEST": "Raycasts and shape tests: what is in front of you, line of sight.",
    "SOCIALCLUB": "Social Club (online).",
    "STATS": "Player statistics (skills, progress).",
    "STREAMING": "Loading models, animations and other assets into memory.",
    "TASK": "AI tasks: make peds walk, drive, fight, follow, play animations.",
    "VEHICLE": "Vehicles: create, repair, colors, mods, doors, engine, speed.",
    "WATER": "Water level and waves.",
    "WEAPON": "Weapons: give, remove, ammo, damage.",
    "ZONE": "Map zones and their names.",
}

URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")


def notes_html(comment: str) -> str:
    """Native comments are free text (lists, enums, code): keep them verbatim."""
    out, last = [], 0
    for m in URL_RE.finditer(comment):
        out.append(html.escape(comment[last:m.start()]))
        url = html.escape(m.group(0))
        out.append(f'<a href="{url}" rel="nofollow noopener">{url}</a>')
        last = m.end()
    out.append(html.escape(comment[last:]))
    text = "".join(out).expandtabs(4).strip("\n")
    return f'<pre class="native-notes">{text}</pre>'


def c_signature(nat: dict) -> str:
    params = ", ".join(f'{p["type"]} {p.get("name", "")}'.strip() for p in nat.get("params", []))
    return f'{nat.get("return_type", "void")} {nat["name"]}({params})'


def namespace_page(ns: str, natives: dict) -> str:
    mod = ns.lower()
    items = sorted(natives.values(), key=lambda n: n["name"].lstrip("_"))
    hashes = {id(n): h for h, n in natives.items()}
    lines = [
        f"# {mod}",
        "",
        f"{NAMESPACE_INFO.get(ns, '')} **{len(items)} natives.**",
        "",
        "```python",
        f"from gta.natives import {mod}",
        "```",
        "",
        "Natives with a pointer argument (`BOOL*`, `int*`, `Vector3*`...) return what the game",
        "writes there, after the normal result. See [](/guide/natives.md).",
        "",
    ]
    for nat in items:
        hash_hex = hashes[id(nat)]
        _, pyi, _, _ = emit_native(f"0x{int(hash_hex, 16):016X}", nat)
        sig = pyi.removeprefix("def ").removesuffix(": ...")
        lines += [
            f"## {nat['name']}",
            "",
            "```python",
            f"{mod}.{sig}",
            "```",
            "",
            f"<p class=\"native-meta\">C: <code>{html.escape(c_signature(nat))}</code>"
            f" &middot; hash <code>{int(hash_hex, 16):#018x}</code></p>",
            "",
        ]
        comment = (nat.get("comment") or "").strip()
        if comment:
            lines += [notes_html(comment), ""]
    return "\n".join(lines)


def index_page(data: dict) -> str:
    total = sum(len(v) for v in data.values())
    lines = [
        "# Natives",
        "",
        f"Natives are the functions of the game engine itself. PyloaderV gives you **all {total}**",
        "of them, grouped by namespace, in `gta.natives`:",
        "",
        "```python",
        "from gta.natives import player, vehicle",
        "",
        "ped = player.PLAYER_PED_ID()",
        "```",
        "",
        "New to natives? Read [](/guide/natives.md) first.",
        "",
        "```{tip}",
        "Looking for one native? Type its name (or a word like `WEATHER`) in the search box.",
        "Your editor autocompletes them too after `pip install pyloaderv`.",
        "```",
        "",
        "| Namespace | What it is for | Natives |",
        "|---|---|---|",
    ]
    for ns in sorted(data):
        mod = ns.lower()
        lines.append(f"| [{mod}]({mod}.md) | {NAMESPACE_INFO.get(ns, '')} | {len(data[ns])} |")
    lines += [
        "",
        "Descriptions come from the community native database. Many natives have no",
        "description yet, and parameter names like `p1` mean nobody knows exactly what they do.",
        "",
        "```{toctree}",
        ":hidden:",
        "",
        *[ns.lower() for ns in sorted(data)],
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    data = json.loads(NATIVES_JSON.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()
    for ns, natives in data.items():
        (OUT_DIR / f"{ns.lower()}.md").write_text(namespace_page(ns, natives), encoding="utf-8")
    (OUT_DIR / "index.md").write_text(index_page(data), encoding="utf-8")
    print(f"natives docs: {sum(len(v) for v in data.values())} natives, {len(data)} pages -> {OUT_DIR}")


if __name__ == "__main__":
    main()
