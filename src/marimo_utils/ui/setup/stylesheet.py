from __future__ import annotations

import importlib.resources
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

_STATIC = importlib.resources.files("marimo_utils.ui.static")
DR_CSS = _STATIC.joinpath("dr.css").read_text(encoding="utf-8")
DR_STYLE_BLOCK = f'<style id="dr-styles">{DR_CSS}</style>'


@contextmanager
def stylesheet_path() -> Iterator[Path]:
    """Filesystem path to the packaged stylesheet for web-host ``<link>`` usage.

    Use as a context manager so the path resolves correctly for wheel/zip
    installs via :func:`importlib.resources.as_file`.
    """
    ref = _STATIC.joinpath("dr.css")
    with importlib.resources.as_file(ref) as path:
        yield path
