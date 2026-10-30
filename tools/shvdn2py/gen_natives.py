"""
Generate pure-Python wrappers for every GTA V native from natives.json.

Output:
    _draft/natives/__init__.py
    _draft/natives/<namespace>.py   (one per namespace: PLAYER, VEHICLE, ...)
    _draft/natives/<namespace>.pyi  (stubs)

Every native becomes a one-liner wrapper around `gta.invoke(HASH, ...)`.
This is build-time generation — the output is reviewed (or at least spot-checked)
before shipping in `shvpy_runtime/pylib/gta/natives/`.
"""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NATIVES_JSON = ROOT / "natives.json"
OUT_DIR = ROOT / "_draft" / "natives"


# ─── Type mapping ───────────────────────────────────────────────────────────
# (python_annotation, gta.invoke return_type, is_pointer)

HANDLE_TYPES = {"Ped", "Vehicle", "Entity", "Player", "Object", "Blip",
                "Cam", "Pickup", "Interior", "ScrHandle", "FireId"}

def map_type(cs: str) -> tuple[str, str, bool]:
    t = cs.strip()
    is_ptr = t.endswith("*")
    if is_ptr:
        t = t.rstrip("*").strip()

    if t == "void":         return ("None", "void", False)
    if t == "BOOL":         return ("bool", "bool", is_ptr)
    if t == "int":          return ("int", "int", is_ptr)
    if t == "float":        return ("float", "float", is_ptr)
    if t == "const char":   return ("str", "string", is_ptr)
    if t == "char":         return ("str", "string", is_ptr)
    if t == "Vector3":      return ("'gta.Vector3'", "vector3", is_ptr)
    if t == "Hash":         return ("int", "int", is_ptr)
    if t == "Any":          return ("int", "int", is_ptr)
    if t in HANDLE_TYPES:   return ("int", "handle", is_ptr)
    return ("int", "int", is_ptr)  # unknown -> int


# ─── Typed fast-path bindings ────────────────────────────────────────────────
# Each native calls a typed gta._invoke_* function (METH_FASTCALL, no kwargs)
# instead of the generic gta.invoke(..., return_type=...). Maps the invoke
# return_type (2nd element of map_type) to (C function name, local alias).

FAST = {
    "void":    ("_invoke_void",    "_iv"),
    "bool":    ("_invoke_bool",    "_ib"),
    "int":     ("_invoke_int",     "_ii"),
    "handle":  ("_invoke_int",     "_ii"),   # handle decodes the same as int
    "float":   ("_invoke_float",   "_if"),
    "string":  ("_invoke_str",     "_is"),
    "vector3": ("_invoke_vector3", "_ivec"),
}
# Stable import order for the per-module `from gta import ...` line.
FAST_ORDER = ["_invoke_void", "_invoke_bool", "_invoke_int",
              "_invoke_float", "_invoke_str", "_invoke_vector3"]
FAST_ALIAS = {full: alias for full, alias in FAST.values()}


# ─── Identifier hygiene ─────────────────────────────────────────────────────

PY_KEYWORDS = set(keyword.kwlist) | {"match", "case"}

