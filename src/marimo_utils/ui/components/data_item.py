from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import div, span  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui._rendering import html_block


class DataItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        container = "flex items-baseline gap-3"
        if self.klass:
            container = f"{container} {self.klass}"
        return html_block(
            div(
                span(
                    self.label,
                    klass=(
                        "inline-block min-w-28 text-xs font-medium "
                        "uppercase tracking-wide text-muted-foreground"
                    ),
                ),
                span(
                    self.value,
                    klass="text-sm font-semibold text-foreground",
                ),
                klass=container,
            )
        )
