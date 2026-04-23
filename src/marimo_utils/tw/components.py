from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import span  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.tw._rendering import html_block
from marimo_utils.tw.variants import BADGE_BASE, BADGE_VARIANT_CLASSES, BadgeVariant


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    variant: BadgeVariant = BadgeVariant.DEFAULT
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        parts = [BADGE_BASE, BADGE_VARIANT_CLASSES[self.variant]]
        if self.klass:
            parts.append(self.klass)
        classes = " ".join(parts)
        return html_block(span(self.label, klass=classes))


__all__ = ["Badge"]
