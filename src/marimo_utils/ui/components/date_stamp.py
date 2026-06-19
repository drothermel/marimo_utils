from __future__ import annotations

from datetime import datetime

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.components.lucide_icon import LucideIcon
from marimo_utils.ui.drhtml import cn, div, html_block, span
from marimo_utils.ui.styles import DivLayouts


class DateStamp(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: datetime | None
    icon_name: str = "calendar"
    klass: str | None = None

    def _text(self) -> str:
        if self.value is None:
            return "--- --"
        return self.value.strftime("%b %d")

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                LucideIcon(name=self.icon_name).render(),
                span(
                    self._text(),
                    klass="text-sm font-medium text-muted-foreground",  # BODY_MUTED
                ),
                klass=cn(DivLayouts.INLINE_ROW, "gap-1", self.klass),
            )
        )
