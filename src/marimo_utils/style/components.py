from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from marimo_utils.style._mohtml import div, p, path, rect, span, svg
from marimo_utils.style.css import css
from marimo_utils.style.protocols import HtmlRenderable
from marimo_utils.style.settings import (
    ColorPalette,
    IconStyle,
    LayoutToken,
    PaletteToneName,
    SpacingScale,
    Typography,
)


class MetaStamp(BaseModel):
    model_config = ConfigDict(frozen=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    icon_style: IconStyle = Field(default_factory=IconStyle.default)
    display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [
            LayoutToken.INLINE_FLEX,
            LayoutToken.ALIGN_CENTER,
        ]
    )

    def icon(self) -> HtmlRenderable:
        raise NotImplementedError("MetaStamp subclasses must implement icon().")

    def text(self) -> str:
        raise NotImplementedError("MetaStamp subclasses must implement text().")

    def render(self) -> HtmlRenderable:
        return div(
            self.icon(),
            span(
                self.text(),
                style=css(self.typography.meta.css(color=self.palette.text_subtle)),
            ),
            style=css(
                LayoutToken.css(self.display_styles),
                margin_top=self.spacing.sm,
                gap=self.spacing.sm,
            ),
        )


class DateStamp(MetaStamp):
    value: datetime | None

    def icon(self) -> HtmlRenderable:
        return svg(
            path(d="M8 2v4"),
            path(d="M16 2v4"),
            rect(width="18", height="18", x="3", y="4", rx="2"),
            path(d="M3 10h18"),
            **self.icon_style.svg_kwargs(),
            style=css(self.icon_style.css(color=self.palette.text_subtle)),
        )

    def text(self) -> str:
        if self.value is None:
            return "--- --"
        return self.value.strftime("%b %d")


class ProjectStamp(MetaStamp):
    project_name: str

    def icon(self) -> HtmlRenderable:
        return svg(
            path(
                d=(
                    "M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9"
                    "L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"
                )
            ),
            **self.icon_style.svg_kwargs(),
            style=css(self.icon_style.css(color=self.palette.text_subtle)),
        )

    def text(self) -> str:
        return self.project_name


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    label: str
    tone: PaletteToneName = PaletteToneName.INFO
    border_radius: str = "999px"
    border_type: str = "border: 1px solid"
    display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [LayoutToken.INLINE_BLOCK, LayoutToken.NOWRAP]
    )

    def render(self) -> HtmlRenderable:
        tone = self.palette.tone(self.tone)
        return span(
            self.label,
            style=css(
                LayoutToken.css(self.display_styles),
                f"{self.border_type} {tone.border}",
                self.typography.badge.css(color=tone.text),
                padding=f"{self.spacing.xs} {self.spacing.md}",
                border_radius=self.border_radius,
                background=tone.bg,
            ),
        )


class DataItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    label: str
    value: str
    value_tone: PaletteToneName | None = None
    label_min_width: str = "7rem"
    label_display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [LayoutToken.INLINE_BLOCK]
    )

    def value_color(self) -> str:
        if self.value_tone is None:
            return self.palette.text_primary
        return self.palette.tone(self.value_tone).text

    def render(self) -> HtmlRenderable:
        return div(
            span(
                self.label,
                style=css(
                    LayoutToken.css(self.label_display_styles),
                    self.typography.label.css(color=self.palette.text_muted),
                    min_width=self.label_min_width,
                ),
            ),
            span(
                self.value,
                style=css(self.typography.body.css(color=self.value_color())),
            ),
            style=css(margin_top=self.spacing.md),
        )


class Title(BaseModel):
    model_config = ConfigDict(frozen=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    drop_text: str
    text: str
    drop_text_margin: str = "0"
    text_margin_inline: str = "0"
    text_margin_bottom: str = "0"

    def render(self) -> HtmlRenderable:
        return div(
            p(
                self.drop_text,
                style=css(
                    self.typography.drop_title.css(color=self.palette.text_subtle),
                    margin=self.drop_text_margin,
                ),
            ),
            p(
                self.text,
                style=css(
                    self.typography.title.css(color=self.palette.text_primary),
                    margin=(
                        f"{self.spacing.xxs} "
                        f"{self.text_margin_inline} {self.text_margin_bottom}"
                    ),
                ),
            ),
        )


class LabeledList(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    section_label: str
    items: list[HtmlRenderable | str]
    display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [
            LayoutToken.FLEX,
            LayoutToken.FLEX_WRAP,
            LayoutToken.ALIGN_CENTER,
        ]
    )

    def render(self) -> HtmlRenderable:
        return div(
            span(
                f"{self.section_label}:",
                style=css(self.typography.label.css(color=self.palette.text_muted)),
            ),
            *self.items,
            style=css(
                LayoutToken.css(self.display_styles),
                margin_top=self.spacing.lg,
                gap=self.spacing.sm,
                line_height=self.spacing.line_height_loose,
            ),
        )


__all__ = [
    "Badge",
    "DataItem",
    "DateStamp",
    "LabeledList",
    "MetaStamp",
    "ProjectStamp",
    "Title",
]
