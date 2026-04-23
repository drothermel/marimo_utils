from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go

from marimo_utils.tw.chart_colors import CHART_HEX, ChartColor
from marimo_utils.tw.charts._base import PlotlyChart

HistNorm = Literal["", "percent", "probability", "density", "probability density"]


class HistogramChart(PlotlyChart):
    """1-D distribution histogram in a single chart-palette color.

    Raw values go in; plotly handles binning via `nbins` or `bin_size`.
    Single-color chart — the `color` field is required (defaults to
    `ChartColor.ONE`).
    """

    values: list[float]
    color: ChartColor = ChartColor.ONE
    nbins: int | None = None
    bin_size: float | None = None
    histnorm: HistNorm = ""
    orientation: Literal["v", "h"] = "v"
    height: int | None = 220
    stroke_color: str = "#ffffff"
    stroke_width: int = 1

    def empty_state_html(self) -> str:
        return (
            '<div class="text-sm italic text-muted-foreground">'
            "No values to histogram."
            "</div>"
        )

    def _has_data(self) -> bool:
        return len(self.values) > 0

    def _build_figure(self) -> go.Figure:
        marker = {
            "color": CHART_HEX[self.color],
            "line": {"color": self.stroke_color, "width": self.stroke_width},
        }
        axis_kwarg: dict[str, object] = {}
        if self.orientation == "v":
            axis_kwarg["x"] = self.values
        else:
            axis_kwarg["y"] = self.values
            axis_kwarg["orientation"] = "h"

        hist = go.Histogram(
            marker=marker,
            nbinsx=self.nbins if self.orientation == "v" else None,
            nbinsy=self.nbins if self.orientation == "h" else None,
            xbins=(
                {"size": self.bin_size}
                if self.bin_size is not None and self.orientation == "v"
                else None
            ),
            ybins=(
                {"size": self.bin_size}
                if self.bin_size is not None and self.orientation == "h"
                else None
            ),
            histnorm=self.histnorm,
            **axis_kwarg,
        )
        fig = go.Figure(data=[hist])
        fig.update_layout(**self._layout())
        fig.update_layout(bargap=0.05)
        self._apply_dimensions(fig)
        return fig


__all__ = ["HistNorm", "HistogramChart"]
