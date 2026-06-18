from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import cn, div, html_block
from marimo_utils.ui.styles import BADGE_BASE, BadgeVariant, DivLayouts


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
                    self.variant,
                    self.klass,
                ),
            )
        )
