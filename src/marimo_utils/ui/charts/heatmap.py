from __future__ import annotations

import plotly.graph_objects as go
from pydantic import Field, model_validator

from marimo_utils.ui.chart_colors import ChartColor, chart_colorscale
from marimo_utils.ui.charts._base import (
    SHADCN_FONT_FAMILY,
    SHADCN_FOREGROUND_HEX,
    PlotlyChart,
)


class HeatmapChart(PlotlyChart):
    """2-D heatmap with a single-color sequential gradient.

    `z` is a row-major matrix. Rows align with `y_labels` top-to-bottom
    (plotly's default `yaxis.autorange='reversed'` is applied when
    `y_labels` is supplied); columns align with `x_labels`. The
    colorscale is a two-stop gradient from low-alpha to saturated chart
    color — see `chart_colorscale` in `chart_colors`.
    """

    z: list[list[float]]
    x_labels: list[str] = Field(default_factory=list)
    y_labels: list[str] = Field(default_factory=list)
    color: ChartColor = ChartColor.ONE
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
        return self._empty_state_html("No heatmap data available.")

    def _has_data(self) -> bool:
        return bool(self.z) and bool(self.z[0])

    def _build_figure(self) -> go.Figure:
        # Heatmaps don't have a meaningful traditional legend — the color
        # information lives in the colorscale bar. So we remap the base
        # `show_legend` toggle to `showscale` for this chart type, and
        # suppress the empty traditional legend unconditionally.
        heatmap_kwargs: dict[str, object] = {
            "z": self.z,
            "colorscale": chart_colorscale(self.color),
            "showscale": self.show_legend,
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
                "family": SHADCN_FONT_FAMILY,
                "color": SHADCN_FOREGROUND_HEX,
                "size": self._effective_tick_font_size(),
            }

        fig = go.Figure(data=[go.Heatmap(**heatmap_kwargs)])
        fig.update_layout(**self._layout())
        # Heatmap never shows plotly's traditional legend; the colorbar is
        # the legend equivalent and is controlled via `showscale` above.
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False, autorange="reversed")
        self._apply_dimensions(fig)
        return fig
