from __future__ import annotations

import plotly.graph_objects as go
from pydantic import BaseModel, ConfigDict, Field, computed_field

from marimo_utils.style.charts._base import PlotlyChart
from marimo_utils.style.settings import PaletteToneName


class PieSlice(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: int = Field(ge=0)
    tone: PaletteToneName = PaletteToneName.NEUTRAL
    color: str | None = None


class PieChart(PlotlyChart):
    slices: list[PieSlice]
    height: int | None = 260
    hole: float = 0.0
    textposition: str = "outside"
    textinfo: str = "label+value"
    stroke_color: str = "#f8fafc"
    stroke_width: int = 2

    @computed_field
    @property
    def visible_slices(self) -> list[PieSlice]:
        return [slice_ for slice_ in self.slices if slice_.value > 0]

    @computed_field
    @property
    def total(self) -> int:
        return sum(slice_.value for slice_ in self.visible_slices)

    def color_for_slice(self, slice_: PieSlice) -> str:
        if slice_.color is not None:
            return slice_.color
        return self.style.palette.tone(slice_.tone).border

    def empty_state_html(self) -> str:
        return (
            '<div style="opacity: 0.6; font-style: italic;">'
            "No slice data available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return bool(self.visible_slices)

    def _build_figure(self) -> go.Figure:
        visible = self.visible_slices
        labels = [slice_.label for slice_ in visible]
        values = [slice_.value for slice_ in visible]
        colors = [self.color_for_slice(slice_) for slice_ in visible]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=self.hole,
                    textposition=self.textposition,
                    textinfo=self.textinfo,
                    marker={
                        "colors": colors,
                        "line": {
                            "color": self.stroke_color,
                            "width": self.stroke_width,
                        },
                    },
                    sort=False,
                    direction="clockwise",
                )
            ]
        )
        fig.update_layout(**self.style.plotly_layout())
        self._apply_dimensions(fig)
        return fig


__all__ = ["PieChart", "PieSlice"]
