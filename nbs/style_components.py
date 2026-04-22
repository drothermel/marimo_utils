import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    import marimo as mo
    from datetime import datetime
    from pathlib import Path

    from mohtml import div

    from marimo_utils.style import (
        Badge,
        Card,
        ColorPalette,
        DataItem,
        DateStamp,
        LabeledList,
        PaletteToneName,
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

    demo_date = datetime(2026, 4, 22)
    return demo_date, palette, spacing, typography


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
    a `.render()` method returning HTML (via `mohtml`). Tokens — `ColorPalette`,
    `Typography`, `SpacingScale` — flow in as dependencies.

    The demos below compose the shared defaults defined in the left column.
    """)
    return


@app.cell(hide_code=True)
def _(palette, spacing, typography):
    mo.vstack(
        [
            mo.md(
                r"""
                ### Badge

                A pill-shaped label with palette-tone aware colors. Tones come
                from `PaletteToneName`.
                """
            ),
            mo.hstack(
                [
                    mo.Html(
                        str(
                            Badge(
                                palette=palette,
                                typography=typography,
                                spacing=spacing,
                                label=tone.value,
                                tone=tone,
                            ).render()
                        )
                    )
                    for tone in PaletteToneName
                ],
                justify="start",
                gap=0.5,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(palette, spacing, typography):
    mo.vstack(
        [
            mo.md(
                r"""
                ### DataItem

                Label + value pair. Optional `value_tone` colors the value using
                the palette.
                """
            ),
            mo.Html(
                str(
                    div(
                        DataItem(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            label="Samples",
                            value="12,345",
                            value_tone=PaletteToneName.SUCCESS,
                        ).render(),
                        DataItem(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            label="In flight",
                            value="7",
                            value_tone=PaletteToneName.INFO,
                        ).render(),
                        DataItem(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            label="Pending",
                            value="124",
                            value_tone=PaletteToneName.WARNING,
                        ).render(),
                        DataItem(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            label="Failed",
                            value="2",
                            value_tone=PaletteToneName.DANGER,
                        ).render(),
                        DataItem(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            label="Notes",
                            value="no special tone",
                        ).render(),
                    )
                )
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(palette, spacing, typography):
    mo.vstack(
        [
            mo.md(
                r"""
                ### Title

                Two-line heading: an uppercase `drop_text` kicker above the main
                `text`. Used as the `Card`'s top section.
                """
            ),
            mo.Html(
                str(
                    Title(
                        palette=palette,
                        typography=typography,
                        spacing=spacing,
                        drop_text="Pool Card",
                        text="demo pool",
                    ).render()
                )
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(demo_date, palette, spacing, typography):
    mo.vstack(
        [
            mo.md(
                r"""
                ### DateStamp and ProjectStamp

                Inline icon + text meta stamps, both `MetaStamp` subclasses.
                """
            ),
            mo.Html(
                str(
                    div(
                        DateStamp(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            value=demo_date,
                        ).render(),
                        ProjectStamp(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            project_name="demo-project",
                        ).render(),
                        style="display: flex; gap: 1rem; align-items: center;",
                    )
                )
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(palette, spacing, typography):
    mo.vstack(
        [
            mo.md(
                r"""
                ### LabeledList

                A section label followed by a horizontal list of rendered items.
                Wraps to multiple lines.
                """
            ),
            mo.Html(
                str(
                    LabeledList(
                        palette=palette,
                        typography=typography,
                        spacing=spacing,
                        section_label="Axes",
                        items=[
                            Badge(
                                palette=palette,
                                typography=typography,
                                spacing=spacing,
                                label=name,
                            ).render()
                            for name in (
                                "model",
                                "dataset",
                                "split",
                                "seed",
                                "step",
                            )
                        ],
                    ).render()
                )
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(demo_date, palette, spacing, typography):
    _card_header = div(
        Badge(
            palette=palette,
            typography=typography,
            spacing=spacing,
            label="in_progress",
            tone=PaletteToneName.WARNING,
        ).render(),
        ProjectStamp(
            palette=palette,
            typography=typography,
            spacing=spacing,
            project_name="demo-project",
        ).render(),
        DateStamp(
            palette=palette,
            typography=typography,
            spacing=spacing,
            value=demo_date,
        ).render(),
        LabeledList(
            palette=palette,
            typography=typography,
            spacing=spacing,
            section_label="Axes",
            items=[
                Badge(
                    palette=palette,
                    typography=typography,
                    spacing=spacing,
                    label=name,
                ).render()
                for name in ("model", "dataset", "split")
            ],
        ).render(),
        style=(
            "display: flex; flex-wrap: wrap; gap: 0.5rem; "
            "align-items: center; margin-top: 0.25rem;"
        ),
    )

    _card_content = div(
        DataItem(
            palette=palette,
            typography=typography,
            spacing=spacing,
            label="Samples",
            value="12,345",
            value_tone=PaletteToneName.SUCCESS,
        ).render(),
        DataItem(
            palette=palette,
            typography=typography,
            spacing=spacing,
            label="In flight",
            value="7",
            value_tone=PaletteToneName.INFO,
        ).render(),
        DataItem(
            palette=palette,
            typography=typography,
            spacing=spacing,
            label="Pending",
            value="124",
            value_tone=PaletteToneName.WARNING,
        ).render(),
        DataItem(
            palette=palette,
            typography=typography,
            spacing=spacing,
            label="Failed",
            value="2",
            value_tone=PaletteToneName.DANGER,
        ).render(),
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ### Card

                The top-level composer. Wraps an optional `Title`, a `header`
                div, and a `content` div inside a styled surface. A divider is
                drawn automatically between the header and content when both
                are present.
                """
            ),
            mo.Html(
                str(
                    Card(
                        palette=palette,
                        typography=typography,
                        spacing=spacing,
                        width="22rem",
                        title=Title(
                            palette=palette,
                            typography=typography,
                            spacing=spacing,
                            drop_text="Pool Card",
                            text="demo pool",
                        ),
                        header=_card_header,
                        content=_card_content,
                    ).render()
                )
            ),
        ]
    )
    return


@app.cell(column=2, hide_code=True)
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
