from __future__ import annotations

import random
from collections.abc import Sequence  # noqa: TC003
from typing import TYPE_CHECKING, Literal

import marimo as mo
import pandas as pd
import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.charts._base import PlotlyChart
from marimo_utils.ui.charts.colors import (
    CHART_COLORWAY,
    CHART_HEX,
    ChartColor,
    filled_trace_colors,
)
from marimo_utils.ui.charts.quantiles import QuantileFences  # noqa: TC001
from marimo_utils.ui.components.card import Card

if TYPE_CHECKING:
    from dr_widget.inline import ActiveHtml

ViolinPoints = Literal["all", "outliers", "suspectedoutliers", False]
ViolinSpanmode = Literal["soft", "hard"]
ViolinSide = Literal["both", "positive", "negative"]


class ViolinGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    values: list[float]
    color: ChartColor | None = None


class ViolinChart(PlotlyChart):
    """Grouped violin plot — one trace per `ViolinGroup` so each gets its own color.

    Groups without an explicit `color` cycle through `CHART_COLORWAY` by
    index. For large datasets, set `max_samples` to downsample each group
    in Python before the trace is serialized — Plotly's violin trace
    otherwise ships every point to the browser and computes the KDE
    client-side, so payload and render time both scale with raw N.

    Tail-legibility knobs: `spanmode="hard"` clips the KDE at the data
    range (vs. the default soft smoothing which can smear a latency
    distribution into negative territory); `bandwidth` overrides the KDE
    bandwidth; `jitter` spreads overlaid points when `points != False`;
    `side` supports half-violins.
    """

    groups: list[ViolinGroup]
    show_box: bool = True
    show_meanline: bool = False
    points: ViolinPoints = "outliers"
    orientation: Literal["v", "h"] = "v"
    height: int | None = 260
    max_samples: int | None = None
    sample_seed: int = 0
    spanmode: ViolinSpanmode = "soft"
    bandwidth: float | None = None
    jitter: float | None = None
    side: ViolinSide = "both"

    def _color_for_group(self, group: ViolinGroup, index: int) -> str:
        if group.color is not None:
            return CHART_HEX[group.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def empty_state_html(self) -> str:
        return self._empty_state_html("No violin groups available.")

    def _has_data(self) -> bool:
        return any(len(group.values) > 0 for group in self.groups)

    def _subsample(self, values: list[float], index: int) -> list[float]:
        # Seed offset by group index so groups don't correlate but the
        # render is reproducible across reruns.
        if self.max_samples is None or len(values) <= self.max_samples:
            return values
        rng = random.Random(self.sample_seed + index)  # noqa: S311
        return rng.sample(values, self.max_samples)

    def _build_figure(self) -> go.Figure:
        traces: list[go.Violin] = []
        for i, group in enumerate(self.groups):
            if not group.values:
                continue
            values = self._subsample(group.values, i)
            color = self._color_for_group(group, i)
            shared: dict[str, object] = {
                "name": group.label,
                "box_visible": self.show_box,
                "meanline_visible": self.show_meanline,
                "points": self.points,
                "spanmode": self.spanmode,
                "side": self.side,
                **filled_trace_colors(color),
            }
            if self.bandwidth is not None:
                shared["bandwidth"] = self.bandwidth
            if self.jitter is not None:
                shared["jitter"] = self.jitter
            category = [group.label] * len(values)
            if self.orientation == "v":
                shared["y"] = values
                shared["x"] = category
            else:
                shared["x"] = values
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


class ViolinPlotCard(BaseModel):
    """Card-wrapped `ViolinChart` for one column of data.

    Accepts a `pd.DataFrame` (picked via `column`), a `pd.Series`, or any
    `Sequence[float]`. Unlike `BoxPlotCard`, violins require the raw
    values for the KDE, so the efficiency knob is `max_samples` —
    downsamples before the trace is serialized. `spanmode="hard"` clips
    the KDE at the data range, which avoids the "latency smeared into
    negative territory" failure mode on positive-only distributions.

    `clip_fences` drops values outside the given quantile range *before*
    sampling, so the violin focuses on the distribution's bulk instead
    of being stretched by extreme outliers. Note that clipping re-fits
    the KDE on the remaining data — it changes the density's shape near
    the clip boundary, not just its support. For p1/p99 this is usually
    imperceptible; at p10/p90 the shoulders visibly bulge. Pairs
    naturally with an unclipped `BoxPlotCard` next to it: the box's
    whiskers mark the clip region, the violin shows fine shape inside.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    column: str
    data: pd.DataFrame | pd.Series | Sequence[float]
    label: str | None = None
    title: str | None = None
    description: str | None = None
    orientation: Literal["v", "h"] = "v"
    color: ChartColor | None = None
    show_box: bool = True
    show_meanline: bool = True
    points: ViolinPoints = False
    spanmode: ViolinSpanmode = "hard"
    clip_fences: QuantileFences | None = None
    max_samples: int | None = 2000
    sample_seed: int = 0
    bandwidth: float | None = None
    jitter: float | None = None
    side: ViolinSide = "both"
    value_scale: float = 1.0
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

    def _clip(self, series: pd.Series) -> pd.Series:
        if self.clip_fences is None:
            return series
        lower, upper = self.clip_fences.value
        lo = float(series.quantile(float(lower)))
        hi = float(series.quantile(float(upper)))
        return series[(series >= lo) & (series <= hi)]

    def render(self) -> mo.Html | ActiveHtml:
        series = self._clip(self._series())
        if series.empty:
            content: object = mo.md("_No numeric data to display._")
        else:
            x_tick = self.tick_format if self.orientation == "h" else None
            y_tick = self.tick_format if self.orientation == "v" else None
            content = ViolinChart(
                groups=[
                    ViolinGroup(
                        label=self.label if self.label is not None else self.column,
                        values=series.tolist(),
                        color=self.color,
                    ),
                ],
                show_box=self.show_box,
                show_meanline=self.show_meanline,
                points=self.points,
                spanmode=self.spanmode,
                max_samples=self.max_samples,
                sample_seed=self.sample_seed,
                bandwidth=self.bandwidth,
                jitter=self.jitter,
                side=self.side,
                orientation=self.orientation,
                height=self.height,
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
