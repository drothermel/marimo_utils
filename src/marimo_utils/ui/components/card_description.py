from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import html_block, p
from marimo_utils.ui.rendering import render_inline


class CardDescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        base = "text-sm text-muted-foreground"
        classes = f"{base} {self.klass}" if self.klass else base
        return html_block(p(*render_inline(self.text), klass=classes))