def safe_ident(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if not name or name[0].isdigit():
        name = "_" + name
    if name in PY_KEYWORDS:
        name = name + "_"
    return name


# ─── Emit one namespace ─────────────────────────────────────────────────────

# Typed pointer params become out-params handled by gta._out: the Python
# argument is the pointer's initial value (optional when trailing) and the
# wrapper returns what the native wrote. Any* stays a raw address (unknown size).
# kind letter, input annotation, output annotation, default value
OUT_KINDS = {
    "BOOL":    ("b", "bool", "bool", "False"),
    "int":     ("i", "int", "int", "0"),
    "Hash":    ("i", "int", "int", "0"),
    "float":   ("f", "float", "float", "0.0"),
    "Vector3": ("v", "tuple[float, float, float]", "'gta.Vector3'", "(0.0, 0.0, 0.0)"),
}
for _h in HANDLE_TYPES:
    OUT_KINDS[_h] = ("i", "int", "int", "0")


def out_kind(cs: str):
    t = cs.strip()
    if not t.endswith("*"):
        return None
    return OUT_KINDS.get(t.rstrip("*").strip())


def emit_native(hash_hex: str, nat: dict) -> tuple[str, str, str, bool]:
    """Return (py_src, pyi_line, fast_fullname, uses_out) for a single native."""
    name = nat["name"]
    params = nat.get("params", [])
    ret_type = nat.get("return_type", "void")

    py_ret_ann, invoke_ret, _ = map_type(ret_type)

    names: list[str] = []
    used: set[str] = set()
    for p in params:
        pname = safe_ident(p.get("name", "arg"))
        # dedupe (some natives have duplicate param names)
        base = pname
        i = 2
        while pname in used:
            pname = f"{base}{i}"
            i += 1
        used.add(pname)
        names.append(pname)

    outs = [out_kind(p["type"]) for p in params]
    # Out-params after the last plain param get a default, so callers can omit them.
    last_plain = max((i for i, o in enumerate(outs) if o is None), default=-1)

    py_params: list[str] = []
    pyi_params: list[str] = []
    for i, (p, pname, out) in enumerate(zip(params, names, outs)):
        if out is not None:
            ann = out[1]
            if i > last_plain:
                py_params.append(f"{pname}: {ann} = {out[3]}")
                pyi_params.append(f"{pname}: {ann} = ...")
                continue
        else:
            ann, _, is_ptr = map_type(p["type"])
            # Any* (and other untyped pointers) stay raw addresses. `const char*`
            # is a plain string input, keep the `str` type.
            if is_ptr and p["type"].strip() not in ("const char*", "char*"):
                ann = "int"
        py_params.append(f"{pname}: {ann}")
        pyi_params.append(f"{pname}: {ann}")

    sig_py = ", ".join(py_params)
    sig_pyi = ", ".join(pyi_params)
    call_list = ", ".join(names)
    fast_full, fast_alias = FAST[invoke_ret]
    out_anns = [o[2] for o in outs if o is not None]

    if out_anns:
        kinds = "".join(o[0] if o else "-" for o in outs)
        if ret_type == "void":
            ret_ann = out_anns[0] if len(out_anns) == 1 else f"tuple[{', '.join(out_anns)}]"
            py_body = f'    return _ocv({fast_alias}, {hash_hex}, "{kinds}", {call_list})'
        else:
            ret_ann = f"tuple[{', '.join([py_ret_ann] + out_anns)}]"
            py_body = f'    return _oc({fast_alias}, {hash_hex}, "{kinds}", {call_list})'
    else:
        ret_ann = py_ret_ann
        call = f"{fast_alias}({hash_hex}, {call_list})" if call_list else f"{fast_alias}({hash_hex})"
        py_body = f"    {call}" if ret_type == "void" else f"    return {call}"

    py = f"def {name}({sig_py}) -> {ret_ann}:\n{py_body}\n"
    pyi = f"def {name}({sig_pyi}) -> {ret_ann}: ..."
    return py, pyi, fast_full, bool(out_anns)


def emit_namespace(ns_name: str, natives: dict, out_dir: Path) -> int:
    # Stable order: by hash. Emit natives first so we know which typed
    # fast-path functions this namespace actually uses (for the import line).
    items = sorted(natives.items(), key=lambda kv: kv[0])
    native_pys: list[str] = []
    pyi_bodies: list[str] = []
    used_fns: set[str] = set()
    uses_out = False
    count = 0
    for hash_hex, nat in items:
        try:
            normalized_hash = f"0x{int(hash_hex, 16):016X}"
        except ValueError:
            continue
        py, pyi, fast_full, native_out = emit_native(normalized_hash, nat)
        uses_out = uses_out or native_out
        native_pys.append(py)
        pyi_bodies.append(pyi)
        used_fns.add(fast_full)
        count += 1

    imports = [f for f in FAST_ORDER if f in used_fns]
    import_line = (
        "from gta import " + ", ".join(f"{f} as {FAST_ALIAS[f]}" for f in imports)
        if imports else ""
    )

    py_lines = [
        f'"""Auto-generated raw native bindings for namespace {ns_name}.',
        "",
        "Generated from natives.json — do not edit by hand. Re-run gen_natives.py",
        "to refresh. Idiomatic wrappers live in gta.world, gta.ui, etc.",
        "",
        "Each native calls a typed gta._invoke_* fast-path (vectorcall, no kwargs).",
        '"""',
        "",
        "import gta",
    ]
    if import_line:
        py_lines.append(import_line)
    if uses_out:
        py_lines.append("from gta._out import call as _oc, call_void as _ocv")
    py_lines += ["", ""]
    py_lines += native_pys

    pyi_lines = [
        f"# Stubs for gta.natives.{ns_name.lower()}",
        "",
        "import gta",
        "",
    ]
    pyi_lines += pyi_bodies

    fname = ns_name.lower()
    (out_dir / f"{fname}.py").write_text("\n".join(py_lines), encoding="utf-8")
    (out_dir / f"{fname}.pyi").write_text("\n".join(pyi_lines) + "\n", encoding="utf-8")
    return count


# ─── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    data = json.loads(NATIVES_JSON.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    ns_list = []
    for ns_name, natives in data.items():
        n = emit_namespace(ns_name, natives, OUT_DIR)
        ns_list.append((ns_name, n))
        total += n

    # Package __init__.py — imports every namespace module.
    init_py = ['"""Auto-generated native bindings package."""', ""]
    for ns_name, _ in ns_list:
        init_py.append(f"from . import {ns_name.lower()}")
    (OUT_DIR / "__init__.py").write_text("\n".join(init_py) + "\n", encoding="utf-8")

    # __init__.pyi
    init_pyi = ["# Stubs for gta.natives", ""]
    for ns_name, _ in ns_list:
        init_pyi.append(f"from . import {ns_name.lower()} as {ns_name.lower()}")
    (OUT_DIR / "__init__.pyi").write_text("\n".join(init_pyi) + "\n", encoding="utf-8")

    print(f"{total} natives across {len(ns_list)} namespaces")
    for ns_name, n in sorted(ns_list, key=lambda kv: -kv[1])[:10]:
        print(f"  {ns_name}: {n}")
    print(f"output: {OUT_DIR.relative_to(ROOT.parent.parent)}")


if __name__ == "__main__":
    main()
