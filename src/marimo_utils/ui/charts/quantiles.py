from __future__ import annotations

import math
from collections.abc import Sequence
from enum import Enum


class Quantile(float, Enum):
    """Named quantile levels in [0, 1].

    Using a float subclass so members can be passed directly to
    `pandas.Series.quantile` (or anywhere a float is expected) without an
    explicit `.value`.
    """

    P00 = 0.0
    P01 = 0.01
    P05 = 0.05
    P10 = 0.10
    P25 = 0.25
    P50 = 0.50
    P75 = 0.75
    P90 = 0.90
    P95 = 0.95
    P99 = 0.99
    P100 = 1.0


class QuantileFences(Enum):
    """Lower/upper quantile pairs for box-plot whisker fences.

    Chosen so the whiskers anchor at meaningful percentiles instead of
    Plotly's default 1.5x IQR rule — important for heavy-tailed data
    where the default rule generates misleading whiskers and a swarm of
    "outlier" markers. Pass `fences=None` to get Plotly's default behavior.
    """

    P1_P99 = (Quantile.P01, Quantile.P99)
    P5_P95 = (Quantile.P05, Quantile.P95)
    P10_P90 = (Quantile.P10, Quantile.P90)
    MIN_MAX = (Quantile.P00, Quantile.P100)


def compute_gini(counts: Sequence[float | None]) -> float:
    """Gini coefficient of a non-negative count distribution.

    Returns `0.0` for empty / single-value / all-zero inputs (the "no
    skew to measure" cases). `None` and `NaN` entries are dropped; other
    values are coerced to float. Output in [0, 1]: 0 is perfectly even,
    approaches 1 as mass concentrates in a single bucket.
    """
    cleaned = [
        float(c)
        for c in counts
        if c is not None and not (isinstance(c, float) and math.isnan(c))
    ]
    if any(not math.isfinite(c) or c < 0.0 for c in cleaned):
        raise ValueError(
            "compute_gini: counts must contain only finite, non-negative values"
        )
    n = len(cleaned)
    if n <= 1:
        return 0.0
    total = sum(cleaned)
    if total == 0:
        return 0.0
    sorted_asc = sorted(cleaned)
    weighted = sum((i + 1) * c for i, c in enumerate(sorted_asc))
    return (2.0 * weighted) / (n * total) - (n + 1.0) / n


def skew_label(gini: float) -> str:
    """Human-readable bucket for a Gini coefficient.

    Thresholds chosen to match common "how lopsided is this?" intuition:
    under 0.1 is effectively uniform, over 0.7 is one-value-dominates.
    """
    if gini < 0.1:
        return "near-even"
    if gini < 0.3:
        return "mild skew"
    if gini < 0.5:
        return "moderate skew"
    if gini < 0.7:
        return "high skew"
    return "dominated"
