from __future__ import annotations

from enum import StrEnum


class BadgeVariant(StrEnum):
    DEFAULT = "default"
    SECONDARY = "secondary"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"


BADGE_BASE = (
    "self-start inline-flex items-center rounded-md border px-2.5 py-0.5 "
    "text-xs font-semibold transition-colors "
    "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
)


BADGE_VARIANT_CLASSES: dict[BadgeVariant, str] = {
    BadgeVariant.DEFAULT: (
        "border-transparent bg-primary "
        "text-primary-foreground hover:bg-primary/80"
    ),
    BadgeVariant.SECONDARY: (
        "border-transparent bg-secondary text-secondary-foreground "
        "hover:bg-secondary/80"
    ),
    BadgeVariant.DESTRUCTIVE: (
        "border-transparent bg-destructive text-destructive-foreground "
        "hover:bg-destructive/80"
    ),
    BadgeVariant.OUTLINE: "text-foreground",
}
