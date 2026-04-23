import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    import random
    from datetime import datetime
    from pathlib import Path

    import marimo as mo

    from marimo_utils.style import (
        Badge,
        BarChart,
        BarItem,
        Card,
        DataItem,
        DateStamp,
        HeatmapChart,
        HistogramChart,
        LabeledList,
        PaletteToneName,
        PieChart,
        PieSlice,
        ProjectStamp,
        Style,
        Title,
        ViolinChart,
        ViolinGroup,
    )

    NOTEBOOK_PATH = Path(__file__).resolve()
    REPO_ROOT = NOTEBOOK_PATH.parent.parent
    SRC_ROOT = REPO_ROOT / "src"
    PACKAGE_ROOT = SRC_ROOT / "marimo_utils"
    DEMO_RNG = random.Random(42)


@app.cell
def tokens():
    style = Style.default()
    return (style,)


@app.cell(hide_code=True)
def _():
    _rng = random.Random(42)
    demo_data = {
        "type": "Classic Card",
        "title": "Class Distribution",
        "project_name": "demo-project",
        "badge_section_label": "Axes",
        "badges": ["model", "dataset", "split"],
        "stats": {"class_a": 5, "class_b": 10, "class_c": 5, "class_d": 1},
        "date": datetime(2026, 4, 22),
        "loss_values": [_rng.gauss(0.4, 0.12) for _ in range(180)],
        "group_distributions": {
            "train": [_rng.gauss(0.35, 0.10) for _ in range(120)],
            "val": [_rng.gauss(0.45, 0.14) for _ in range(120)],
            "test": [_rng.gauss(0.52, 0.11) for _ in range(120)],
        },
        "confusion": {
            "rows": ["cat", "dog", "bird"],
            "cols": ["cat", "dog", "bird"],
            "z": [[42, 3, 1], [4, 38, 2], [2, 5, 33]],
        },
    }
    mo.vstack(
        [
            mo.md("**Demo Data**"),
            demo_data,
        ]
    )
    return (demo_data,)


@app.cell(column=1, hide_code=True)
def _():
    mo.md(r"""
    ## Style Components
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `marimo_utils.style` is a small design system for rendering Pydantic-backed
    inspection cards in marimo notebooks. Each atom is a frozen `BaseModel` with
    a `.render()` method returning a marimo-native renderable. `mohtml` remains
    the HTML authoring tool for the styled atoms, while `Card` can now host
    both those styled fragments and native notebook outputs like charts.

    The demos below compose the shared defaults defined in the left column.
    """)
    return


@app.cell(hide_code=True)
def _(demo_data, style):
    badge_row = mo.hstack(
        [
            Badge(
                style=style,
                label=_label,
                tone=_tone,
            ).render()
            for _label, _tone in zip(
                demo_data["badges"],
                (
                    PaletteToneName.INFO,
                    PaletteToneName.SUCCESS,
                    PaletteToneName.WARNING,
                ),
                strict=False,
            )
        ],
        justify="start",
        gap=0.5,
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### Badge

                A pill-shaped label with palette-tone aware colors. This demo now
                reuses the shared badge labels from `demo_data`.
                """
            ),
            badge_row,
        ]
    )
    return


@app.cell(hide_code=True)
def _(demo_data, style):
    data_item_list = mo.vstack(
        [
            DataItem(
                style=style,
                label=_label.replace("_", " ").title(),
                value=str(_value),
                value_tone=_tone,
            ).render()
            for (_label, _value), _tone in zip(
                demo_data["stats"].items(),
                (
                    PaletteToneName.NEUTRAL,
                    PaletteToneName.INFO,
                    PaletteToneName.SUCCESS,
                    PaletteToneName.WARNING,
                ),
                strict=False,
            )
        ],
        gap=0,
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### DataItem

                Label + value pair. Optional `value_tone` colors the value using
                the palette. This demo now reads its labels and values from
                `demo_data["stats"]`.
                """
            ),
            data_item_list,
        ]
    )
    return (data_item_list,)


@app.cell(hide_code=True)
def _(demo_data, style):
    classic_card_title = Title(
        style=style,
        drop_text=demo_data["type"],
        text=demo_data["title"],
    ).render()

    pie_card_title = Title(
        style=style,
        drop_text="Pie Card",
        text=demo_data["title"],
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Title

                Two-line heading: an uppercase `drop_text` kicker above the main
                `text`. Used as the `Card`'s top section.
                """
            ),
            classic_card_title,
        ]
    )
    return classic_card_title, pie_card_title


@app.cell(hide_code=True)
def _(demo_data, style):
    meta_stamp_row = mo.hstack(
        [
            DateStamp(
                style=style,
                value=demo_data["date"],
            ).render(),
            ProjectStamp(
                style=style,
                project_name=demo_data["project_name"],
            ).render(),
        ],
        justify="start",
        align="center",
        gap=0.5,
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### DateStamp and ProjectStamp

                Inline icon + text meta stamps, both `MetaStamp` subclasses.
                Both values now come from `demo_data`.
                """
            ),
            meta_stamp_row,
        ]
    )
    return (meta_stamp_row,)


