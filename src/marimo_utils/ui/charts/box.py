from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

import marimo as mo
import pandas as pd
import plotly.graph_objects as go
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict, model_validator

from marimo_utils.ui.card import Card
from marimo_utils.ui.chart_colors import (
    CHART_COLORWAY,
    CHART_HEX,
    ChartColor,
    filled_trace_colors,
)
from marimo_utils.ui.charts._base import PlotlyChart
from marimo_utils.ui.charts.quantiles import Quantile, QuantileFences

BoxPoints = Literal["all", "outliers", "suspectedoutliers", False]
BoxMean = Literal[True, False, "sd"]


class BoxGroup(BaseModel):
    """A single box in a `BoxChart`, in one of two mutually-exclusive modes.

    Raw mode — pass `values`; Plotly computes quartiles and Tukey whiskers
    client-side. Suitable for small datasets or quick exploration.

    Precomputed mode — pass at least `q1`, `median`, `q3`. Optionally pass
    `lowerfence` / `upperfence` (whisker endpoints); set these to suppress
    Plotly's default 1.5x IQR rule and anchor the whiskers at meaningful
    values like p1/p99 or min/max — critical for heavy-tailed
    distributions where the default rule generates misleading whiskers
    and hundreds of "outlier" markers. `mean` / `sd` are consumed only
    when the parent `BoxChart.boxmean` is truthy.
    """

    model_config = ConfigDict(frozen=True)

    label: str
    color: ChartColor | None = None

    values: list[float] | None = None

    q1: float | None = None
    median: float | None = None
    q3: float | None = None
    lowerfence: float | None = None
    upperfence: float | None = None
    mean: float | None = None
    sd: float | None = None

    @classmethod
    def from_values(
        cls,
        label: str,
        values: Sequence[float],
        *,
        fences: QuantileFences | None = QuantileFences.P1_P99,
        include_mean: bool = True,
        color: ChartColor | None = None,
    ) -> BoxGroup:
        """Build a precomputed-stats `BoxGroup` from raw `values`.

        Computes q1/median/q3 server-side; whiskers land at `fences`
        (default p1/p99) or are left to Plotly's default 1.5x IQR rule
        when `fences=None`. The resulting group ships ~5 floats to the
        browser regardless of input size.
        """
        series = pd.to_numeric(pd.Series(list(values)), errors="coerce").dropna()
        if series.empty:
            raise ValueError(
                f"BoxGroup.from_values({label!r}): no numeric values after dropna."
            )

        def q(level: Quantile | float) -> float:
            return float(series.quantile(float(level)))

        kwargs: dict[str, Any] = {
            "label": label,
            "q1": q(Quantile.P25),
            "median": q(Quantile.P50),
            "q3": q(Quantile.P75),
            "sd": float(series.std(ddof=0)),
        }
        if color is not None:
            kwargs["color"] = color
        if fences is not None:
            lower, upper = fences.value
            kwargs["lowerfence"] = q(lower)
            kwargs["upperfence"] = q(upper)
        if include_mean:
            kwargs["mean"] = float(series.mean())
        return cls(**kwargs)

    @model_validator(mode="after")
    def _validate_exactly_one_mode(self) -> BoxGroup:
        has_values = self.values is not None and len(self.values) > 0
        has_core_stats = (
            self.q1 is not None and self.median is not None and self.q3 is not None
        )
        any_stats = any(
            v is not None
            for v in (
                self.q1,
                self.median,
                self.q3,
                self.lowerfence,
                self.upperfence,
                self.mean,
                self.sd,
            )
        )
        if has_values and any_stats:
            raise ValueError(
                "BoxGroup: provide either `values` (raw mode) or precomputed "
                "stats (`q1`, `median`, `q3` at minimum), not both."
            )
        if not has_values and not has_core_stats:
            raise ValueError(
                "BoxGroup: provide either non-empty `values` or all of "
                "`q1`, `median`, `q3`."
            )
        return self


