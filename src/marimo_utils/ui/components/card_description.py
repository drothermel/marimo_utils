from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import cn, html_block, p
from marimo_utils.ui.rendering import render_inline
from marimo_utils.ui.styles import Typography

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class CardDescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            p(*render_inline(self.text), klass=cn(Typography.BODY, self.klass))
        )
