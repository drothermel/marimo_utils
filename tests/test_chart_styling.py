"""Style-contract tests for filled plotly charts.

Filled charts (violin, box) must keep outlines fully saturated so
medians, whiskers, and strokes read crisply; the translucency must live
on `fillcolor` as rgba rather than on trace-level `opacity`, which dims
lines and fill uniformly. These tests lock that contract in — when a new
filled chart is added, parametrize it here.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from marimo_utils.ui import (
    BoxChart,
    BoxGroup,
    ViolinChart,
    ViolinGroup,
)
from marimo_utils.ui.charts._base import PlotlyChart


def _build_violin() -> ViolinChart:
    return ViolinChart(
        groups=[
            ViolinGroup(label="a", values=[1.0, 2.0, 3.0, 4.0]),
            ViolinGroup(label="b", values=[2.0, 3.0, 4.0, 5.0]),
        ]
    )


def _build_box_raw() -> BoxChart:
    return BoxChart(
        groups=[
            BoxGroup(label="a", values=[1.0, 2.0, 3.0, 4.0]),
            BoxGroup(label="b", values=[2.0, 3.0, 4.0, 5.0]),
        ]
    )


def _build_box_precomputed() -> BoxChart:
    return BoxChart(
        groups=[
            BoxGroup(label="pre", q1=1.0, median=2.0, q3=3.0),
        ]
    )


FILLED_CHART_CASES = [
    pytest.param(_build_violin, id="violin"),
    pytest.param(_build_box_raw, id="box-raw"),
    pytest.param(_build_box_precomputed, id="box-precomputed"),
]


def _rgba_alpha(color: str) -> float:
    # "rgba(r, g, b, a)" -> a
    return float(color.rsplit(",", 1)[-1].rstrip(" )"))


@pytest.mark.parametrize("build", FILLED_CHART_CASES)
def test_filled_trace_contract(build: Callable[[], PlotlyChart]) -> None:
    fig = build()._build_figure()
    assert len(fig.data) > 0, "chart built no traces"

    for trace in fig.data:
        line_color = trace.line.color if trace.line is not None else None
        if line_color is not None and isinstance(line_color, str):
            assert not line_color.startswith("rgba"), (
                f"line color must be solid (no alpha); got {line_color!r}"
            )

        fillcolor = trace.fillcolor
        if fillcolor is not None:
            assert isinstance(fillcolor, str), (
                f"fillcolor must be a string; got {fillcolor!r}"
            )
            assert fillcolor.startswith("rgba"), (
                f"fillcolor must carry alpha as rgba(...); got {fillcolor!r}"
            )
            alpha = _rgba_alpha(fillcolor)
            assert 0.0 < alpha < 1.0, (
                f"fillcolor alpha must be in (0, 1); got {alpha} from {fillcolor!r}"
            )

        trace_opacity = trace.opacity
        assert trace_opacity is None or trace_opacity >= 1.0, (
            "trace-level opacity dims lines and fill equally and washes out "
            f"markings; got opacity={trace_opacity}"
        )
