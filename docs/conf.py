"""Sphinx configuration for the PyloaderV documentation.

Build locally:
    pip install -r docs/requirements.txt
    sphinx-build -b html docs docs/_build/html
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent

# The natives reference is generated from natives.json on every build.
subprocess.check_call([sys.executable, str(ROOT / "tools" / "gen_docs_natives.py")])


def _core_version() -> str:
    # Source tree: read the core version. Docs-only repository: version.txt,
    # written by tools/export_docs_repo.py.
    gta_module = ROOT / "src" / "GtaModule.cpp"
    if gta_module.exists():
        m = re.search(r'"__version__",\s*"([^"]+)"', gta_module.read_text(encoding="utf-8"))
        return m.group(1) if m else ""
    return (DOCS / "version.txt").read_text(encoding="utf-8").strip()


project = "PyloaderV"
author = "meumeuh007"
copyright = "2026, meumeuh007"
release = _core_version()
version = release

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3

source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = ["_build", "README.md", "requirements.txt"]
language = "en"

html_theme = "furo"
html_title = f"PyloaderV {release}"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False
html_copy_source = False
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#1f7a4d",
        "color-brand-content": "#1f7a4d",
        "font-stack": "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    },
    "dark_css_variables": {
        "color-brand-primary": "#5fd39a",
        "color-brand-content": "#5fd39a",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

copybutton_prompt_text = r">>> |\.\.\. |\$ |PS> "
copybutton_prompt_is_regexp = True
copybutton_exclude = ".linenos, .gp, .go"

pygments_style = "friendly"
pygments_dark_style = "monokai"

suppress_warnings = ["myst.header"]
