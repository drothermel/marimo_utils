from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import cn, h3, html_block
from marimo_utils.ui.styles import Typography

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class CardTitle(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(h3(self.text, klass=cn(Typography.TITLE, self.klass)))
