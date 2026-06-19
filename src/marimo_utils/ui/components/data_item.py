from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import cn, div, html_block, span
from marimo_utils.ui.styles import DivLayouts, SpanLayouts


class DataItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                span(
                    self.label,
                    klass=cn(
                        SpanLayouts.KEY_VAL_LABEL,
                        "text-xs font-medium text-muted-foreground uppercase tracking-wide",
                    ),  # XS_MUTED, LABEL_CASE
                ),
                span(
                    self.value,
                    klass="text-sm font-semibold text-foreground",  # BODY_SEMIBOLD
                ),
                klass=cn(DivLayouts.KEY_VAL_ROW, self.klass),
            )
        )
