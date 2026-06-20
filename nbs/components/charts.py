# Chart component demos (#13): run with
#   marimo run nbs/components/charts.py --headless --no-token -p 2722

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="full")

with app.setup:
    import sys
    from pathlib import Path

    _NBS_ROOT = Path(__file__).resolve().parent.parent
    if str(_NBS_ROOT) not in sys.path:
        sys.path.insert(0, str(_NBS_ROOT))

    import marimo as mo

    from fixtures.synthetic import (
        CONFUSION_LABELS,
        CONFUSION_Z,
        GROUP_TEST,
        GROUP_TRAIN,
        GROUP_VAL,
        LINE_STEPS,
        LINE_TRAIN_LOSS,
        LINE_VAL_LOSS,
        LOSS_VALUES,
        SCATTER_A_X,
        SCATTER_A_Y,
        SCATTER_B_X,
        SCATTER_B_Y,
    )
    from marimo_utils.ui import (
        BarChart,
        BarItem,
        BoxChart,
        BoxGroup,
        BoxPlotCard,
        Card,
        CardWidth,
        ChartColor,
        HeatmapChart,
        HistogramCard,
        HistogramChart,
        LineChart,
        LineSeries,
        PieChart,
        PieSlice,
        ScatterChart,
        ScatterSeries,
        ViolinChart,
        ViolinGroup,
        ViolinPlotCard,
        bootstrap_tailwind,
    )


