from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

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
    height: str | None = None
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
        constrained = self.height is not None

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
            content_fragment = as_html(self.content)
            if constrained:
                content_fragment = div(
                    content_fragment,
                    style=css(
                        flex="1 1 auto",
                        min_height="0",
                        display="flex",
                        flex_direction="column",
                    ),
                )
            sections.append(content_fragment)

        return html_block(
            div(
                *sections,
                style=css(
                    font_family=self.style.typography.font_family,
                    color=self.style.palette.text_primary,
                    width=self.width,
                    height=self.height,
                    display="flex" if constrained else None,
                    flex_direction="column" if constrained else None,
                    box_sizing="border-box" if constrained else None,
                    padding=f"{self.style.spacing.xl} {self.style.spacing.xxl}",
                    border_radius=self.border_radius,
                    border=(f"{self.border_type} {self.style.palette.surface_border}"),
                    background=self.style.palette.surface_background,
                    box_shadow=self.style.palette.surface_shadow,
                ),
            )
        )


__all__ = ["Card"]
