from __future__ import annotations

from typing import Literal

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict, computed_field

from marimo_utils.style.charts._base import PlotlyChart
from marimo_utils.style.settings import PaletteToneName


class BarItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: float
    tone: PaletteToneName = PaletteToneName.NEUTRAL
    color: str | None = None


class BarChart(PlotlyChart):
    """Single-series categorical bar chart with per-bar tone colors.

    Multi-series / stacked / grouped variants are intentionally deferred —
    keep one ``BarItem`` per bar and build a new chart for each series.
    """

    items: list[BarItem]
    orientation: Literal["v", "h"] = "v"
    height: int | None = 220
    stroke_color: str = "#f8fafc"
    stroke_width: int = 1

    @computed_field
    @property
    def visible_items(self) -> list[BarItem]:
        return list(self.items)

    def color_for_item(self, item: BarItem) -> str:
        if item.color is not None:
            return item.color
        return self.style.palette.tone(item.tone).border

    def empty_state_html(self) -> str:
        return (
            '<div style="opacity: 0.6; font-style: italic;">'
            "No bar data available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return bool(self.visible_items)

    def _build_figure(self) -> go.Figure:
        labels = [item.label for item in self.visible_items]
        values = [item.value for item in self.visible_items]
        colors = [self.color_for_item(item) for item in self.visible_items]

        if self.orientation == "v":
            bar = go.Bar(
                x=labels,
                y=values,
                marker={
                    "color": colors,
                    "line": {
                        "color": self.stroke_color,
                        "width": self.stroke_width,
                    },
                },
            )
        else:
            bar = go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker={
                    "color": colors,
                    "line": {
                        "color": self.stroke_color,
                        "width": self.stroke_width,
                    },
                },
            )

        fig = go.Figure(data=[bar])
        fig.update_layout(**self.style.plotly_layout())
        self._apply_dimensions(fig)
        return fig


__all__ = ["BarChart", "BarItem"]
