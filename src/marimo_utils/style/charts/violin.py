from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict

from marimo_utils.style.charts._base import PlotlyChart
from marimo_utils.style.settings import PaletteToneName

ViolinPoints = Literal["all", "outliers", "suspectedoutliers", False]


class ViolinGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    values: list[float]
    tone: PaletteToneName = PaletteToneName.INFO
    color: str | None = None


class ViolinChart(PlotlyChart):
    """Grouped violin plot — one trace per ``ViolinGroup`` so each group gets its own tone."""  # noqa: E501

    groups: list[ViolinGroup]
    show_box: bool = True
    show_meanline: bool = False
    points: ViolinPoints = "outliers"
    orientation: Literal["v", "h"] = "v"
    height: int | None = 260

    def color_for_group(self, group: ViolinGroup) -> str:
        if group.color is not None:
            return group.color
        return self.style.palette.tone(group.tone).border

    def empty_state_html(self) -> str:
        return (
            '<div style="opacity: 0.6; font-style: italic;">'
            "No violin groups available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return any(len(group.values) > 0 for group in self.groups)

    def _build_figure(self) -> go.Figure:
        traces: list[go.Violin] = []
        for group in self.groups:
            if not group.values:
                continue
            color = self.color_for_group(group)
            shared: dict[str, object] = {
                "name": group.label,
                "box_visible": self.show_box,
                "meanline_visible": self.show_meanline,
                "points": self.points,
                "line_color": color,
                "fillcolor": color,
                "opacity": 0.55,
            }
            if self.orientation == "v":
                shared["y"] = group.values
            else:
                shared["x"] = group.values
                shared["orientation"] = "h"
            traces.append(go.Violin(**shared))

        fig = go.Figure(data=traces)
        fig.update_layout(**self.style.plotly_layout())
        fig.update_layout(
            violinmode="group",
            showlegend=len(traces) > 1,
        )
        self._apply_dimensions(fig)
        return fig


__all__ = ["ViolinChart", "ViolinGroup", "ViolinPoints"]
