from __future__ import annotations

import importlib.resources
from pathlib import Path

_STATIC = importlib.resources.files("marimo_utils.ui.static")
DR_CSS = _STATIC.joinpath("dr.css").read_text(encoding="utf-8")
DR_STYLE_BLOCK = f'<style id="dr-styles">{DR_CSS}</style>'


def stylesheet_path() -> Path:
    """Filesystem path to the packaged stylesheet for web-host ``<link>`` usage."""
    return Path(str(_STATIC.joinpath("dr.css")))
