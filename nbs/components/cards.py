# Card component demo (#13): run with
#   marimo run nbs/components/cards.py --headless --no-token -p 2721

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")

with app.setup:
    import sys
    from pathlib import Path

    import marimo as mo

    from marimo_utils.ui import Badge, BadgeVariant, Card, DataItem, bootstrap_tailwind

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
    # `marimo_utils.ui` — Card
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Card
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Card chrome with shadcn-style flat `title=` and `description=`
            string params. Internally the outer wrapper uses
            `DivLayouts.COL_SHELL`; title and description compose into a
            `DivLayouts.COL` header section; `content` renders in a
            sibling `DivLayouts.COL` with `pt-0` when a header is present
            (full `COL` padding when there is no header). Default width
            `CardWidth.DEFAULT` (`w-100`); override with ``CardWidth.NARROW``,
            ``CardWidth.WIDE``, or any Tailwind width utility.
            """),
            mo.md("---"),
            Card(
                title="Class Distribution",
                description="Class counts across the training split",
                content=mo.vstack(
                    [
                        Badge(
                            label="dataset",
                            variant=BadgeVariant.SECONDARY,
                        ).render(),
                        DataItem(label="Class A", value="5").render(),
                        DataItem(label="Class B", value="10").render(),
                        DataItem(label="Class C", value="5").render(),
                        DataItem(label="Class D", value="1").render(),
                    ],
                    gap=0.25,
                ),
            ).render(),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
