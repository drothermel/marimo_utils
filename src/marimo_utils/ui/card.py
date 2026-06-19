from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.components import CardDescription, CardTitle
from marimo_utils.ui.drhtml import cn, div, html_block
from marimo_utils.ui.rendering import auto_render
from marimo_utils.ui.styles import DivLayouts

CARD_SURFACE = (
    "rounded-lg border border-border bg-card shadow-sm"
    "text-sm font-medium text-foreground"  # BODY
)


class Card(BaseModel):
    """Shadcn Card
    ``CARD_SURFACE`` chrome on a ``DivLayouts.COL_SHELL`` stack.

    ``title`` and ``description`` are flat string params that compose into a
    ``DivLayouts.COL`` header section when present. ``content`` goes in
    ``DivLayouts.COL`` with ``pt-0`` when a header exists, or full ``COL``
    padding when there is no header.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    title: str | None = None
    description: str | None = None
    content: object | None = None
    width: str = "w-72"
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        container_cls = cn(
            DivLayouts.COL_SHELL, CARD_SURFACE, self.width, self.klass
        )

        sections: list[object] = []
        header_children: list[object] = []
        if self.title is not None:
            header_children.append(CardTitle(text=self.title).render())
        if self.description is not None:
            header_children.append(
                CardDescription(text=self.description).render()
            )
        if header_children:
            sections.append(div(*header_children, klass=DivLayouts.COL))
        if self.content is not None:
            content_cls = (
                cn(DivLayouts.COL, "pt-0")
                if header_children
                else DivLayouts.COL
            )
            sections.append(div(auto_render(self.content), klass=content_cls))

        return html_block(div(*sections, klass=container_cls))