@app.cell(hide_code=True)
def _(demo_data, style):
    labeled_list_demo = LabeledList(
        style=style,
        section_label=demo_data["badge_section_label"],
        items=[
            Badge(
                style=style,
                label=_name,
            ).render()
            for _name in demo_data["badges"]
        ],
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### LabeledList

                A section label followed by a horizontal list of rendered items.
                Wraps to multiple lines.
                """
            ),
            labeled_list_demo,
        ]
    )
    return (labeled_list_demo,)


@app.cell(hide_code=True)
def _(demo_data, style):
    pie_chart_demo = PieChart(
        style=style,
        slices=[
            PieSlice(
                label=_label.replace("_", " ").title(),
                value=_value,
                tone=_tone,
            )
            for (_label, _value), _tone in zip(
                demo_data["stats"].items(),
                (
                    PaletteToneName.NEUTRAL,
                    PaletteToneName.INFO,
                    PaletteToneName.SUCCESS,
                    PaletteToneName.WARNING,
                ),
                strict=False,
            )
        ],
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### PieChart

                A plotly-backed pie chart with outside labels (`label+value`)
                so small slices stay readable. Displayed bare it renders
                non-reactively via `_repr_html_`; call `.reactive()` for a
                marimo-reactive widget.
                """
            ),
            pie_chart_demo,
        ]
    )
    return (pie_chart_demo,)


@app.cell(hide_code=True)
def _(demo_data, style):
    bar_chart_demo = BarChart(
        style=style,
        height=200,
        items=[
            BarItem(
                label=_label.replace("_", " ").title(),
                value=_value,
                tone=_tone,
            )
            for (_label, _value), _tone in zip(
                demo_data["stats"].items(),
                (
                    PaletteToneName.NEUTRAL,
                    PaletteToneName.INFO,
                    PaletteToneName.SUCCESS,
                    PaletteToneName.WARNING,
                ),
                strict=False,
            )
        ],
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### BarChart

                Categorical bar chart with per-bar tones. Shares the
                palette/tone semantics of `PieSlice` via `BarItem`.
                """
            ),
            bar_chart_demo,
        ]
    )
    return (bar_chart_demo,)


@app.cell(hide_code=True)
def _(demo_data, style):
    histogram_demo = HistogramChart(
        style=style,
        height=200,
        values=demo_data["loss_values"],
        tone=PaletteToneName.INFO,
        nbins=24,
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### HistogramChart

                1-D distribution via `go.Histogram`. Single tone; plotly
                handles binning via `nbins` or `bin_size`.
                """
            ),
            histogram_demo,
        ]
    )
    return (histogram_demo,)


@app.cell(hide_code=True)
def _(demo_data, style):
    violin_chart_demo = ViolinChart(
        style=style,
        height=240,
        groups=[
            ViolinGroup(label=_name, values=_values, tone=_tone)
            for (_name, _values), _tone in zip(
                demo_data["group_distributions"].items(),
                (
                    PaletteToneName.INFO,
                    PaletteToneName.SUCCESS,
                    PaletteToneName.WARNING,
                ),
                strict=False,
            )
        ],
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### ViolinChart

                Grouped violin plot — one trace per `ViolinGroup` so each
                group gets its own palette tone.
                """
            ),
            violin_chart_demo,
        ]
    )
    return (violin_chart_demo,)


@app.cell(hide_code=True)
def _(demo_data, style):
    heatmap_demo = HeatmapChart(
        style=style,
        height=240,
        z=demo_data["confusion"]["z"],
        x_labels=demo_data["confusion"]["cols"],
        y_labels=demo_data["confusion"]["rows"],
        tone=PaletteToneName.INFO,
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### HeatmapChart

                2-D matrix with a tone-driven sequential colorscale (from
                `Style.tone_colorscale`). Rows align with `y_labels`,
                columns with `x_labels`; cell values are annotated via
                `show_values`.
                """
            ),
            heatmap_demo,
        ]
    )
    return (heatmap_demo,)


