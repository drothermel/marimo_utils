from __future__ import annotations

import marimo as mo
from pydantic import BaseModel, ConfigDict

from marimo_utils.style._active_html import ActiveHtml
from marimo_utils.style._mohtml import div
from marimo_utils.style._rendering import as_html, html_block
from marimo_utils.style.components import Title
from marimo_utils.style.css import css
from marimo_utils.style.protocols import HtmlRenderable
from marimo_utils.style.settings import Style


class Card(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    style: Style
    title: Title | HtmlRenderable | None = None
    header: HtmlRenderable | None = None
    content: object | None = None
    width: str = "18rem"
    border_radius: str = "16px"
    border_type: str = "1px solid"
    divider_border_type: str = "1px solid"

    def divider(self) -> HtmlRenderable:
        return div(
            style=css(
                margin_top=self.style.spacing.lg,
                padding_top=self.style.spacing.sm,
                border_top=(
                    f"{self.divider_border_type} {self.style.palette.surface_border}"
                ),
            ),
        )

    def render(self) -> mo.Html | ActiveHtml:
        sections: list[HtmlRenderable] = []
        if self.title is not None:
            sections.append(
                self.title.render() if isinstance(self.title, Title) else self.title
            )
        if self.header is not None:
            sections.append(self.header)
        if sections and self.content is not None:
            sections.append(self.divider())
        if self.content is not None:
            sections.append(as_html(self.content))

        return html_block(
            div(
                *sections,
                style=css(
                    font_family=self.style.typography.font_family,
                    color=self.style.palette.text_primary,
                    width=self.width,
                    padding=f"{self.style.spacing.xl} {self.style.spacing.xxl}",
                    border_radius=self.border_radius,
                    border=(f"{self.border_type} {self.style.palette.surface_border}"),
                    background=self.style.palette.surface_background,
                    box_shadow=self.style.palette.surface_shadow,
                ),
            )
        )


__all__ = ["Card"]
