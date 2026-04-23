from __future__ import annotations

import marimo as mo
import plotly.graph_objects as go
import plotly.io as pio
from pydantic import BaseModel, ConfigDict

from marimo_utils.style.settings import Style


class PlotlyChart(BaseModel):
    """Base class for Card-ready plotly charts.

    Subclasses override ``_has_data`` and ``_build_figure``. Shared plumbing
    (``_repr_html_``, ``__str__``, ``reactive``, empty state, dimension
    application) lives here so every chart keeps the same Card-embedding
    contract.

    Dimensions default to ``None`` meaning *fill the container*; ``responsive``
    defaults to ``True`` so plotly.js refits on container resize. Pass explicit
    ``width`` / ``height`` ints (pixels) to fix dimensions.
    """

    model_config = ConfigDict(frozen=True)

    style: Style
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
        return '<div style="opacity: 0.6; font-style: italic;">No data available.</div>'

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
        """Opt-in marimo-reactive widget.

        Use as the last expression of a cell when you want plotly selections
        fed back into marimo's reactive graph via ``.value``. For static
        display (including inside a ``Card``), use the instance directly —
        its ``_repr_html_`` produces a plotly-rendered HTML fragment that
        still has client-side hover/zoom interactivity.
        """
        if not self._has_data():
            return mo.Html(self.empty_state_html())
        return mo.ui.plotly(self._build_figure())


__all__ = ["PlotlyChart"]
