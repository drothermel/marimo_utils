from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict

from marimo_utils.tw.chart_colors import CHART_COLORWAY, CHART_HEX, ChartColor
from marimo_utils.tw.charts._base import PlotlyChart

ViolinPoints = Literal["all", "outliers", "suspectedoutliers", False]


class ViolinGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    values: list[float]
    color: ChartColor | None = None


class ViolinChart(PlotlyChart):
    """Grouped violin plot — one trace per `ViolinGroup` so each gets its own color.

    Groups without an explicit `color` cycle through `CHART_COLORWAY` by
    index.
    """

    groups: list[ViolinGroup]
    show_box: bool = True
    show_meanline: bool = False
    points: ViolinPoints = "outliers"
    orientation: Literal["v", "h"] = "v"
    height: int | None = 260

    def _color_for_group(self, group: ViolinGroup, index: int) -> str:
        if group.color is not None:
            return CHART_HEX[group.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def empty_state_html(self) -> str:
        return (
            '<div class="text-sm italic text-muted-foreground">'
            "No violin groups available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return any(len(group.values) > 0 for group in self.groups)

    def _build_figure(self) -> go.Figure:
        traces: list[go.Violin] = []
        for i, group in enumerate(self.groups):
            if not group.values:
                continue
            color = self._color_for_group(group, i)
            shared: dict[str, object] = {
                "name": group.label,
                "box_visible": self.show_box,
                "meanline_visible": self.show_meanline,
                "points": self.points,
                "line_color": color,
                "fillcolor": color,
                "opacity": 0.55,
            }
            category = [group.label] * len(group.values)
            if self.orientation == "v":
                shared["y"] = group.values
                shared["x"] = category
            else:
                shared["x"] = group.values
                shared["y"] = category
                shared["orientation"] = "h"
            traces.append(go.Violin(**shared))

        fig = go.Figure(data=traces)
        fig.update_layout(**self._layout())
        # `violinmode="overlay"` (the default) pairs with the categorical x
        # values above so each violin anchors to its own x-tick. With
        # `violinmode="group"`, plotly adds a trace-index offset inside each
        # category and the outer violins drift outward from their labels.
        fig.update_layout(violinmode="overlay")
        self._apply_dimensions(fig)
        return fig


__all__ = ["ViolinChart", "ViolinGroup", "ViolinPoints"]
