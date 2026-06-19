from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import h3, html_block


class CardTitle(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        base = "text-2xl font-semibold leading-none tracking-tight"  # TITLE
        classes = f"{base} {self.klass}" if self.klass else base
        return html_block(h3(self.text, klass=classes))
