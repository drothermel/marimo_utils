from __future__ import annotations

import marimo as mo
import plotly.graph_objects as go
import plotly.io as pio
from pydantic import BaseModel, ConfigDict

from marimo_utils.tw.chart_colors import CHART_COLORWAY

# Hex mirrors of the shadcn CSS variables, used where plotly needs
# literal color strings (plotly can't consume `hsl(var(--x))`).
SHADCN_FOREGROUND_HEX = "#09090b"
SHADCN_MUTED_FG_HEX = "#71717a"
SHADCN_BORDER_HEX = "#e4e4e7"


SHADCN_PLOTLY_LAYOUT: dict[str, object] = {
    "font": {
        "family": "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif",
        "color": SHADCN_FOREGROUND_HEX,
    },
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"l": 8, "r": 8, "t": 8, "b": 8},
    "colorway": CHART_COLORWAY,
    "showlegend": False,
    "xaxis": {
        "gridcolor": SHADCN_BORDER_HEX,
        "zerolinecolor": SHADCN_BORDER_HEX,
    },
    "yaxis": {
        "gridcolor": SHADCN_BORDER_HEX,
        "zerolinecolor": SHADCN_BORDER_HEX,
    },
}


class PlotlyChart(BaseModel):
    """Base class for shadcn-themed plotly charts.

    Subclasses override `_has_data` and `_build_figure`. Shared plumbing
    (dimensions, empty state, `_repr_html_`, reactive widget) lives here
    so every chart keeps the same Card-embedding contract. Charts flow
    through `ActiveHtml` because plotly embeds `<script>` tags; the
    Tailwind bootstrap injects the shadcn stylesheet inside each shadow
    root so Card chrome hosting a chart still resolves its utilities.
    """

    model_config = ConfigDict(frozen=True)

    width: int | None = None
    height: int | None = None
    responsive: bool = True

    def _has_data(self) -> bool:
        raise NotImplementedError

    def _build_figure(self) -> go.Figure:
        raise NotImplementedError

    def _apply_dimensions(self, fig: go.Figure) -> None:
        if self.width is not None:
            fig.update_layout(width=self.width)
        if self.height is not None:
            fig.update_layout(height=self.height)

    def empty_state_html(self) -> str:
        return (
            '<div class="text-sm italic text-muted-foreground">No data available.</div>'
        )

    def _repr_html_(self) -> str:
        if not self._has_data():
            return self.empty_state_html()
        return pio.to_html(
            self._build_figure(),
            include_plotlyjs="cdn",
            full_html=False,
            config={"responsive": self.responsive},
        )

    def __str__(self) -> str:
        return self._repr_html_()

    def reactive(self) -> mo.Html:
        """Return a marimo-reactive widget when you want `.value` wired in."""
        if not self._has_data():
            return mo.Html(self.empty_state_html())
        return mo.ui.plotly(self._build_figure())


__all__ = [
    "SHADCN_BORDER_HEX",
    "SHADCN_FOREGROUND_HEX",
    "SHADCN_MUTED_FG_HEX",
    "SHADCN_PLOTLY_LAYOUT",
    "PlotlyChart",
]
