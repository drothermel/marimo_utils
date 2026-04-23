from __future__ import annotations

import marimo as mo
import plotly.graph_objects as go
import plotly.io as pio
from pydantic import BaseModel, ConfigDict, Field, computed_field

from marimo_utils.style.settings import PaletteToneName, Style


class PieSlice(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: int = Field(ge=0)
    tone: PaletteToneName = PaletteToneName.NEUTRAL
    color: str | None = None


class PieChart(BaseModel):
    model_config = ConfigDict(frozen=True)

    style: Style
    slices: list[PieSlice]
    width: int = 260
    height: int = 260
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
        fig.update_layout(width=self.width, height=self.height)
        return fig

    def empty_state_html(self) -> str:
        return (
            '<div style="opacity: 0.6; font-style: italic;">'
            "No slice data available."
            "</div>"
        )

    def _repr_html_(self) -> str:
        if not self.visible_slices:
            return self.empty_state_html()
        return pio.to_html(
            self._build_figure(),
            include_plotlyjs="cdn",
            full_html=False,
        )

    def __str__(self) -> str:
        return self._repr_html_()

    def reactive(self) -> mo.Html:
        """Opt-in marimo-reactive widget.

        Use as the last expression of a cell when you want plotly selections
        fed back into marimo's reactive graph via ``.value``. For static
        display (including inside a ``Card``), use the instance directly —
        its ``_repr_html_`` produces a plotly-rendered HTML fragment that
        still has client-side hover/zoom interactivity.
        """
        if not self.visible_slices:
            return mo.Html(self.empty_state_html())
        return mo.ui.plotly(self._build_figure())


__all__ = ["PieChart", "PieSlice"]