class BoxChart(PlotlyChart):
    """Grouped box plot — one trace per `BoxGroup` so each gets its own color.

    Groups without an explicit `color` cycle through `CHART_COLORWAY` by
    index. Each group may be in raw-values mode or precomputed-stats
    mode; mixing is allowed.

    Defaults: `points=False` (box is a summary view; opt in to outlier
    markers explicitly), `boxmean=False`. When groups provide custom
    `lowerfence` / `upperfence`, Plotly's automatic 1.5x IQR fence rule is
    suppressed — the whiskers render exactly where you put them.
    """

    groups: list[BoxGroup]
    points: BoxPoints = False
    boxmean: BoxMean = False
    notched: bool = False
    orientation: Literal["v", "h"] = "v"
    height: int | None = 260

    def _color_for_group(self, group: BoxGroup, index: int) -> str:
        if group.color is not None:
            return CHART_HEX[group.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def empty_state_html(self) -> str:
        return (
            '<div class="text-sm italic text-muted-foreground">'
            "No box groups available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return len(self.groups) > 0

    def _build_figure(self) -> go.Figure:
        traces: list[go.Box] = []
        for i, group in enumerate(self.groups):
            color = self._color_for_group(group, i)
            shared: dict[str, object] = {
                "name": group.label,
                "boxpoints": self.points,
                "boxmean": self.boxmean,
                "notched": self.notched,
                **filled_trace_colors(color),
            }
            if group.values is None:
                self._apply_precomputed_stats(shared, group)
                category = [group.label]
                if self.orientation == "v":
                    shared["x"] = category
                else:
                    shared["y"] = category
                    shared["orientation"] = "h"
            else:
                values = group.values
                category = [group.label] * len(values)
                if self.orientation == "v":
                    shared["y"] = values
                    shared["x"] = category
                else:
                    shared["x"] = values
                    shared["y"] = category
                    shared["orientation"] = "h"
            traces.append(go.Box(**shared))

        fig = go.Figure(data=traces)
        fig.update_layout(**self._layout())
        # `boxmode="overlay"` pairs with the categorical x/y values above
        # so each box anchors to its own tick. Matches ViolinChart's use
        # of `violinmode="overlay"`.
        fig.update_layout(boxmode="overlay")
        self._apply_dimensions(fig)
        return fig

    @staticmethod
    def _apply_precomputed_stats(shared: dict[str, object], group: BoxGroup) -> None:
        # Validator guarantees q1/median/q3 are non-None when values is None.
        assert group.q1 is not None
        assert group.median is not None
        assert group.q3 is not None
        shared["q1"] = [group.q1]
        shared["median"] = [group.median]
        shared["q3"] = [group.q3]
        if group.lowerfence is not None:
            shared["lowerfence"] = [group.lowerfence]
        if group.upperfence is not None:
            shared["upperfence"] = [group.upperfence]
        if group.mean is not None:
            shared["mean"] = [group.mean]
        if group.sd is not None:
            shared["sd"] = [group.sd]


class BoxPlotCard(BaseModel):
    """Card-wrapped `BoxChart` for one column of data, using precomputed stats.

    Accepts a `pd.DataFrame` (picked via `column`), a `pd.Series`, or any
    `Sequence[float]`. Quartiles and whisker fences are computed server-side
    via `BoxGroup.from_values`, so the browser only receives the summary
    floats — ideal for large or heavy-tailed numeric columns (e.g. LLM
    latencies).
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    column: str
    data: pd.DataFrame | pd.Series | Sequence[float]
    label: str | None = None
    title: str | None = None
    description: str | None = None
    fences: QuantileFences | None = QuantileFences.P1_P99
    boxmean: BoxMean = True
    orientation: Literal["v", "h"] = "v"
    include_mean: bool = True
    color: ChartColor | None = None
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

    def render(self) -> mo.Html | ActiveHtml:
        series = self._series()
        if series.empty:
            content: object = mo.md("_No numeric data to display._")
        else:
            group = BoxGroup.from_values(
                self.label if self.label is not None else self.column,
                series.tolist(),
                fences=self.fences,
                include_mean=self.include_mean,
                color=self.color,
            )
            x_tick = self.tick_format if self.orientation == "h" else None
            y_tick = self.tick_format if self.orientation == "v" else None
            content = BoxChart(
                groups=[group],
                boxmean=self.boxmean,
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


__all__ = [
    "BoxChart",
    "BoxGroup",
    "BoxMean",
    "BoxPlotCard",
    "BoxPoints",
]
