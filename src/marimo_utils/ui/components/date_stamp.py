from __future__ import annotations

from datetime import datetime

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import div, span  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui._rendering import html_block
from marimo_utils.ui.components.lucide_icon import LucideIcon


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
        container = (
            "self-start inline-flex items-center "
            "gap-2 text-sm text-muted-foreground"
        )
        if self.klass:
            container = f"{container} {self.klass}"
        return html_block(
            div(
                LucideIcon(name=self.icon_name).render(),
                span(self._text()),
                klass=container,
            )
        )
