import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    from datetime import datetime
    from pathlib import Path

    import marimo as mo

    from marimo_utils.style import (
        Badge,
        Card,
        ColorPalette,
        DataItem,
        DateStamp,
        LabeledList,
        PaletteToneName,
        PieChart,
        PieSlice,
        ProjectStamp,
        SpacingScale,
        Title,
        Typography,
    )

    NOTEBOOK_PATH = Path(__file__).resolve()
    REPO_ROOT = NOTEBOOK_PATH.parent.parent
    SRC_ROOT = REPO_ROOT / "src"
    PACKAGE_ROOT = SRC_ROOT / "marimo_utils"


@app.cell
def tokens():
    palette = ColorPalette.default()
    typography = Typography.default()
    spacing = SpacingScale.default()
    return palette, spacing, typography


@app.cell(hide_code=True)
def _():
    demo_data = {
        "type": "Classic Card",
        "title": "Class Distribution",
        "project_name": "demo-project",
        "badge_section_label": "Axes",
        "badges": ["model", "dataset", "split"],
        "stats": {"class_a": 5, "class_b": 10, "class_c": 5, "class_d": 1},
        "date": datetime(2026, 4, 22),
    }
    demo_data
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
def _(demo_data, palette, spacing, typography):
    badge_row = mo.hstack(
        [
            Badge(
                palette=palette,
                typography=typography,
                spacing=spacing,
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
def _(demo_data, palette, spacing, typography):
    data_item_list = mo.vstack(
        [
            DataItem(
                palette=palette,
                typography=typography,
                spacing=spacing,
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
def _(demo_data, palette, spacing, typography):
    classic_card_title = Title(
        palette=palette,
        typography=typography,
        spacing=spacing,
        drop_text=demo_data["type"],
        text=demo_data["title"],
    ).render()

    pie_card_title = Title(
        palette=palette,
        typography=typography,
        spacing=spacing,
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
def _(demo_data, palette, spacing, typography):
    meta_stamp_row = mo.hstack(
        [
            DateStamp(
                palette=palette,
                typography=typography,
                spacing=spacing,
                value=demo_data["date"],
            ).render(),
            ProjectStamp(
                palette=palette,
                typography=typography,
                spacing=spacing,
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
def _(demo_data, palette, spacing, typography):
    labeled_list_demo = LabeledList(
        palette=palette,
        typography=typography,
        spacing=spacing,
        section_label=demo_data["badge_section_label"],
        items=[
            Badge(
                palette=palette,
                typography=typography,
                spacing=spacing,
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
def _(demo_data, palette, typography):
    pie_chart_demo = PieChart(
        palette=palette,
        typography=typography,
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
    ).render()

    mo.vstack(
        [
            mo.md(
                r"""
                ### PieChart

                A categorical pie chart using the shared `demo_data["stats"]`
                values and the palette tones used elsewhere in the notebook.
                """
            ),
            pie_chart_demo,
        ]
    )
    return (pie_chart_demo,)


@app.cell(column=2, hide_code=True)
def _(
    classic_card_title,
    data_item_list,
    labeled_list_demo,
    meta_stamp_row,
    palette,
    spacing,
    typography,
):
    card_header = mo.vstack(
        [meta_stamp_row, labeled_list_demo],
        gap=0,
    )

    card_demo = Card(
        palette=palette,
        typography=typography,
        spacing=spacing,
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
def _(
    card_header,
    palette,
    pie_card_title,
    pie_chart_demo,
    spacing,
    typography,
):
    pie_card_demo = Card(
        palette=palette,
        typography=typography,
        spacing=spacing,
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
