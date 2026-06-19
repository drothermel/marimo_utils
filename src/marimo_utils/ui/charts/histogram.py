from __future__ import annotations

import math
from collections.abc import Sequence  # noqa: TC003
from typing import TYPE_CHECKING, Literal

import marimo as mo
import pandas as pd
import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.card import Card
from marimo_utils.ui.chart_colors import CHART_HEX, ChartColor
from marimo_utils.ui.charts._base import PlotlyChart

if TYPE_CHECKING:
    from dr_widget.inline import ActiveHtml

HistNorm = Literal["", "percent", "probability", "density", "probability density"]
Binning = Literal["auto", "integer", "continuous"]


def _is_integer_valued(values: Sequence[float]) -> bool:
    for v in values:
        if v is None:
            continue
        if isinstance(v, float) and math.isnan(v):
            continue
        if not float(v).is_integer():
            return False
    return True


class HistogramChart(PlotlyChart):
    """1-D distribution histogram in a single chart-palette color.

    Raw values go in; plotly handles binning via `nbins` / `bin_size`, or
    — when `binning="integer"` — unit-width bars centered on integer
    ticks. `binning="auto"` (default) picks `"integer"` when the values
    are integer-valued *and* their range fits within `max_integer_bars`;
    otherwise `"continuous"`. `log_y` applies a log scale to the count
    axis (x when `orientation="h"`).
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
    x_range: tuple[float, float] | None = None
    log_y: bool = False
    binning: Binning = "auto"
    max_integer_bars: int = 10

    def empty_state_html(self) -> str:
        return self._empty_state_html("No values to histogram.")

    def _has_data(self) -> bool:
        return len(self.values) > 0

    def _resolve_binning(self) -> Binning:
        if self.binning != "auto":
            return self.binning
        if not self.values or not _is_integer_valued(self.values):
            return "continuous"
        lo = min(self.values)
        hi = max(self.values)
        bucket_count = int(hi - lo) + 1
        if bucket_count > self.max_integer_bars:
            return "continuous"
        # Density gate: if integer mode would produce more buckets than data
        # points, the histogram becomes sparse unit bars — continuous binning
        # packs the same data into fewer, better-filled bars.
        if bucket_count > len(self.values):
            return "continuous"
        return "integer"

    def _integer_bins(self) -> dict[str, float]:
        lo = min(self.values)
        hi = max(self.values)
        return {
            "start": math.floor(lo) - 0.5,
            "end": math.ceil(hi) + 0.5,
            "size": 1,
        }

    def _build_figure(self) -> go.Figure:
        marker = {
            "color": CHART_HEX[self.color],
            "line": {"color": self.stroke_color, "width": self.stroke_width},
        }
        resolved = self._resolve_binning()
        axis_kwarg: dict[str, object] = {}
        if self.orientation == "v":
            axis_kwarg["x"] = self.values
        else:
            axis_kwarg["y"] = self.values
            axis_kwarg["orientation"] = "h"

        if resolved == "integer":
            int_bins = self._integer_bins()
            xbins = int_bins if self.orientation == "v" else None
            ybins = int_bins if self.orientation == "h" else None
            nbinsx = None
            nbinsy = None
        else:
            xbins = (
                {"size": self.bin_size}
                if self.bin_size is not None and self.orientation == "v"
                else None
            )
            ybins = (
                {"size": self.bin_size}
                if self.bin_size is not None and self.orientation == "h"
                else None
            )
            nbinsx = self.nbins if self.orientation == "v" else None
            nbinsy = self.nbins if self.orientation == "h" else None

        hist = go.Histogram(
            marker=marker,
            nbinsx=nbinsx,
            nbinsy=nbinsy,
            xbins=xbins,
            ybins=ybins,
            histnorm=self.histnorm,
            **axis_kwarg,
        )
        fig = go.Figure(data=[hist])
        # Histogram is the one chart with a genuinely numeric x-axis, so
        # it's also the one that threads `x_range` through to the layout.
        fig.update_layout(**self._layout(x_range=self.x_range))
        fig.update_layout(bargap=0.05)
        if resolved == "integer":
            value_axis = "xaxis" if self.orientation == "v" else "yaxis"
            fig.update_layout({value_axis: {"dtick": 1}})
        if self.log_y:
            # `log_y` names the count axis: y when vertical bars, x when horizontal.
            count_axis = "yaxis" if self.orientation == "v" else "xaxis"
            fig.update_layout({count_axis: {"type": "log"}})
        self._apply_dimensions(fig)
        return fig


class HistogramCard(BaseModel):
    """Card-wrapped `HistogramChart` for one column of data.

    Accepts a `pd.DataFrame` (picked via `column`), a `pd.Series`, or any
    `Sequence[float]`. `binning="auto"` picks integer-centered unit bars
    for narrow integer ranges and falls back to `nbins`-driven continuous
    bins otherwise; pass `binning="integer"` or `"continuous"` to force.
    `log_y` applies log scale to the count axis.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    column: str
    data: pd.DataFrame | pd.Series | Sequence[float]
    label: str | None = None
    title: str | None = None
    description: str | None = None
    color: ChartColor = ChartColor.ONE
    binning: Binning = "auto"
    nbins: int | None = None
    bin_size: float | None = None
    max_integer_bars: int = 10
    log_y: bool = False
    value_scale: float = 1.0
    x_range: tuple[float, float] | None = None
    orientation: Literal["v", "h"] = "v"
    tick_format: str | None = None
    x_label: str | None = None
    y_label: str | None = None
    height: int = 220
    width: str = "w-80"

    def _series(self) -> pd.Series:
        if isinstance(self.data, pd.DataFrame):
            raw = self.data[self.column]
        elif isinstance(self.data, pd.Series):
            raw = self.data
        else:
            raw = pd.Series(list(self.data))
        series = pd.to_numeric(raw, errors="coerce").dropna()
        if self.value_scale != 1.0:
            series = series * self.value_scale
        return series

    def render(self) -> mo.Html | ActiveHtml:
        series = self._series()
        if series.empty:
            content: object = mo.md("_No numeric data to display._")
        else:
            x_tick = self.tick_format if self.orientation == "v" else None
            y_tick = self.tick_format if self.orientation == "h" else None
            content = HistogramChart(
                values=[float(v) for v in series.tolist()],
                color=self.color,
                nbins=self.nbins,
                bin_size=self.bin_size,
                binning=self.binning,
                max_integer_bars=self.max_integer_bars,
                log_y=self.log_y,
                orientation=self.orientation,
                height=self.height,
                x_range=self.x_range,
                show_legend=False,
                x_label=self.x_label,
                y_label=self.y_label,
                x_tick_format=x_tick,
                y_tick_format=y_tick,
            )
        return Card(
            title=self.title,
            description=self.description,
            content=content,
            width=self.width,
        ).render()
