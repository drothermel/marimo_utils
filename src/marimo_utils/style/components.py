from __future__ import annotations

import abc
from datetime import datetime

import marimo as mo
from lucide import lucide_icon
from pydantic import BaseModel, ConfigDict, Field

from marimo_utils.style._active_html import ActiveHtml
from marimo_utils.style._mohtml import div, p, span
from marimo_utils.style._rendering import html_block, rem_to_float
from marimo_utils.style.css import css
from marimo_utils.style.protocols import HtmlRenderable
from marimo_utils.style.settings import LayoutToken, PaletteToneName, Style


class MetaStamp(BaseModel, abc.ABC):
    model_config = ConfigDict(frozen=True)

    style: Style
    icon_name: str
    display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [
            LayoutToken.INLINE_FLEX,
            LayoutToken.ALIGN_CENTER,
        ]
    )

    @abc.abstractmethod
    def text(self) -> str: ...

    def icon(self) -> HtmlRenderable:
        icon_svg = lucide_icon(
            self.icon_name,
            width=self.style.icon_style.width,
            height=self.style.icon_style.height,
            stroke_width=self.style.icon_style.stroke_width,
            stroke="currentColor",
        )
        wrapper_style = css(
            color=self.style.palette.text_subtle,
            flex=self.style.icon_style.flex,
            display="inline-flex",
        )
        return mo.Html(f'<span style="{wrapper_style}">{icon_svg}</span>')

    def render(self) -> mo.Html | ActiveHtml:
        fragment = div(
            self.icon(),
            span(
                self.text(),
                style=css(
                    self.style.typography.meta.css(color=self.style.palette.text_subtle)
                ),
            ),
            style=css(
                LayoutToken.css(self.display_styles),
                margin_top=self.style.spacing.sm,
                gap=self.style.spacing.sm,
            ),
        )
        return html_block(fragment)


class DateStamp(MetaStamp):
    icon_name: str = "calendar"
    value: datetime | None

    def text(self) -> str:
        if self.value is None:
            return "--- --"
        return self.value.strftime("%b %d")


class ProjectStamp(MetaStamp):
    icon_name: str = "folder"
    project_name: str

    def text(self) -> str:
        return self.project_name


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    style: Style
    label: str
    tone: PaletteToneName = PaletteToneName.INFO
    border_radius: str = "999px"
    border_type: str = "1px solid"
    display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [LayoutToken.INLINE_BLOCK, LayoutToken.NOWRAP]
    )

    def render(self) -> mo.Html | ActiveHtml:
        tone = self.style.palette.tone(self.tone)
        fragment = span(
            self.label,
            style=css(
                LayoutToken.css(self.display_styles),
                self.style.typography.badge.css(color=tone.text),
                padding=f"{self.style.spacing.xs} {self.style.spacing.md}",
                border_radius=self.border_radius,
                background=tone.bg,
                border=f"{self.border_type} {tone.border}",
            ),
        )
        return html_block(fragment)


class DataItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    style: Style
    label: str
    value: str
    value_tone: PaletteToneName | None = None
    label_min_width: str = "7rem"
    label_display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [LayoutToken.INLINE_BLOCK]
    )

    def value_color(self) -> str:
        if self.value_tone is None:
            return self.style.palette.text_primary
        return self.style.palette.tone(self.value_tone).text

    def render(self) -> mo.Html | ActiveHtml:
        fragment = div(
            span(
                self.label,
                style=css(
                    LayoutToken.css(self.label_display_styles),
                    self.style.typography.label.css(
                        color=self.style.palette.text_muted
                    ),
                    min_width=self.label_min_width,
                ),
            ),
            span(
                self.value,
                style=css(self.style.typography.body.css(color=self.value_color())),
            ),
            style=css(margin_top=self.style.spacing.md),
        )
        return html_block(fragment)


class Title(BaseModel):
    model_config = ConfigDict(frozen=True)

    style: Style
    drop_text: str
    text: str
    drop_text_margin: str = "0"
    text_margin_inline: str = "0"
    text_margin_bottom: str = "0"

    def render(self) -> mo.Html | ActiveHtml:
        fragment = div(
            p(
                self.drop_text,
                style=css(
                    self.style.typography.drop_title.css(
                        color=self.style.palette.text_subtle
                    ),
                    margin=self.drop_text_margin,
                ),
            ),
            p(
                self.text,
                style=css(
                    self.style.typography.title.css(
                        color=self.style.palette.text_primary
                    ),
                    margin=(
                        f"{self.style.spacing.xxs} "
                        f"{self.text_margin_inline} {self.text_margin_bottom}"
                    ),
                ),
            ),
        )
        return html_block(fragment)


class LabeledList(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    style: Style
    section_label: str
    items: list[object | str]
    display_styles: list[LayoutToken] = Field(
        default_factory=lambda: [
            LayoutToken.FLEX,
            LayoutToken.FLEX_WRAP,
            LayoutToken.ALIGN_CENTER,
        ]
    )

    def section_label_item(self) -> mo.Html | ActiveHtml:
        return html_block(
            span(
                f"{self.section_label}:",
                style=css(
                    self.style.typography.label.css(color=self.style.palette.text_muted)
                ),
            )
        )

    def rendered_items(self) -> list[object]:
        rendered: list[object] = []
        for item in self.items:
            if isinstance(item, str):
                rendered.append(
                    html_block(
                        span(
                            item,
                            style=css(
                                self.style.typography.body.css(
                                    color=self.style.palette.text_primary
                                )
                            ),
                        )
                    )
                )
                continue
            rendered.append(item)
        return rendered

    def render(self) -> mo.Html:
        return mo.style(
            mo.hstack(
                [self.section_label_item(), *self.rendered_items()],
                justify="start",
                align="center",
                wrap=True,
                gap=rem_to_float(self.style.spacing.sm),
            ),
            margin_top=self.style.spacing.lg,
            line_height=self.style.spacing.line_height_loose,
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
