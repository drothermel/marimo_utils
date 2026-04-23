from __future__ import annotations

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.chart_colors import CHART_COLORWAY, CHART_HEX, ChartColor
from marimo_utils.ui.charts._base import PlotlyChart


class ScatterSeries(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    x: list[float]
    y: list[float]
    color: ChartColor | None = None


class ScatterChart(PlotlyChart):
    """Multi-series scatter plot — one trace per `ScatterSeries`.

    Series without an explicit `color` cycle through `CHART_COLORWAY` by
    index. Both axes are genuinely numeric, so `x_range` is accepted here
    (paralleling `HistogramChart`) and threaded into the layout.
    """

    series: list[ScatterSeries]
    marker_size: int = 8
    stroke_color: str = "#ffffff"
    stroke_width: int = 1
    height: int | None = 260
    x_range: tuple[float, float] | None = None

    def _color_for_series(self, series: ScatterSeries, index: int) -> str:
        if series.color is not None:
            return CHART_HEX[series.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def empty_state_html(self) -> str:
        return (
            '<div class="text-sm italic text-muted-foreground">'
            "No scatter series available."
            "</div>"
        )

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
                    mode="markers",
                    name=series.label,
                    marker={
                        "color": color,
                        "size": self.marker_size,
                        "line": {
                            "color": self.stroke_color,
                            "width": self.stroke_width,
                        },
                    },
                )
            )

        fig = go.Figure(data=traces)
        fig.update_layout(**self._layout(x_range=self.x_range))
        self._apply_dimensions(fig)
        return fig


__all__ = ["ScatterChart", "ScatterSeries"]
