from __future__ import annotations

import marimo as mo
import plotly.graph_objects as go
import plotly.io as pio
from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.charts.colors import CHART_COLORWAY
from marimo_utils.ui.core.drhtml import cn
from marimo_utils.ui.styles import Typography

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
    show_legend: bool = False,
    title: str | None = None,
    title_font_size: int | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
    x_tick_format: str | None = None,
    y_tick_format: str | None = None,
) -> dict[str, object]:
    """Build a shadcn-themed plotly layout dict parameterized by typography.

    `font_size` governs the base font — legend, hover, axis titles — and
    the default for tick labels when `tick_font_size` is `None`. Pass an
    explicit `tick_font_size` to decouple tick labels from the base font.
    `tick_label_standoff` is the pixel gap between tick labels and the
    axis line; plotly's default is 0, and a few pixels of breathing room
    reads more cleanly. `show_legend` opts in to plotly's legend; default
    is off because most dashboard-style charts label their series inline.
    `title`, `x_label`, `y_label` are optional text — when set, plotly's
    `automargin` expands the relevant margin to fit. `title_font_size`
    sets the plot title size independently; when `None`, it defaults to
    `font_size + 2`. The title is always rendered bold (shadcn-style
    card-heading weight). `x_range` / `y_range` pin the axis bounds to a
    `(min, max)` tuple; leave `None` for plotly's auto-range.
    """
    effective_tick_size = font_size if tick_font_size is None else tick_font_size

    def _axis(
        label: str | None,
        range_: tuple[float, float] | None,
        tick_format: str | None,
    ) -> dict[str, object]:
        axis: dict[str, object] = {
            "gridcolor": SHADCN_BORDER_HEX,
            "zerolinecolor": SHADCN_BORDER_HEX,
            "tickfont": {"size": effective_tick_size},
            "ticklabelstandoff": tick_label_standoff,
        }
        if label is not None:
            axis["title"] = {"text": label}
            axis["automargin"] = True
        if range_ is not None:
            axis["range"] = list(range_)
        if tick_format is not None:
            axis["tickformat"] = tick_format
        return axis

    margin = {"l": 8, "r": 8, "t": 8, "b": 8}
    if title is not None:
        margin["t"] = 40

    layout: dict[str, object] = {
        "font": {
            "family": SHADCN_FONT_FAMILY,
            "color": SHADCN_FOREGROUND_HEX,
            "size": font_size,
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": margin,
        "colorway": CHART_COLORWAY,
        "showlegend": show_legend,
        "xaxis": _axis(x_label, x_range, x_tick_format),
        "yaxis": _axis(y_label, y_range, y_tick_format),
    }
    if title is not None:
        effective_title_size = (
            title_font_size if title_font_size is not None else font_size + 2
        )
        layout["title"] = {
            "text": title,
            "font": {"size": effective_title_size, "weight": "bold"},
            "x": 0.0,
            "xanchor": "left",
            "pad": {"l": 8},
        }
    return layout


# Default layout instance — kept as a module-level constant so callers who
# want the theme without per-chart overrides can splat it directly.
SHADCN_PLOTLY_LAYOUT: dict[str, object] = shadcn_plotly_layout()


class PlotlyChart(BaseModel):
    """Base class for shadcn-themed plotly charts.

    Subclasses override `_has_data` and `_build_figure`. Shared plumbing
    (dimensions, empty state, `_repr_html_`, reactive widget, layout
    generation) lives here so every chart keeps the same Card-embedding
    contract. Charts flow through `ActiveHtml` because plotly embeds
    `<script>` tags; the precompiled stylesheet is injected inside each
    shadow root so Card chrome hosting a chart still resolves its utilities.

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
    show_legend: bool = False
    title: str | None = None
    title_font_size: int | None = None
    x_label: str | None = None
    y_label: str | None = None
    y_range: tuple[float, float] | None = None
    x_tick_format: str | None = None
    y_tick_format: str | None = None

    def _effective_tick_font_size(self) -> int:
        """Tick font size, inheriting from `font_size` when unset."""
        return self.font_size if self.tick_font_size is None else self.tick_font_size

    def _layout(
        self, *, x_range: tuple[float, float] | None = None
    ) -> dict[str, object]:
        """Build the per-chart layout dict.

        `x_range` is accepted here (not as a base field) because it only
        makes sense on charts with a continuous-numeric x-axis —
        `HistogramChart`, `ScatterChart`, `LineChart`. Charts with
        categorical x (Bar, Violin, Heatmap) don't pass it; pinning a
        numeric range on a categorical axis silently clips by category
        index, which is rarely what you want.
        """
        return shadcn_plotly_layout(
            font_size=self.font_size,
            tick_font_size=self.tick_font_size,
            tick_label_standoff=self.tick_label_standoff,
            show_legend=self.show_legend,
            title=self.title,
            title_font_size=self.title_font_size,
            x_label=self.x_label,
            y_label=self.y_label,
            x_range=x_range,
            y_range=self.y_range,
            x_tick_format=self.x_tick_format,
            y_tick_format=self.y_tick_format,
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

    def _empty_state_html(self, message: str) -> str:
        klass = cn(Typography.BODY_MUTED, "italic")
        return f'<div class="{klass}">{message}</div>'

    def empty_state_html(self) -> str:
        return self._empty_state_html("No data available.")

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
