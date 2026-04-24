from __future__ import annotations

import math
import re
from enum import IntEnum


class ChartColor(IntEnum):
    """Shadcn chart palette — five categorical, non-semantic colors.

    Matches shadcn's stock `--chart-1` through `--chart-5` CSS variables.
    The names are deliberately neutral (numbers, not meanings) so they
    don't collide with UI token semantics like `primary` / `destructive`.
    Series without an explicit color cycle through `CHART_COLORWAY` by
    index.
    """

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


CHART_HEX: dict[ChartColor, str] = {
    ChartColor.ONE: "#e76e50",
    ChartColor.TWO: "#2a9d8f",
    ChartColor.THREE: "#264653",
    ChartColor.FOUR: "#e9c468",
    ChartColor.FIVE: "#f4a261",
}


CHART_COLORWAY: list[str] = list(CHART_HEX.values())


def chart_colorscale(
    color: ChartColor, *, light_alpha: float = 0.12
) -> list[list[float | str]]:
    """Two-stop sequential colorscale for plotly heatmap/choropleth.

    Low stop is the chart color at low alpha (airy background); high stop
    is the full saturated chart color. Mirrors the contract of the
    existing `Style.tone_colorscale` — plug the return value into
    `go.Heatmap(colorscale=...)`.
    """
    return [[0.0, hex_to_rgba(CHART_HEX[color], light_alpha)], [1.0, CHART_HEX[color]]]


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert a `#rrggbb` string to a plotly-ready `rgba(r, g, b, a)` string.

    Used to build translucent fills that keep line_color solid — uniform
    trace-level `opacity` dims fills and outlines equally, which washes
    out box-plot median lines and violin inner-box markings.
    """
    if not isinstance(hex_color, str):
        raise ValueError("hex_to_rgba: hex_color must be a string")
    if not isinstance(alpha, int | float) or not math.isfinite(alpha):
        raise ValueError("hex_to_rgba: alpha must be a finite number in [0.0, 1.0]")

    h = hex_color.lstrip("#")
    if len(h) != 6 or re.fullmatch(r"[0-9A-Fa-f]{6}", h) is None:
        raise ValueError("hex_to_rgba: hex_color must be exactly 6 hex characters")
    if not 0.0 <= float(alpha) <= 1.0:
        raise ValueError("hex_to_rgba: alpha must be in [0.0, 1.0]")

    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def filled_trace_colors(hex_color: str, *, fill_alpha: float = 0.35) -> dict[str, str]:
    """Return `line_color` + `fillcolor` kwargs for a filled plotly trace.

    Charts that draw both an outline and a fill (violin, box) must keep
    the outline fully saturated so medians, whiskers, and strokes read
    crisply — and push the translucency onto `fillcolor` via rgba rather
    than trace-level `opacity`, which would dim lines and fill equally
    and wash out the visual hierarchy. Always construct the pair through
    this helper so the invariant can't drift per chart.
    """
    return {
        "line_color": hex_color,
        "fillcolor": hex_to_rgba(hex_color, fill_alpha),
    }


__all__ = [
    "CHART_COLORWAY",
    "CHART_HEX",
    "ChartColor",
    "chart_colorscale",
    "filled_trace_colors",
    "hex_to_rgba",
]
