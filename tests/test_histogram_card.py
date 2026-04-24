"""Structural tests for HistogramChart binning/log_y and HistogramCard.

Locks the contract for the three knobs added alongside HistogramCard:
- `binning="integer"` renders unit-width bars centered on integer ticks
  (xbins.size == 1 and dtick == 1 on the value axis).
- `binning="continuous"` falls back to plotly's auto-bin / nbins path.
- `binning="auto"` picks integer for narrow integer-valued ranges,
  continuous otherwise.
- `log_y` sets the count-axis type to "log" (routes to xaxis when
  orientation is horizontal).
"""

from __future__ import annotations

import pandas as pd

from marimo_utils.ui import HistogramCard, HistogramChart


def test_integer_binning_sets_unit_bins_and_dtick() -> None:
    fig = HistogramChart(
        values=[1, 1, 2, 3, 3, 3, 4], binning="integer"
    )._build_figure()
    xbins = fig.data[0].xbins
    assert xbins is not None
    assert xbins.size == 1
    assert xbins.start == 0.5
    assert xbins.end == 4.5
    assert fig.layout.xaxis.dtick == 1


def test_continuous_binning_uses_nbins() -> None:
    fig = HistogramChart(
        values=[0.1, 0.2, 0.3, 0.9, 1.5, 2.7],
        binning="continuous",
        nbins=10,
    )._build_figure()
    assert fig.data[0].nbinsx == 10
    # xbins.size must not be set — that would override nbinsx.
    xbins = fig.data[0].xbins
    assert xbins is None or xbins.size is None


def test_auto_picks_integer_for_narrow_integer_range() -> None:
    fig = HistogramChart(
        values=[1, 1, 2, 2, 3, 3, 4, 4, 5, 5], binning="auto"
    )._build_figure()
    assert fig.data[0].xbins is not None
    assert fig.data[0].xbins.size == 1


def test_auto_picks_continuous_when_range_exceeds_max_integer_bars() -> None:
    fig = HistogramChart(
        values=[0, 10, 20, 30, 40, 100], binning="auto"
    )._build_figure()
    xbins = fig.data[0].xbins
    assert xbins is None or xbins.size is None


def test_auto_density_gate_prefers_continuous_for_sparse_integers() -> None:
    # 6 integer values spread over a range of 8 (0..8) would give 9 integer
    # buckets — more buckets than data points. Density gate should fall back
    # to continuous so bars aren't mostly empty.
    values: list[float] = [0.0, 1.0, 3.0, 5.0, 7.0, 8.0]
    fig = HistogramChart(values=values, binning="auto")._build_figure()
    xbins = fig.data[0].xbins
    assert xbins is None or xbins.size is None


def test_auto_respects_custom_max_integer_bars() -> None:
    # Range 19 exceeds default max=10, but with max_integer_bars=25 it fits,
    # and density is fine (20 buckets, 20 values).
    values: list[float] = [float(i) for i in range(20)]
    fig = HistogramChart(
        values=values, binning="auto", max_integer_bars=25
    )._build_figure()
    assert fig.data[0].xbins is not None
    assert fig.data[0].xbins.size == 1


def test_auto_picks_continuous_for_float_values() -> None:
    fig = HistogramChart(
        values=[0.1, 0.2, 0.5, 0.9, 1.3], binning="auto"
    )._build_figure()
    xbins = fig.data[0].xbins
    assert xbins is None or xbins.size is None


def test_log_y_sets_count_axis_log_vertical() -> None:
    fig = HistogramChart(
        values=[1.0, 2.0, 3.0, 4.0], log_y=True, orientation="v"
    )._build_figure()
    assert fig.layout.yaxis.type == "log"


def test_log_y_routes_to_xaxis_when_horizontal() -> None:
    fig = HistogramChart(
        values=[1.0, 2.0, 3.0, 4.0], log_y=True, orientation="h"
    )._build_figure()
    assert fig.layout.xaxis.type == "log"


def test_empty_values_hits_empty_state_html() -> None:
    chart = HistogramChart(values=[])
    assert not chart._has_data()
    assert "No values to histogram" in chart.empty_state_html()


def test_histogram_card_renders_from_sequence() -> None:
    card = HistogramCard(data=[1, 1, 1, 2, 3, 3], column="x", title="t")
    html = str(card.render())
    assert len(html) > 0


def test_histogram_card_renders_from_dataframe_column() -> None:
    frame = pd.DataFrame({"n": [1, 2, 2, 3, 3, 3]})
    card = HistogramCard(data=frame, column="n")
    html = str(card.render())
    assert len(html) > 0


def test_histogram_card_empty_series_and_render_does_not_raise() -> None:
    card = HistogramCard(data=[], column="x")
    assert card._series().empty
    # render() must handle the empty path without raising.
    card.render()


def test_histogram_card_drops_non_numeric() -> None:
    frame = pd.DataFrame({"n": [1, 2, "bad", None, 3]})
    card = HistogramCard(data=frame, column="n")
    # Should not raise; produces a non-empty render.
    assert len(str(card.render())) > 0


def test_histogram_card_value_scale_applied() -> None:
    card = HistogramCard(
        data=[1000.0, 2000.0, 3000.0],
        column="latency_ms",
        value_scale=0.001,
        binning="continuous",
    )
    series = card._series()
    assert list(series) == [1.0, 2.0, 3.0]
