from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime  # noqa: TC003
from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.components.lucide_icon import LucideIcon
from marimo_utils.ui.drhtml import cn, div, html_block, span
from marimo_utils.ui.styles import DivLayouts, Typography

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class StampKind(StrEnum):
    DATE = "date"
    PROJECT = "project"


@dataclass(frozen=True)
class StampPreset:
    icon_name: str
    empty_text: str = "---"


STAMP_PRESETS: dict[StampKind, StampPreset] = {}


def register_stamp(
    kind: StampKind,
    *,
    icon_name: str,
    empty_text: str = "---",
):
    """Register a stamp preset and attach it to a builder at import time."""

    def decorator(fn):
        STAMP_PRESETS[kind] = StampPreset(icon_name=icon_name, empty_text=empty_text)
        return fn

    return decorator


class Stamp(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: str | None = None
    icon_name: str = "folder"
    empty_text: str = "---"
    allow_empty: bool = True
    spacing: str = "gap-1"
    klass: str | None = None

    def _display_text(self) -> str:
        missing = self.value is None or self.value.strip() == ""
        if missing:
            if not self.allow_empty:
                raise ValueError("Stamp value is required")
            return self.empty_text
        assert self.value is not None
        return self.value

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                LucideIcon(name=self.icon_name).render(),
                span(self._display_text(), klass=Typography.BODY_MUTED),
                klass=cn(DivLayouts.INLINE_ROW, self.spacing, self.klass),
            )
        )


def _stamp_from_preset(
    kind: StampKind,
    value: str | None,
    *,
    icon_name: str | None = None,
    empty_text: str | None = None,
    allow_empty: bool = True,
    spacing: str = "gap-1",
    klass: str | None = None,
) -> Stamp:
    preset = STAMP_PRESETS[kind]
    return Stamp(
        value=value,
        icon_name=preset.icon_name if icon_name is None else icon_name,
        empty_text=preset.empty_text if empty_text is None else empty_text,
        allow_empty=allow_empty,
        spacing=spacing,
        klass=klass,
    )


@register_stamp(StampKind.DATE, icon_name="calendar")
def date_stamp(
    value: datetime | None = None,
    *,
    icon_name: str | None = None,
    empty_text: str | None = None,
    allow_empty: bool = True,
    spacing: str = "gap-1",
    klass: str | None = None,
) -> Stamp:
    text = None if value is None else value.strftime("%b %d")
    return _stamp_from_preset(
        StampKind.DATE,
        text,
        icon_name=icon_name,
        empty_text=empty_text,
        allow_empty=allow_empty,
        spacing=spacing,
        klass=klass,
    )


@register_stamp(StampKind.PROJECT, icon_name="folder")
def project_stamp(
    project_name: str | None = None,
    *,
    icon_name: str | None = None,
    empty_text: str | None = None,
    allow_empty: bool = True,
    spacing: str = "gap-1",
    klass: str | None = None,
) -> Stamp:
    return _stamp_from_preset(
        StampKind.PROJECT,
        project_name,
        icon_name=icon_name,
        empty_text=empty_text,
        allow_empty=allow_empty,
        spacing=spacing,
        klass=klass,
    )
