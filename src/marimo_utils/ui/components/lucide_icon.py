from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from lucide import lucide_icon  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.drhtml import html_block, span


class LucideIcon(BaseModel):
    """Lucide icon rendered as an SVG inside an `inline-flex` span.

    `size` carries Tailwind height/width utilities (default `h-4 w-4`); the
    SVG fills the span at `100%` so resizing is driven by the utility class,
    not pixel attributes. `stroke="currentColor"` makes the icon color
    inherit from any `text-*` utility on an ancestor — a Badge tone, a
    muted meta row, etc. — without an explicit color prop here.

    Designed as the standalone primitive that other icon-bearing components
    (`DateStamp`, `ProjectStamp`, future icon-aware Badges) compose.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    size: str = "h-4 w-4"
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        svg = lucide_icon(
            self.name,
            width="100%",
            height="100%",
            stroke_width="2",
            stroke="currentColor",
        )
        wrapper = f"inline-flex flex-shrink-0 {self.size}"
        if self.klass:
            wrapper = f"{wrapper} {self.klass}"
        return html_block(span(svg, klass=wrapper))
