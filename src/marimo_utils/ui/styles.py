"""Named Tailwind class enums for marimo_utils UI components.

Convention: no raw layout Tailwind in components — compose ``styles.*`` enums
via ``cn()`` from ``drhtml`` (tailwind-merge). Override per instance with the
``klass`` prop last.
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


class Padding(StrEnum):
    BADGE = "px-2.5 py-0.5"


BORDER = "border border-border rounded-md shadow-sm"

BADGE_FOCUS = (
    "transition-colors focus:outline-none focus:ring-2 focus:ring-ring "
    "focus:ring-offset-2"
)


class Background(StrEnum):
    PRIMARY = "bg-primary text-primary-foreground hover:bg-primary/80"
    SECONDARY = "bg-secondary text-secondary-foreground hover:bg-secondary/80"
    DESTRUCTIVE = "bg-destructive text-destructive-foreground hover:bg-destructive/80"
    CARD = "bg-card"
    OUTLINE = "text-foreground hover:bg-accent hover:text-accent-foreground"


class BadgeVariant(StrEnum):
    DEFAULT = Background.PRIMARY
    SECONDARY = Background.SECONDARY
    DESTRUCTIVE = Background.DESTRUCTIVE
    OUTLINE = Background.OUTLINE
