# Chart color palette demo (#13): run with
#   marimo run nbs/components/color_themes.py --headless --no-token -p 2723

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")

with app.setup:
    import sys
    from pathlib import Path

    import marimo as mo

    from marimo_utils.ui import BarChart, BarItem, ChartColor, bootstrap_tailwind

    _NBS_ROOT = Path(__file__).resolve().parent.parent
    if str(_NBS_ROOT) not in sys.path:
        sys.path.insert(0, str(_NBS_ROOT))


@app.cell
def _():
    bootstrap_tailwind()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # `marimo_utils.ui` — Chart color palette

    Charts cycle through shadcn's stock `--chart-1` → `--chart-5` CSS
    variables by default. Pin a specific slot with `color=ChartColor.X`
    on any series, slice, or bar item.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pinned palette slots (`ChartColor.ONE` → `ChartColor.FIVE`)

    Each bar pins one `ChartColor` enum value, mapping to the
    corresponding `--chart-N` token in the precompiled theme.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md("---"),
            BarChart(
                items=[
                    BarItem(label="ONE", value=5, color=ChartColor.ONE),
                    BarItem(label="TWO", value=5, color=ChartColor.TWO),
                    BarItem(label="THREE", value=5, color=ChartColor.THREE),
                    BarItem(label="FOUR", value=5, color=ChartColor.FOUR),
                    BarItem(label="FIVE", value=5, color=ChartColor.FIVE),
                ],
                title="Pinned ChartColor slots",
                x_label="Slot",
                y_label="Value",
                height=240,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Default colorway cycling (`CHART_COLORWAY`)

    Bars without an explicit `color=` cycle through the five palette
    colors by index — the same behavior used for multi-series charts.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md("---"),
            BarChart(
                items=[
                    BarItem(label="A", value=5),
                    BarItem(label="B", value=5),
                    BarItem(label="C", value=5),
                    BarItem(label="D", value=5),
                    BarItem(label="E", value=5),
                    BarItem(label="F", value=5),
                ],
                title="CHART_COLORWAY cycling",
                x_label="Category",
                y_label="Value",
                height=240,
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
