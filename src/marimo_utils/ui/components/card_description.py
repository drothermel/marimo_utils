from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import p  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui._rendering import html_block, render_inline


class CardDescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        base = "text-sm text-muted-foreground"
        classes = f"{base} {self.klass}" if self.klass else base
        return html_block(p(*render_inline(self.text), klass=classes))
