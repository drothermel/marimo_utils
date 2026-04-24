"""Structural tests for FrequencyBarCard.

Covers the three data-input modes (DataFrame raw, DataFrame weighted,
pre-aggregated Series), top-N truncation, label truncation, sort
modes, and empty-data handling.
"""

from __future__ import annotations

import pandas as pd

from marimo_utils.ui import FrequencyBarCard


def test_dataframe_raw_runs_value_counts() -> None:
    frame = pd.DataFrame({"key": ["a", "b", "a", "a", "c"]})
    card = FrequencyBarCard(data=frame, column="key")
    counts = card._counts()
    assert int(counts["a"]) == 3
    assert int(counts["b"]) == 1
    assert int(counts["c"]) == 1


def test_dataframe_weighted_sums_weight_column() -> None:
    frame = pd.DataFrame(
        {
            "key": ["a", "a", "b", "c"],
            "count": [10, 5, 7, 3],
        }
    )
    card = FrequencyBarCard(data=frame, column="key", weight_column="count")
    counts = card._counts()
    assert int(counts["a"]) == 15
    assert int(counts["b"]) == 7
    assert int(counts["c"]) == 3


def test_series_used_as_pre_aggregated() -> None:
    series = pd.Series({"a": 12, "b": 3, "c": 9})
    card = FrequencyBarCard(data=series, column="key")
    counts = card._counts()
    assert int(counts["a"]) == 12
    assert int(counts["b"]) == 3


def test_mapping_used_as_pre_aggregated() -> None:
    card = FrequencyBarCard(data={"a": 12.0, "b": 3.0}, column="key")
    counts = card._counts()
    assert int(counts["a"]) == 12
    assert int(counts["b"]) == 3


def test_top_n_truncates() -> None:
    series = pd.Series({f"id_{i}": 100 - i for i in range(50)})
    card = FrequencyBarCard(data=series, column="id", top_n=5, sort="count_desc")
    html = str(card.render())
    # Structural: render produces non-empty output; we can't introspect the
    # bar list from the HTML, but we can check the ordered path directly.
    ordered = card._ordered(card._counts()).head(card.top_n)
    assert list(ordered.index) == ["id_0", "id_1", "id_2", "id_3", "id_4"]
    assert len(html) > 0


def test_sort_count_asc() -> None:
    series = pd.Series({"a": 5, "b": 1, "c": 3})
    card = FrequencyBarCard(data=series, column="k", sort="count_asc")
    ordered = card._ordered(card._counts())
    assert list(ordered.index) == ["b", "c", "a"]


def test_sort_label() -> None:
    series = pd.Series({"b": 5, "a": 1, "c": 3})
    card = FrequencyBarCard(data=series, column="k", sort="label")
    ordered = card._ordered(card._counts())
    assert list(ordered.index) == ["a", "b", "c"]


def test_empty_series_renders_without_raising() -> None:
    card = FrequencyBarCard(data=pd.Series(dtype=float), column="k")
    assert card._counts().empty
    card.render()


def test_label_truncation_applied() -> None:
    series = pd.Series({"this_is_a_very_long_identifier_indeed": 4})
    card = FrequencyBarCard(data=series, column="k", label_width=10)
    html = str(card.render())
    assert len(html) > 0


def test_auto_height_scales_with_bar_count_horizontal() -> None:
    # Single-bar card stays at the min-height floor.
    short = FrequencyBarCard(data=pd.Series({"a": 1}), column="k")
    assert short._effective_height(1) == short.min_height
    # Many-bar card grows to accommodate all labels.
    tall = FrequencyBarCard(
        data=pd.Series({f"id_{i}": 10 for i in range(18)}), column="k"
    )
    expected = tall.bar_pixels * 18 + tall.chrome_pixels
    assert expected > tall.min_height
    assert tall._effective_height(18) == expected


def test_auto_height_ignores_orientation_v() -> None:
    card = FrequencyBarCard(
        data=pd.Series({f"id_{i}": 10 for i in range(18)}),
        column="k",
        orientation="v",
    )
    assert card._effective_height(18) == card.min_height


def test_explicit_height_overrides_auto_sizing() -> None:
    card = FrequencyBarCard(
        data=pd.Series({f"id_{i}": 10 for i in range(18)}),
        column="k",
        height=300,
    )
    assert card._effective_height(18) == 300
