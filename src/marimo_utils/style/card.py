from __future__ import annotations

import marimo as mo
from pydantic import BaseModel, ConfigDict

from marimo_utils.style.settings import ColorPalette, SpacingScale, Typography


class Card(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    title: object | None = None
    header: object | None = None
    content: object | None = None
    width: str = "18rem"
    border_radius: str = "16px"
    border_type: str = "1px solid"
    divider_border_type: str = "1px solid"

    def divider(self) -> mo.Html:
        return mo.style(
            mo.Html("<div></div>"),
            margin_top=self.spacing.lg,
            padding_top=self.spacing.sm,
            border_top=f"{self.divider_border_type} {self.palette.surface_border}",
        )

    def render(self) -> mo.Html:
        top_sections: list[object] = []
        if self.title is not None:
            top_sections.append(self.title)
        if self.header is not None:
            top_sections.append(self.header)

        sections: list[object] = [*top_sections]
        if top_sections and self.content is not None:
            sections.append(self.divider())
        if self.content is not None:
            sections.append(self.content)

        return mo.style(
            mo.vstack(sections, gap=0),
            font_family=self.typography.font_family,
            color=self.palette.text_primary,
            width=self.width,
            padding=f"{self.spacing.xl} {self.spacing.xxl}",
            border_radius=self.border_radius,
            border=f"{self.border_type} {self.palette.surface_border}",
            background=self.palette.surface_background,
            box_shadow=self.palette.surface_shadow,
        )


__all__ = ["Card"]
