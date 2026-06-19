from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.chart_colors import CHART_COLORWAY, CHART_HEX, ChartColor
from marimo_utils.ui.charts._base import PlotlyChart

LineDash = Literal["solid", "dot", "dash", "longdash", "dashdot"]


class LineSeries(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    x: list[float]
    y: list[float]
    color: ChartColor | None = None
    dash: LineDash = "solid"


class LineChart(PlotlyChart):
    """Multi-series line chart — one trace per `LineSeries`.

    Series without an explicit `color` cycle through `CHART_COLORWAY` by
    index. `dash` on each series lets callers distinguish paired lines
    (e.g., solid train vs dashed validation). Both axes are numeric, so
    `x_range` is accepted here and threaded into the layout.
    """

    series: list[LineSeries]
    line_width: int = 2
    height: int | None = 260
    x_range: tuple[float, float] | None = None

    def _color_for_series(self, series: LineSeries, index: int) -> str:
        if series.color is not None:
            return CHART_HEX[series.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def empty_state_html(self) -> str:
        return self._empty_state_html("No line series available.")

    def _has_data(self) -> bool:
        return any(len(s.x) > 0 and len(s.x) == len(s.y) for s in self.series)

    def _build_figure(self) -> go.Figure:
        traces: list[go.Scatter] = []
        for i, series in enumerate(self.series):
            if not series.x or len(series.x) != len(series.y):
                continue
            color = self._color_for_series(series, i)
            traces.append(
                go.Scatter(
                    x=series.x,
                    y=series.y,
                    mode="lines",
                    name=series.label,
                    line={
                        "color": color,
                        "width": self.line_width,
                        "dash": series.dash,
                    },
                )
            )

        fig = go.Figure(data=traces)
        fig.update_layout(**self._layout(x_range=self.x_range))
        self._apply_dimensions(fig)
        return fig
