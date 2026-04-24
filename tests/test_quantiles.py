"""Unit tests for compute_gini and skew_label.

Gini edge cases: empty / single value / all-equal should return 0.0 ("no
skew to measure"). A perfectly concentrated distribution (one bucket)
approaches (n-1)/n. NaN and None are silently dropped.
"""

from __future__ import annotations

import math

from marimo_utils.ui import compute_gini, skew_label


def test_gini_empty() -> None:
    assert compute_gini([]) == 0.0


def test_gini_single_value() -> None:
    assert compute_gini([5]) == 0.0


def test_gini_all_equal() -> None:
    assert compute_gini([3, 3, 3, 3]) == 0.0


def test_gini_all_zero() -> None:
    assert compute_gini([0, 0, 0]) == 0.0


def test_gini_concentrated_approaches_n_minus_1_over_n() -> None:
    counts = [0] * 9 + [100]
    gini = compute_gini(counts)
    assert math.isclose(gini, 9 / 10, rel_tol=1e-9)


def test_gini_drops_none_and_nan() -> None:
    assert compute_gini([3, 3, 3, None, float("nan")]) == 0.0


def test_gini_moderate_skew_in_range() -> None:
    gini = compute_gini([1, 1, 2, 4, 8])
    assert 0.3 < gini < 0.6


def test_skew_label_thresholds() -> None:
    assert skew_label(0.0) == "near-even"
    assert skew_label(0.09) == "near-even"
    assert skew_label(0.1) == "mild skew"
    assert skew_label(0.29) == "mild skew"
    assert skew_label(0.3) == "moderate skew"
    assert skew_label(0.49) == "moderate skew"
    assert skew_label(0.5) == "high skew"
    assert skew_label(0.69) == "high skew"
    assert skew_label(0.7) == "dominated"
    assert skew_label(1.0) == "dominated"
