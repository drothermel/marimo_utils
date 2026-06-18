from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.components import CardDescription, CardTitle
from marimo_utils.ui.drhtml import div, html_block
from marimo_utils.ui.rendering import auto_render


class Card(BaseModel):
    """Shadcn Card — `rounded-lg border bg-card text-card-foreground shadow-sm`.

    `title` and `description` are flat string params that compose into a
    shadcn-shaped `CardHeader` internally (`flex flex-col space-y-1.5 p-6`).
    Either may be omitted. `content` goes in `CardContent` with `p-6 pt-0`
    when a header is present, or `p-6` when there is no header.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    title: str | None = None
    description: str | None = None
    content: object | None = None
    width: str = "w-72"
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        base = (
            "self-start rounded-lg border border-border "
            "bg-card text-card-foreground shadow-sm"
        )
        container_cls = " ".join(filter(None, [base, self.width, self.klass]))

        sections: list[object] = []
        header_children: list[object] = []
        if self.title is not None:
            header_children.append(CardTitle(text=self.title).render())
        if self.description is not None:
            header_children.append(CardDescription(text=self.description).render())
        if header_children:
            sections.append(
                div(*header_children, klass="flex flex-col space-y-1.5 p-6")
            )
        if self.content is not None:
            content_padding = "p-6 pt-0" if header_children else "p-6"
            sections.append(div(auto_render(self.content), klass=content_padding))

        return html_block(div(*sections, klass=container_cls))
