from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.core.drhtml import cn, div, html_block
from marimo_utils.ui.styles import (
    BADGE_FOCUS,
    BORDER,
    BadgeVariant,
    DivLayouts,
    Padding,
    Typography,
)

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    variant: BadgeVariant = BadgeVariant.DEFAULT
    klass: str | None = None

    def _class_name(self) -> str:
        return cn(
            DivLayouts.INLINE_ROW,
            BORDER,
            BADGE_FOCUS,
            Padding.BADGE,
            Typography.BODY_SEMIBOLD,
            self.variant,
            self.klass,
        )

    def to_html(self) -> str:
        return str(
            div(
                self.label,
                klass=self._class_name(),
                data_component="badge",
            )
        )

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                self.label,
                klass=self._class_name(),
            )
        )
