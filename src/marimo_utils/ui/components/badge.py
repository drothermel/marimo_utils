from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import cn, div, html_block
from marimo_utils.ui.styles import DivLayouts
from marimo_utils.ui.variants import (
    BADGE_BASE,
    BADGE_VARIANT_CLASSES,
    BadgeVariant,
)


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    variant: BadgeVariant = BadgeVariant.DEFAULT
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                self.label,
                klass=cn(
                    DivLayouts.INLINE_ROW,
                    BADGE_BASE,
                    BADGE_VARIANT_CLASSES[self.variant],
                    self.klass,
                ),
            )
        )
