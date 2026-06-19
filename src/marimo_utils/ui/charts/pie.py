from __future__ import annotations

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict, Field, computed_field

from marimo_utils.ui.chart_colors import CHART_COLORWAY, CHART_HEX, ChartColor
from marimo_utils.ui.charts._base import PlotlyChart


class PieSlice(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: int = Field(ge=0)
    color: ChartColor | None = None


class PieChart(PlotlyChart):
    """Shadcn-themed pie chart.

    Slices without an explicit `color` cycle through `CHART_COLORWAY` by
    index, so unthemed usage produces a balanced categorical palette.
    The default `stroke_color` is `--background` (white) so slice
    boundaries blend into a Card's `bg-card` surface.
    """

    slices: list[PieSlice]
    height: int | None = 260
    hole: float = Field(default=0.0, ge=0.0, le=1.0)
    textposition: str = "outside"
    textinfo: str = "label+value"
    stroke_color: str = "#ffffff"
    stroke_width: int = Field(default=2, ge=0)

    @computed_field
    @property
    def visible_slices(self) -> list[PieSlice]:
        return [s for s in self.slices if s.value > 0]

    @computed_field
    @property
    def total(self) -> int:
        return sum(s.value for s in self.visible_slices)

    def _has_data(self) -> bool:
        return bool(self.visible_slices)

    def empty_state_html(self) -> str:
        return self._empty_state_html("No slice data available.")

    def _color_for_slice(self, slice_: PieSlice, index: int) -> str:
        if slice_.color is not None:
            return CHART_HEX[slice_.color]
        return CHART_COLORWAY[index % len(CHART_COLORWAY)]

    def _build_figure(self) -> go.Figure:
        visible = self.visible_slices
        labels = [s.label for s in visible]
        values = [s.value for s in visible]
        colors = [self._color_for_slice(s, i) for i, s in enumerate(visible)]

        pie_kwargs: dict[str, object] = {
            "labels": labels,
            "values": values,
            "hole": self.hole,
            "textposition": self.textposition,
            "textinfo": self.textinfo,
            "marker": {
                "colors": colors,
                "line": {
                    "color": self.stroke_color,
                    "width": self.stroke_width,
                },
            },
            "sort": False,
            "direction": "clockwise",
        }
        # When a legend is shown, shrink the pie's horizontal domain so its
        # outside labels don't collide with the legend column. The reserved
        # right strip fits plotly's default right-anchored legend.
        if self.show_legend:
            pie_kwargs["domain"] = {"x": [0.0, 0.72]}

        fig = go.Figure(data=[go.Pie(**pie_kwargs)])
        fig.update_layout(**self._layout())
        self._apply_dimensions(fig)
        return fig
