from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go

from marimo_utils.style.charts._base import PlotlyChart
from marimo_utils.style.settings import PaletteToneName

HistNorm = Literal["", "percent", "probability", "density", "probability density"]


class HistogramChart(PlotlyChart):
    """1-D distribution histogram with a single palette tone.

    Raw values go in; plotly handles binning via ``nbins`` or ``bin_size``.
    """

    values: list[float]
    tone: PaletteToneName = PaletteToneName.INFO
    color: str | None = None
    nbins: int | None = None
    bin_size: float | None = None
    histnorm: HistNorm = ""
    orientation: Literal["v", "h"] = "v"
    height: int | None = 220
    stroke_color: str = "#f8fafc"
    stroke_width: int = 1

    def resolved_color(self) -> str:
        if self.color is not None:
            return self.color
        return self.style.palette.tone(self.tone).border

    def empty_state_html(self) -> str:
        return (
            '<div style="opacity: 0.6; font-style: italic;">'
            "No values to histogram."
            "</div>"
        )

    def _has_data(self) -> bool:
        return len(self.values) > 0

    def _build_figure(self) -> go.Figure:
        marker = {
            "color": self.resolved_color(),
            "line": {
                "color": self.stroke_color,
                "width": self.stroke_width,
            },
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
        fig.update_layout(**self.style.plotly_layout())
        fig.update_layout(bargap=0.05)
        self._apply_dimensions(fig)
        return fig


__all__ = ["HistNorm", "HistogramChart"]