@app.cell(column=2, hide_code=True)
def _(
    classic_card_title,
    data_item_list,
    labeled_list_demo,
    meta_stamp_row,
    style,
):
    card_header = mo.vstack(
        [meta_stamp_row, labeled_list_demo],
        gap=0,
    )

    card_demo = Card(
        style=style,
        width="22rem",
        title=classic_card_title,
        header=card_header,
        content=data_item_list,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Card

                The top-level composer. This classic card reuses the component
                globals defined above and renders the shared data-item list as its
                content.
                """
            ),
            card_demo,
        ]
    )
    return (card_header,)


@app.cell(hide_code=True)
def _(card_header, pie_card_title, pie_chart_demo, style):
    pie_card_demo = Card(
        style=style,
        width="22rem",
        title=pie_card_title,
        header=card_header,
        content=pie_chart_demo,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Pie Card

                A second card variant that reuses the same header components and
                swaps the content area to the shared pie chart renderable.
                """
            ),
            pie_card_demo,
        ]
    )
    return


@app.cell(hide_code=True)
def _(bar_chart_demo, card_header, demo_data, style):
    bar_card_title = Title(
        style=style,
        drop_text="Bar Card",
        text=demo_data["title"],
    ).render()
    bar_card_demo = Card(
        style=style,
        # width="22rem",
        width="10rem",
        title=bar_card_title,
        header=card_header,
        content=bar_chart_demo,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Bar Card

                Card variant that swaps the content area for the shared
                bar chart renderable.
                """
            ),
            bar_card_demo,
        ]
    )
    return


@app.cell(hide_code=True)
def _(card_header, histogram_demo, style):
    histogram_card_title = Title(
        style=style,
        drop_text="Histogram Card",
        text="Loss Distribution",
    ).render()
    histogram_card_demo = Card(
        style=style,
        width="22rem",
        title=histogram_card_title,
        header=card_header,
        content=histogram_demo,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Histogram Card

                Card variant showing a 1-D distribution via the
                `HistogramChart` renderable.
                """
            ),
            histogram_card_demo,
        ]
    )
    return


@app.cell(hide_code=True)
def _(card_header, style, violin_chart_demo):
    violin_card_title = Title(
        style=style,
        drop_text="Violin Card",
        text="Split Distributions",
    ).render()
    violin_card_demo = Card(
        style=style,
        width="22rem",
        title=violin_card_title,
        header=card_header,
        content=violin_chart_demo,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Violin Card

                Card variant showing grouped distributions via the
                `ViolinChart` renderable.
                """
            ),
            violin_card_demo,
        ]
    )
    return


@app.cell(hide_code=True)
def _(card_header, heatmap_demo, style):
    heatmap_card_title = Title(
        style=style,
        drop_text="Heatmap Card",
        text="Confusion Matrix",
    ).render()
    heatmap_card_demo = Card(
        style=style,
        width="22rem",
        title=heatmap_card_title,
        header=card_header,
        content=heatmap_demo,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Heatmap Card

                Card variant showing a 2-D matrix via the
                `HeatmapChart` renderable.
                """
            ),
            heatmap_card_demo,
        ]
    )
    return


@app.cell(hide_code=True)
def _(card_header, demo_data, style):
    constrained_chart = BarChart(
        style=style,
        height=None,
        items=[
            BarItem(
                label=_label.replace("_", " ").title(),
                value=_value,
                tone=_tone,
            )
            for (_label, _value), _tone in zip(
                demo_data["stats"].items(),
                (
                    PaletteToneName.NEUTRAL,
                    PaletteToneName.INFO,
                    PaletteToneName.SUCCESS,
                    PaletteToneName.WARNING,
                ),
                strict=False,
            )
        ],
    )
    constrained_card_title = Title(
        style=style,
        drop_text="Constrained Card",
        text="Fixed Height",
    ).render()
    constrained_card_demo = Card(
        style=style,
        width="22rem",
        height="22rem",
        title=constrained_card_title,
        header=card_header,
        content=constrained_chart,
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### Constrained Card

                `Card(height=...)` turns the card into a flex column and wraps
                the content area with `flex: 1 1 auto`, so a responsive chart
                (`height=None`) fills the remaining vertical space below the
                title, header, and divider.
                """
            ),
            constrained_card_demo,
        ]
    )
    return


@app.cell(column=3, hide_code=True)
def _():
    mo.md(r"""
    leave space
    """)
    return


@app.cell(hide_code=True)
def _():
    script_output = None
    if mo.app_meta().mode == "script":
        script_output = {
            "mode": "script",
            "notebook_path": NOTEBOOK_PATH.relative_to(REPO_ROOT),
            "package_root": PACKAGE_ROOT.relative_to(REPO_ROOT),
        }
    script_output
    return


if __name__ == "__main__":
    app.run()
