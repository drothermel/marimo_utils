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
    DEFAULT = "bg-primary text-primary-foreground"
    SECONDARY = "bg-secondary text-secondary-foreground"
    DESTRUCTIVE = "bg-destructive text-destructive-foreground"
    OUTLINE = "text-foreground"


class SemanticTone(StrEnum):
    GOOD = "good"
    BAD = "bad"
    NEUTRAL = "neutral"


class ToneEmphasis(StrEnum):
    SOFT = "soft"
    SOLID = "solid"


class ToneSurface(StrEnum):
    GOOD_SOFT = "bg-tone-good-soft text-tone-good-soft-foreground"
    GOOD_SOLID = "bg-tone-good-solid text-tone-good-solid-foreground"
    BAD_SOFT = "bg-tone-bad-soft text-tone-bad-soft-foreground"
    BAD_SOLID = "bg-tone-bad-solid text-tone-bad-solid-foreground"
    NEUTRAL_SOFT = "bg-tone-neutral-soft text-tone-neutral-soft-foreground"
    NEUTRAL_SOLID = "bg-tone-neutral-solid text-tone-neutral-solid-foreground"


class ToneBorder(StrEnum):
    GOOD_SOFT = "border-tone-good-soft"
    GOOD_SOLID = "border-tone-good-solid"
    BAD_SOFT = "border-tone-bad-soft"
    BAD_SOLID = "border-tone-bad-solid"
    NEUTRAL_SOFT = "border-tone-neutral-soft"
    NEUTRAL_SOLID = "border-tone-neutral-solid"


def tone_surface(tone: SemanticTone, emphasis: ToneEmphasis) -> ToneSurface:
    return ToneSurface[f"{tone.name}_{emphasis.name}"]


def tone_border(tone: SemanticTone, emphasis: ToneEmphasis) -> ToneBorder:
    return ToneBorder[f"{tone.name}_{emphasis.name}"]
