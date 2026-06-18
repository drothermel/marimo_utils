from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import cn, div, html_block, span
from marimo_utils.ui.rendering import auto_render
from marimo_utils.ui.styles import DivLayouts


class LabeledList(BaseModel):
    """Section label prefix + flex-wrapping list of rendered items.

    Label uses shadcn's muted inline-label style (`text-sm font-medium
    text-muted-foreground`) rather than the form-coupled `Label` primitive.
    Items are auto-rendered (any component with `.render()`) or passed
    through for string coercion by drhtml tag builders.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    label: str
    items: list[object]
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        rendered_items = [auto_render(item) for item in self.items]
        return html_block(
            div(
                span(
                    f"{self.label}:",
                    klass="text-sm font-medium text-muted-foreground",
                ),
                *rendered_items,
                klass=cn(DivLayouts.INLINE_ROW, self.klass),
            )
        )
