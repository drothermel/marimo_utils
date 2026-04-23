import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    from datetime import datetime
    from pathlib import Path

    import marimo as mo

    from marimo_utils.tw import (
        Badge,
        BadgeVariant,
        Card,
        CardDescription,
        CardTitle,
        DataItem,
        DateStamp,
        LabeledList,
        LucideIcon,
        PieChart,
        PieSlice,
        ProjectStamp,
        bootstrap_tailwind,
    )

    NOTEBOOK_PATH = Path(__file__).resolve()
    REPO_ROOT = NOTEBOOK_PATH.parent.parent
    SRC_ROOT = REPO_ROOT / "src"
    PACKAGE_ROOT = SRC_ROOT / "marimo_utils"


@app.cell
def _():
    bootstrap_tailwind()
    return


@app.cell(column=1, hide_code=True)
def _():
    mo.md(r"""
    # Tailwind + shadcn spike — `marimo_utils.tw`
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Parallel implementation of the style package using Tailwind (Play CDN)
    themed with shadcn/ui defaults. `bootstrap_tailwind()` injects shadcn's
    CSS variables on `:root` (zinc light mode) plus the handful of
    utility rules that depend on them (`bg-primary`, `text-*-foreground`,
    `border-border`, `ring-ring`, hover variants), then loads the Tailwind
    CDN for the built-in utilities.

    Component APIs use shadcn's stock variant names (`default`,
    `secondary`, `destructive`, `outline`) with no custom tone layer.
    The existing inline-CSS version lives in `style_components.py` for
    A/B comparison.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Badge — one per variant
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Four shadcn badge variants. If all four render as distinct
            pills with different fills, the full stack is live: CDN
            loaded, config extension applied, CSS variables resolved.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    Badge(label="default", variant=BadgeVariant.DEFAULT).render(),
                    Badge(
                        label="secondary", variant=BadgeVariant.SECONDARY
                    ).render(),
                    Badge(
                        label="destructive", variant=BadgeVariant.DESTRUCTIVE
                    ).render(),
                    Badge(label="outline", variant=BadgeVariant.OUTLINE).render(),
                ],
                justify="start",
                gap=0.5,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Escape hatch: `klass=` override
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            `Badge(klass="ring-2 ring-ring ring-offset-2")` appends extra
            utilities. The ring color comes from `--ring` via the Tailwind
            config extension, so the emphasis stays on-theme.
            """),
            mo.md("---"),
            Badge(
                label="emphasized",
                variant=BadgeVariant.DEFAULT,
                klass="ring-2 ring-ring ring-offset-2",
            ).render(),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## CardTitle & CardDescription
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Shadcn's canonical header pair — `CardTitle` (`<h3>` with
            `text-2xl font-semibold leading-none tracking-tight`) above
            `CardDescription` (`<p>` with `text-sm text-muted-foreground`).
            Rendered here standalone with a small gap; when used inside
            `Card` they sit in a shared `flex flex-col space-y-1.5 p-6`
            wrapper that matches shadcn's `CardHeader`.
            """),
            mo.md("---"),
            mo.vstack(
                [
                    CardTitle(text="Class Distribution").render(),
                    CardDescription(
                        text="Class counts across the training split"
                    ).render(),
                ],
                gap=0.25,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## DataItem
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Label + value pair. Label uses `text-muted-foreground` in an
            uppercase kicker style; value uses `text-foreground` semibold.
            `min-w-28` on the label keeps multiple items aligned.
            """),
            mo.md("---"),
            mo.vstack(
                [
                    DataItem(label="Class A", value="5").render(),
                    DataItem(label="Class B", value="10").render(),
                    DataItem(label="Class C", value="5").render(),
                    DataItem(label="Class D", value="1").render(),
                ],
                gap=0.25,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## LucideIcon
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Shadcn-style icon primitive: SVG sized by Tailwind utilities on
            the wrapper (default `h-4 w-4`), `stroke="currentColor"` so the
            color inherits from any `text-*` utility on an ancestor. Below:
            the same `calendar` icon at default, larger, and inside a
            `text-destructive` parent so it tints without a color prop.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    LucideIcon(name="calendar").render(),
                    LucideIcon(name="calendar", size="h-6 w-6").render(),
                    mo.Html(
                        f'<span class="text-destructive inline-flex">'
                        f"{LucideIcon(name='calendar').render().text}</span>"
                    ),
                ],
                justify="start",
                align="center",
                gap=1.0,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## DateStamp & ProjectStamp
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Inline icon + text meta rows using the shadcn `flex items-center
            gap-2 text-sm text-muted-foreground` idiom. Icon color inherits
            from the container's muted text color via `currentColor`.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    DateStamp(value=datetime(2026, 4, 22)).render(),
                    ProjectStamp(project_name="demo-project").render(),
                ],
                justify="start",
                align="center",
                gap=1.0,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## LabeledList
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Section label prefix + flex-wrapping list of rendered items.
            Label uses shadcn's muted `text-sm font-medium` style rather
            than the form-coupled `Label` primitive. Items auto-render
            (any `.render()`-bearing component) or pass through.
            """),
            mo.md("---"),
            LabeledList(
                label="Axes",
                items=[
                    Badge(label="model", variant=BadgeVariant.SECONDARY),
                    Badge(label="dataset", variant=BadgeVariant.SECONDARY),
                    Badge(label="split", variant=BadgeVariant.SECONDARY),
                ],
            ).render(),
        ]
    )
    return


@app.cell(column=2, hide_code=True)
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
            string params. Internally they compose into a `CardHeader`-
            shaped wrapper (`flex flex-col space-y-1.5 p-6`) containing
            `CardTitle` + `CardDescription`. `content` renders in a
            sibling `p-6 pt-0` block. Default width `w-72` (~18rem);
            override with `width="w-96"` or any Tailwind width utility.
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
            PieChart(
                slices=[
                    PieSlice(label="Class A", value=5),
                    PieSlice(label="Class B", value=10),
                    PieSlice(label="Class C", value=5),
                    PieSlice(label="Class D", value=1),
                ],
            ),
            mo.md("---"),
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
                width="w-80",
            ).render(),
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
