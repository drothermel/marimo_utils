from __future__ import annotations

import plotly.graph_objects as go
from pydantic import Field, model_validator

from marimo_utils.style.charts._base import PlotlyChart
from marimo_utils.style.settings import PaletteToneName


class HeatmapChart(PlotlyChart):
    """2-D heatmap with a palette-tone-driven sequential colorscale.

    ``z`` is a row-major matrix. Rows align with ``y_labels`` top-to-bottom
    (matching plotly's default ``yaxis.autorange='reversed'`` on heatmaps
    when ``y_labels`` are supplied), columns with ``x_labels``.
    """

    z: list[list[float]]
    x_labels: list[str] = Field(default_factory=list)
    y_labels: list[str] = Field(default_factory=list)
    tone: PaletteToneName = PaletteToneName.INFO
    show_values: bool = True
    value_format: str = ".0f"
    cell_gap: int = 1
    height: int | None = 260

    @model_validator(mode="after")
    def _check_shapes(self) -> HeatmapChart:
        if not self.z:
            return self
        row_len = len(self.z[0])
        for row in self.z:
            if len(row) != row_len:
                raise ValueError("All rows of `z` must have the same length")
        if self.x_labels and len(self.x_labels) != row_len:
            raise ValueError(
                f"x_labels length ({len(self.x_labels)}) must match "
                f"`z` column count ({row_len})"
            )
        if self.y_labels and len(self.y_labels) != len(self.z):
            raise ValueError(
                f"y_labels length ({len(self.y_labels)}) must match "
                f"`z` row count ({len(self.z)})"
            )
        return self

    def empty_state_html(self) -> str:
        return (
            '<div style="opacity: 0.6; font-style: italic;">'
            "No heatmap data available."
            "</div>"
        )

    def _has_data(self) -> bool:
        return bool(self.z) and bool(self.z[0])

    def _build_figure(self) -> go.Figure:
        heatmap_kwargs: dict[str, object] = {
            "z": self.z,
            "colorscale": self.style.tone_colorscale(self.tone),
            "showscale": False,
            "xgap": self.cell_gap,
            "ygap": self.cell_gap,
            "hoverongaps": False,
        }
        if self.x_labels:
            heatmap_kwargs["x"] = self.x_labels
        if self.y_labels:
            heatmap_kwargs["y"] = self.y_labels

        if self.show_values:
            heatmap_kwargs["text"] = [
                [format(cell, self.value_format) for cell in row] for row in self.z
            ]
            heatmap_kwargs["texttemplate"] = "%{text}"
            heatmap_kwargs["textfont"] = {
                "family": self.style.typography.font_family,
                "color": self.style.palette.text_primary,
                "size": 11,
            }

        fig = go.Figure(data=[go.Heatmap(**heatmap_kwargs)])
        fig.update_layout(**self.style.plotly_layout())
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False, autorange="reversed")
        self._apply_dimensions(fig)
        return fig


__all__ = ["HeatmapChart"]
