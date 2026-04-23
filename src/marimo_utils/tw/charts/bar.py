from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict, computed_field

from marimo_utils.tw.chart_colors import CHART_COLORWAY, CHART_HEX, ChartColor
from marimo_utils.tw.charts._base import SHADCN_PLOTLY_LAYOUT, PlotlyChart


class BarItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: float
    color: ChartColor | None = None


class BarChart(PlotlyChart):
    """Single-series categorical bar chart with per-bar chart-palette colors.

    Bars without an explicit `color` cycle through `CHART_COLORWAY` by
    index. Multi-series / stacked / grouped variants are deferred — use
    one `BarChart` per series.
    """

    items: list[BarItem]
    orientation: Literal["v", "h"] = "v"
    height: int | None = 220
    stroke_color: str = "#ffffff"
    stroke_width: int = 1

    @computed_field
    @property
    def visible_items(self) -> list[BarItem]:
        return list(self.items)

    def _color_for_item(self, item: BarItem, index: int) -> str:
        if item.color is not None:
            return CHART_HEX[item.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def empty_state_html(self) -> str:
        return (
            '<div class="text-sm italic text-muted-foreground">'
            "No bar data available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return bool(self.visible_items)

    def _build_figure(self) -> go.Figure:
        items = self.visible_items
        labels = [item.label for item in items]
        values = [item.value for item in items]
        colors = [self._color_for_item(item, i) for i, item in enumerate(items)]

        marker = {
            "color": colors,
            "line": {"color": self.stroke_color, "width": self.stroke_width},
        }
        if self.orientation == "v":
            bar = go.Bar(x=labels, y=values, marker=marker)
        else:
            bar = go.Bar(x=values, y=labels, orientation="h", marker=marker)

        fig = go.Figure(data=[bar])
        fig.update_layout(**SHADCN_PLOTLY_LAYOUT)
        self._apply_dimensions(fig)
        return fig


__all__ = ["BarChart", "BarItem"]
