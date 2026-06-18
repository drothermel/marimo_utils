"""Named Tailwind class enums for marimo_utils UI components.

Convention: no raw layout Tailwind in components — compose ``styles.*`` enums
via ``cn()`` from ``drhtml`` (tailwind-merge). Override per instance with the
``klass`` prop last.

Semantic component variants (e.g. badge color meaning) live in ``variants.py``,
not here.

Planned additions to this module:
- ``Typography`` — text size, weight, color
- ``Surface`` — border, background, shadow, radius
- ``Sizing`` — optional named widths and icon sizes
"""

from __future__ import annotations

from enum import StrEnum


class DivLayouts(StrEnum):
    COL_SHELL = "self-start flex flex-col gap-1.5"
    COL = "flex flex-col p-6 gap-1.5"
    INLINE_ROW = "self-start inline-flex items-center gap-2 flex-wrap"
    KEY_VAL_ROW = "flex items-baseline gap-3"


class SpanLayouts(StrEnum):
    KEY_VAL_LABEL = "inline-block min-w-28"
    ICON_FRAME = "inline-flex flex-shrink-0"
