"""Named Tailwind class enums for marimo_utils UI components.

Convention: no raw layout Tailwind in components — compose ``styles.*`` enums
via ``cn()`` from ``drhtml`` (tailwind-merge). Override per instance with the
``klass`` prop last.

Layout groups (``DivLayouts``, ``SpanLayouts``) and semantic component variants
(``BadgeVariant``, etc.) live here until the module grows enough to split.

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


BADGE_BASE = (
    "rounded-md border px-2.5 py-0.5 text-sm font-semibold transition-colors "
    "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
    "text-foreground"
)


class BadgeVariant(StrEnum):
    DEFAULT = (
        "border-transparent bg-primary "
        "text-primary-foreground hover:bg-primary/80"
    )
    SECONDARY = (
        "border-transparent bg-secondary text-secondary-foreground "
        "hover:bg-secondary/80"
    )
    DESTRUCTIVE = (
        "border-transparent bg-destructive text-destructive-foreground "
        "hover:bg-destructive/80"
    )
    OUTLINE = "text-foreground"
