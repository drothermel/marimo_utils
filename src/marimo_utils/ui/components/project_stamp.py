from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.components.lucide_icon import LucideIcon
from marimo_utils.ui.drhtml import cn, div, html_block, span
from marimo_utils.ui.styles import DivLayouts, Typography

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class ProjectStamp(BaseModel):
    model_config = ConfigDict(frozen=True)

    project_name: str
    icon_name: str = "folder"
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                LucideIcon(name=self.icon_name).render(),
                span(self.project_name, klass=Typography.BODY_MUTED),
                klass=cn(DivLayouts.INLINE_ROW, "gap-1", self.klass),
            )
        )
