"""Named Tailwind class enums for marimo_utils UI components.

Convention: no raw layout Tailwind in components — compose ``styles.*`` enums
via ``cn()`` from ``drhtml`` (tailwind-merge). Override per instance with the
``klass`` prop last.

Exports: ``DivLayouts``, ``SpanLayouts``, ``Typography``, ``IconSize``,
``CardWidth``, ``BadgeVariant``, ``BADGE_BASE``.

Planned additions to this module:
- ``Surface`` — border, background, shadow, radius
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


class Typography(StrEnum):
    TITLE = "text-2xl font-semibold leading-none tracking-tight"
    XS_MUTED = "text-xs font-medium text-muted-foreground"
    BODY_MUTED = "text-sm font-medium text-muted-foreground"
    BODY = "text-sm font-medium text-foreground"
    BODY_SEMIBOLD = "text-sm font-semibold text-foreground"
    LABEL_CASE = "uppercase tracking-wide"


class IconSize(StrEnum):
    SMALL = "h-4 w-4"
    MEDIUM = "h-6 w-6"
    LARGE = "h-8 w-8"


class CardWidth(StrEnum):
    NARROW = "w-80"
    DEFAULT = "w-100"
    WIDE = "w-160"


BADGE_BASE = (
    "rounded-md border px-2.5 py-0.5 transition-colors "
    "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
)


class BadgeVariant(StrEnum):
    DEFAULT = (
        "border-transparent bg-primary text-primary-foreground hover:bg-primary/80"
    )
    SECONDARY = (
        "border-transparent bg-secondary text-secondary-foreground "
        "hover:bg-secondary/80"
    )
    DESTRUCTIVE = (
        "border-transparent bg-destructive text-destructive-foreground "
        "hover:bg-destructive/80"
    )
