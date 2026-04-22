from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from marimo_utils.style._mohtml import div
from marimo_utils.style.components import Title
from marimo_utils.style.css import css
from marimo_utils.style.protocols import HtmlRenderable
from marimo_utils.style.settings import ColorPalette, SpacingScale, Typography


class Card(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    title: Title | None = None
    header: HtmlRenderable | None = None
    content: HtmlRenderable | None = None
    width: str = "18rem"
    border_radius: str = "16px"
    border_type: str = "1px solid"
    divider_border_type: str = "1px solid"

    def divider(self) -> HtmlRenderable:
        return div(
            style=css(
                margin_top=self.spacing.lg,
                padding_top=self.spacing.sm,
                border_top=f"{self.divider_border_type} {self.palette.surface_border}",
            ),
        )

    def render(self) -> HtmlRenderable:
        top_sections: list[HtmlRenderable] = []
        if self.title is not None:
            top_sections.append(self.title.render())
        if self.header is not None:
            top_sections.append(self.header)

        sections: list[HtmlRenderable] = [*top_sections]
        if top_sections and self.content is not None:
            sections.append(self.divider())
        if self.content is not None:
            sections.append(self.content)

        return div(
            *sections,
            style=css(
                font_family=self.typography.font_family,
                color=self.palette.text_primary,
                width=self.width,
                padding=f"{self.spacing.xl} {self.spacing.xxl}",
                border_radius=self.border_radius,
                border=f"{self.border_type} {self.palette.surface_border}",
                background=self.palette.surface_background,
                box_shadow=self.palette.surface_shadow,
            ),
        )


__all__ = ["Card"]
