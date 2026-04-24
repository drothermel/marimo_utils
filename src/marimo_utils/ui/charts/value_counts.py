from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

import marimo as mo
import pandas as pd
from dr_widget.inline import ActiveHtml
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.card import Card
from marimo_utils.ui.chart_colors import ChartColor
from marimo_utils.ui.charts.bar import BarChart, BarItem


def _truncate(s: str, n: int) -> str:
    if n <= 0:
        raise ValueError("label_width must be a positive integer")
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


class FrequencyBarCard(BaseModel):
    """Card-wrapped top-N bar chart of distinct-value frequencies.

    For low-cardinality categoricals where you can afford to label each
    distinct value directly. Three data-input modes:

    - `pd.DataFrame` + `column`: runs `value_counts()` on the column, or
      `groupby(column)[weight_column].sum()` when a `weight_column` is
      given (useful for pre-aggregated frames like a coverage frame with
      a `count` column).
    - `pd.Series`: used as pre-aggregated counts — index becomes the bar
      labels, values become the bar heights. The `column` field is only
      used for display.
    - `Mapping[str, int | float]`: same treatment as a Series.

    Sorted descending by count by default, truncated to `top_n`, labels
    truncated to `label_width` characters. Horizontal orientation is the
    default because vertical tick labels on long ids don't read.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    column: str
    data: pd.DataFrame | pd.Series | Mapping[str, float]
    weight_column: str | None = None
    top_n: int = 20
    sort: Literal["count_desc", "count_asc", "label"] = "count_desc"
    title: str | None = None
    description: str | None = None
    color: ChartColor = ChartColor.TWO
    orientation: Literal["h", "v"] = "h"
    label_width: int = 30
    x_label: str | None = None
    y_label: str | None = None
    # `None` auto-sizes the chart: for horizontal orientation the height
    # scales with the number of bars so labels don't collide, with a 220px
    # floor so a single-bar card doesn't look empty.
    height: int | None = None
    width: str = "w-96"
    # Calibrated to clear plotly's y-tick auto-skip threshold at horizontal
    # orientation: bars need more vertical room than the tick label itself
    # because plotly also reserves the top/bottom plot margin and leaves space
    # for rotated x-tick labels below. Under-budgeting here silently hides
    # most y-labels once the bar count climbs past ~12.
    bar_pixels: int = 30
    min_height: int = 220
    chrome_pixels: int = 120

    def _counts(self) -> pd.Series:
        if isinstance(self.data, pd.DataFrame):
            if self.weight_column is None:
                return self.data[self.column].value_counts(dropna=False)
            return (
                self.data.groupby(self.column, dropna=False)[self.weight_column]
                .sum()
                .astype(float)
            )
        if isinstance(self.data, pd.Series):
            return self.data
        return pd.Series(dict(self.data))

    def _effective_height(self, n_items: int) -> int:
        if self.height is not None:
            return self.height
        if self.orientation == "h":
            return max(self.min_height, self.bar_pixels * n_items + self.chrome_pixels)
        return self.min_height

    def _ordered(self, counts: pd.Series) -> pd.Series:
        if self.sort == "count_desc":
            return counts.sort_values(ascending=False)
        if self.sort == "count_asc":
            return counts.sort_values(ascending=True)
        return counts.sort_index()

    def render(self) -> mo.Html | ActiveHtml:
        counts = self._counts()
        if counts.empty:
            content: object = mo.md("_No values to display._")
        else:
            if self.top_n <= 0:
                raise ValueError("top_n must be a positive integer")
            ordered = self._ordered(counts).head(self.top_n)
            items = [
                BarItem(
                    label=_truncate(str(label), self.label_width),
                    value=float(value),
                    color=self.color,
                )
                for label, value in ordered.items()
            ]
            # Horizontal charts read top-down, so reverse the list — the
            # largest count lands at the top of the axis.
            if self.orientation == "h":
                items = list(reversed(items))
            content = BarChart(
                items=items,
                orientation=self.orientation,
                height=self._effective_height(len(items)),
                show_legend=False,
                x_label=self.x_label,
                y_label=self.y_label,
            )
        return Card(
            title=self.title,
            description=self.description,
            content=content,
            width=self.width,
        ).render()


__all__ = ["FrequencyBarCard"]
