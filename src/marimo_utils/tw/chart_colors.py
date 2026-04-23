from __future__ import annotations

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


__all__ = ["CHART_COLORWAY", "CHART_HEX", "ChartColor"]
