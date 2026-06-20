from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.core.drhtml import cn, div, h3, html_block, p
from marimo_utils.ui.core.rendering import auto_render, render_inline
from marimo_utils.ui.styles import BORDER, Background, CardWidth, DivLayouts, Typography

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class CardTitle(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(h3(self.text, klass=cn(Typography.TITLE, self.klass)))


class CardDescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            p(*render_inline(self.text), klass=cn(Typography.BODY, self.klass))
        )


class Card(BaseModel):
    """Shadcn Card on a ``DivLayouts.COL_SHELL`` stack with ``BORDER`` chrome.

    ``title`` and ``description`` are flat string params that compose into a
    ``DivLayouts.COL`` header section when present. ``content`` goes in
    ``DivLayouts.COL`` with ``pt-0`` when a header exists, or full ``COL``
    padding when there is no header.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    title: str | None = None
    description: str | None = None
    content: object | None = None
    width: CardWidth | str = CardWidth.DEFAULT
    klass: str | None = None

    @staticmethod
    def _content_to_html(content: object) -> str:
        to_html_fn = getattr(content, "to_html", None)
        if callable(to_html_fn):
            return str(to_html_fn())
        return str(auto_render(content))

    def to_html(self) -> str:
        # Duplicates layout logic from render() during additive migration; consolidate
        # when render() is retired.
        container_cls = cn(
            DivLayouts.COL_SHELL,
            BORDER,
            Background.CARD,
            Typography.BODY,
            self.width,
            self.klass,
        )

        sections: list[str] = []
        header_children: list[str] = []
        if self.title is not None:
            header_children.append(str(h3(self.title, klass=cn(Typography.TITLE))))
        if self.description is not None:
            header_children.append(
                str(
                    p(
                        *render_inline(self.description),
                        klass=cn(Typography.BODY),
                    )
                )
            )
        if header_children:
            sections.append(str(div(*header_children, klass=DivLayouts.COL)))
        if self.content is not None:
            content_cls = (
                cn(DivLayouts.COL, "pt-0") if header_children else DivLayouts.COL
            )
            sections.append(
                str(
                    div(
                        self._content_to_html(self.content),
                        klass=content_cls,
                    )
                )
            )

        return str(div(*sections, klass=container_cls, data_component="card"))

    def render(self) -> mo.Html | ActiveHtml:
        container_cls = cn(
            DivLayouts.COL_SHELL,
            BORDER,
            Background.CARD,
            Typography.BODY,
            self.width,
            self.klass,
        )

        sections: list[object] = []
        header_children: list[object] = []
        if self.title is not None:
            header_children.append(CardTitle(text=self.title).render())
        if self.description is not None:
            header_children.append(CardDescription(text=self.description).render())
        if header_children:
            sections.append(div(*header_children, klass=DivLayouts.COL))
        if self.content is not None:
            content_cls = (
                cn(DivLayouts.COL, "pt-0") if header_children else DivLayouts.COL
            )
            sections.append(div(auto_render(self.content), klass=content_cls))

        return html_block(div(*sections, klass=container_cls))
