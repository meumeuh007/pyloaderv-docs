# PyloaderV documentation

Source of the documentation of [PyloaderV](https://www.gta5-mods.com/tools/pyloader-python-scripts-for-gta-v-enhanced)
(also on [GTVault](https://gtvault.org/mods/pyloader-python-scripts-for-gta-v)), the mod that runs Python 3.12 scripts in GTA V (story mode), and of its developer kit
[`pyloaderv`](https://pypi.org/project/pyloaderv/) on PyPI.

Read it online: https://pyloaderv.readthedocs.io

## Build locally

Sphinx + Furo + MyST (Markdown). From the repository root:

    pip install -r docs/requirements.txt
    sphinx-build -b html docs docs/_build/html

Then open `docs/_build/html/index.html`. Live preview while editing:

    pip install sphinx-autobuild
    sphinx-autobuild docs docs/_build/html

The natives reference (`docs/reference/natives/`) is generated from
`tools/shvdn2py/natives.json` by `tools/gen_docs_natives.py`, which `docs/conf.py`
runs at the start of every build. Native descriptions come from the community
GTA V native database.

Read the Docs builds the site from `.readthedocs.yaml`.
