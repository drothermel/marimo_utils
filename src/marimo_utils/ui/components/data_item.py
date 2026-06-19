from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.core.drhtml import cn, div, html_block, span
from marimo_utils.ui.styles import DivLayouts, SpanLayouts, Typography

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


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
                        Typography.XS_MUTED,
                        Typography.LABEL_CASE,
                    ),
                ),
                span(self.value, klass=Typography.BODY_SEMIBOLD),
                klass=cn(DivLayouts.KEY_VAL_ROW, self.klass),
            )
        )
