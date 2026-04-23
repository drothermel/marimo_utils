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


SHADCN_FONT_FAMILY = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"


DEFAULT_FONT_SIZE = 12
DEFAULT_TICK_LABEL_STANDOFF = 5


def shadcn_plotly_layout(
    *,
    font_size: int = DEFAULT_FONT_SIZE,
    tick_font_size: int | None = None,
    tick_label_standoff: int = DEFAULT_TICK_LABEL_STANDOFF,
) -> dict[str, object]:
    """Build a shadcn-themed plotly layout dict parameterized by font sizes.

    `font_size` governs the base font — legend, hover, titles — and also
    the default for tick labels when `tick_font_size` is `None`. Pass an
    explicit `tick_font_size` to decouple tick labels from the base font.
    `tick_label_standoff` is the pixel gap between tick labels and the
    axis line; plotly's default is 0, and a few pixels of breathing room
    reads more cleanly.
    """
    effective_tick_size = font_size if tick_font_size is None else tick_font_size
    axis_style = {
        "gridcolor": SHADCN_BORDER_HEX,
        "zerolinecolor": SHADCN_BORDER_HEX,
        "tickfont": {"size": effective_tick_size},
        "ticklabelstandoff": tick_label_standoff,
    }
    return {
        "font": {
            "family": SHADCN_FONT_FAMILY,
            "color": SHADCN_FOREGROUND_HEX,
            "size": font_size,
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {"l": 8, "r": 8, "t": 8, "b": 8},
        "colorway": CHART_COLORWAY,
        "showlegend": False,
        "xaxis": axis_style,
        "yaxis": axis_style,
    }


# Default layout instance — kept as a module-level constant so callers who
# want the theme without per-chart overrides can splat it directly.
SHADCN_PLOTLY_LAYOUT: dict[str, object] = shadcn_plotly_layout()


class PlotlyChart(BaseModel):
    """Base class for shadcn-themed plotly charts.

    Subclasses override `_has_data` and `_build_figure`. Shared plumbing
    (dimensions, empty state, `_repr_html_`, reactive widget, layout
    generation) lives here so every chart keeps the same Card-embedding
    contract. Charts flow through `ActiveHtml` because plotly embeds
    `<script>` tags; the Tailwind bootstrap injects the shadcn stylesheet
    inside each shadow root so Card chrome hosting a chart still resolves
    its utilities.

    Typography knobs (`font_size`, `tick_font_size`, `tick_label_standoff`)
    are configurable on every chart via the constructor. They feed into
    `_layout()` which returns a per-chart layout dict.
    """

    model_config = ConfigDict(frozen=True)

    width: int | None = None
    height: int | None = None
    responsive: bool = True
    font_size: int = DEFAULT_FONT_SIZE
    tick_font_size: int | None = None
    tick_label_standoff: int = DEFAULT_TICK_LABEL_STANDOFF

    def _effective_tick_font_size(self) -> int:
        """Tick font size, inheriting from `font_size` when unset."""
        return self.font_size if self.tick_font_size is None else self.tick_font_size

    def _layout(self) -> dict[str, object]:
        return shadcn_plotly_layout(
            font_size=self.font_size,
            tick_font_size=self.tick_font_size,
            tick_label_standoff=self.tick_label_standoff,
        )

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
    "DEFAULT_FONT_SIZE",
    "DEFAULT_TICK_LABEL_STANDOFF",
    "SHADCN_BORDER_HEX",
    "SHADCN_FONT_FAMILY",
    "SHADCN_FOREGROUND_HEX",
    "SHADCN_MUTED_FG_HEX",
    "SHADCN_PLOTLY_LAYOUT",
    "PlotlyChart",
    "shadcn_plotly_layout",
]