@app.cell
def _():
    bootstrap_tailwind()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # `marimo_utils.ui` — Charts

    Every section pairs a standalone chart with a Card-wrapped variant via
    `mo.hstack`, exercising the shadow-DOM embedding path uniformly.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## PieChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Shadcn-themed pie chart. Slices cycle through the `--chart-1` →
            `--chart-5` palette by default; pass `color=ChartColor.X` on a
            slice to pin a specific color. The second figure renders the
            chart inside a `Card` to exercise shadow-DOM handling — the
            theme `<style>` travels into the shadow root alongside the
            plotly blob, so card chrome resolves shadcn utilities locally.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    PieChart(
                        slices=[
                            PieSlice(label="Class A", value=5),
                            PieSlice(label="Class B", value=10),
                            PieSlice(label="Class C", value=5),
                            PieSlice(label="Class D", value=1),
                        ],
                        title="Class Distribution",
                        show_legend=True,
                    ),
                    Card(
                        title="Class Distribution",
                        description="Class counts across the training split",
                        content=PieChart(
                            slices=[
                                PieSlice(label="Class A", value=5),
                                PieSlice(label="Class B", value=10),
                                PieSlice(label="Class C", value=5),
                                PieSlice(label="Class D", value=1),
                            ],
                            height=220,
                        ),
                        width=CardWidth.NARROW,
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## BarChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Single-series categorical bar chart. Bars without an explicit
            `color` cycle through `CHART_COLORWAY` by index; pin specific
            bars with `color=ChartColor.X`.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    BarChart(
                        items=[
                            BarItem(label="Class A", value=5),
                            BarItem(label="Class B", value=10),
                            BarItem(label="Class C", value=5),
                            BarItem(label="Class D", value=1),
                        ],
                        title="Class Distribution",
                        x_label="Class",
                        y_label="Count",
                    ),
                    Card(
                        title="Class Distribution",
                        description="Counts across the training split",
                        content=BarChart(
                            items=[
                                BarItem(label="Class A", value=5),
                                BarItem(label="Class B", value=10),
                                BarItem(label="Class C", value=5),
                                BarItem(label="Class D", value=1),
                            ],
                            height=220,
                        ),
                        width=CardWidth.NARROW,
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## HistogramChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            1-D distribution histogram — single-color chart. Set
            `color=ChartColor.X` to pick one of the five palette colors.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    HistogramChart(
                        values=LOSS_VALUES,
                        color=ChartColor.TWO,
                        nbins=28,
                        title="Loss Distribution",
                        x_label="Loss",
                        y_label="Count",
                    ),
                    HistogramCard(
                        column="loss",
                        data=LOSS_VALUES,
                        title="Loss Distribution",
                        description="Per-sample training loss",
                        color=ChartColor.TWO,
                        nbins=28,
                        y_label="Count",
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## HeatmapChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            2-D heatmap with a single-hue sequential gradient (low-alpha to
            saturated chart color). Cells display their values formatted
            via `value_format`. Typical use: confusion matrix.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    HeatmapChart(
                        z=CONFUSION_Z,
                        x_labels=CONFUSION_LABELS,
                        y_labels=CONFUSION_LABELS,
                        color=ChartColor.THREE,
                        show_legend=True,
                        title="Confusion Matrix",
                        x_label="Predicted",
                        y_label="Actual",
                    ),
                    Card(
                        title="Confusion Matrix",
                        description="Predicted vs actual class",
                        content=HeatmapChart(
                            z=CONFUSION_Z,
                            x_labels=CONFUSION_LABELS,
                            y_labels=CONFUSION_LABELS,
                            color=ChartColor.THREE,
                            height=220,
                        ),
                        width=CardWidth.NARROW,
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ViolinChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Grouped violin plot — one trace per `ViolinGroup` so each gets
            its own palette color (cycling `CHART_COLORWAY` by index).
            The legend appears automatically when multiple groups render.

            For large datasets, `max_samples=N` downsamples each group in
            Python (deterministic via `sample_seed`) before shipping to
            Plotly — essential because `go.Violin` otherwise serializes
            every raw point and computes the KDE client-side. The Card on
            the right demos this with `max_samples=40` and
            `spanmode="hard"` to clip the KDE at the data range rather
            than letting bandwidth smear into negatives.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    ViolinChart(
                        groups=[
                            ViolinGroup(label="train", values=GROUP_TRAIN),
                            ViolinGroup(label="val", values=GROUP_VAL),
                            ViolinGroup(label="test", values=GROUP_TEST),
                        ],
                        show_legend=True,
                        title="Loss Distribution by Split",
                        x_label="Split",
                        y_label="Loss",
                    ),
                    ViolinPlotCard(
                        column="train_loss",
                        data=GROUP_TRAIN,
                        title="Train Loss Distribution",
                        description="Single-column violin card",
                        color=ChartColor.ONE,
                        spanmode="hard",
                        max_samples=40,
                        y_label="Loss",
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## BoxChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Grouped box plot — one trace per `BoxGroup`. Two input modes:
            raw `values` (Plotly computes quartiles and Tukey whiskers)
            and precomputed stats (`q1`, `median`, `q3`, optional
            `lowerfence` / `upperfence` / `mean` / `sd`). Custom fences
            replace Plotly's default 1.5x IQR rule — essential for
            heavy-tailed data where you want whiskers at meaningful
            percentiles (p1/p99, min/max) rather than generating a swarm
            of "outlier" markers. The Card on the right ships only five
            floats to Plotly — no raw points travel to the browser.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    BoxChart(
                        groups=[
                            BoxGroup(label="train", values=GROUP_TRAIN),
                            BoxGroup(label="val", values=GROUP_VAL),
                            BoxGroup(label="test", values=GROUP_TEST),
                        ],
                        show_legend=True,
                        title="Loss Distribution by Split",
                        x_label="Split",
                        y_label="Loss",
                    ),
                    BoxPlotCard(
                        column="train_loss",
                        data=GROUP_TRAIN,
                        title="Train Loss Distribution",
                        description="Precomputed stats via BoxPlotCard",
                        color=ChartColor.ONE,
                        y_label="Loss",
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ScatterChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Multi-series scatter — one trace per `ScatterSeries` so each
            cluster gets its own palette color (cycling `CHART_COLORWAY`
            by index). The second figure embeds the same chart inside a
            `Card` to verify shadow-DOM handling, mirroring the pie demo.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    ScatterChart(
                        series=[
                            ScatterSeries(
                                label="cluster A",
                                x=SCATTER_A_X,
                                y=SCATTER_A_Y,
                            ),
                            ScatterSeries(
                                label="cluster B",
                                x=SCATTER_B_X,
                                y=SCATTER_B_Y,
                            ),
                        ],
                        title="Embedding Clusters",
                        show_legend=True,
                        x_label="x",
                        y_label="y",
                    ),
                    Card(
                        title="Embedding Clusters",
                        description="Two-cluster projection preview",
                        content=ScatterChart(
                            series=[
                                ScatterSeries(
                                    label="cluster A",
                                    x=SCATTER_A_X,
                                    y=SCATTER_A_Y,
                                ),
                                ScatterSeries(
                                    label="cluster B",
                                    x=SCATTER_B_X,
                                    y=SCATTER_B_Y,
                                ),
                            ],
                            height=220,
                            show_legend=True,
                            x_label="x",
                            y_label="y",
                        ),
                        width=CardWidth.NARROW,
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## LineChart
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Multi-series line chart — one trace per `LineSeries`. Use
            `dash="dash"` on a series to distinguish paired lines
            (e.g., solid train vs dashed validation).
            """),
            mo.md("---"),
            mo.hstack(
                [
                    LineChart(
                        series=[
                            LineSeries(
                                label="train",
                                x=LINE_STEPS,
                                y=LINE_TRAIN_LOSS,
                            ),
                            LineSeries(
                                label="val",
                                x=LINE_STEPS,
                                y=LINE_VAL_LOSS,
                                dash="dash",
                            ),
                        ],
                        title="Training Curves",
                        show_legend=True,
                        x_label="Step",
                        y_label="Loss",
                    ),
                    Card(
                        title="Training Curves",
                        description="Train vs. validation loss",
                        content=LineChart(
                            series=[
                                LineSeries(
                                    label="train",
                                    x=LINE_STEPS,
                                    y=LINE_TRAIN_LOSS,
                                ),
                                LineSeries(
                                    label="val",
                                    x=LINE_STEPS,
                                    y=LINE_VAL_LOSS,
                                    dash="dash",
                                ),
                            ],
                            show_legend=True,
                            x_label="Step",
                            y_label="Loss",
                            height=220,
                        ),
                        width=CardWidth.NARROW,
                    ).render(),
                ],
                justify="space-around",
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
