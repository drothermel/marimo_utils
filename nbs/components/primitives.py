# UI primitives demo (#13): run with
#   marimo run nbs/components/primitives.py --headless --no-token -p 2720

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")

with app.setup:
    import sys
    from datetime import datetime
    from pathlib import Path

    import marimo as mo

    from marimo_utils.ui import (
        Badge,
        BadgeVariant,
        CardDescription,
        CardTitle,
        DataItem,
        IconSize,
        LabeledList,
        LucideIcon,
        SemanticTone,
        ToneEmphasis,
        bad_badge,
        bool_badge,
        bootstrap_tailwind,
        date_stamp,
        good_badge,
        neutral_badge,
        project_stamp,
    )

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
    # `marimo_utils.ui` — Tailwind + shadcn design primitives
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Design system for rendering Pydantic-backed UI primitives inside
    marimo notebooks. `bootstrap_tailwind()` injects the precompiled
    `dr.css` stylesheet once per page — Tailwind utilities (Preflight
    off), shadcn theme tokens, and a scoped `.dr-scope` reset — without
    loading the Play CDN.

    Component APIs use shadcn's stock variant names (`default`,
    `secondary`, `destructive`, `outline`) for badges, or semantic tone
    builders (`good_badge`, `bad_badge`, `neutral_badge`, `bool_badge`).
    Raw tone swatches live in [`color_themes.py`](./color_themes.py).
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
            Four shadcn badge variants rendered as `div` elements with
            `DivLayouts.INLINE_ROW`, shared `BORDER` chrome, and
            `BadgeVariant` surface fills (no hover — badges are static labels).
            If all four render as
            distinct pills, the full stack is live: stylesheet loaded,
            theme tokens resolved, scoped reset applied.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    Badge(label="outline", variant=BadgeVariant.OUTLINE).render(),
                    Badge(label="default", variant=BadgeVariant.DEFAULT).render(),
                    Badge(
                        label="secondary", variant=BadgeVariant.SECONDARY
                    ).render(),
                    Badge(
                        label="destructive", variant=BadgeVariant.DESTRUCTIVE
                    ).render(),
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
    ## Semantic badges — tone builders and `bool_badge`

    `good_badge()`, `bad_badge()`, and `neutral_badge()` apply
    `ToneSurface` tokens (default emphasis: soft). `bool_badge()` maps a
    boolean to good/bad polarity; pass `false_tone=SemanticTone.NEUTRAL`
    for the common `"skipped"` pill on `False`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.hstack(
                [
                    good_badge("pass").render(),
                    bad_badge("fail").render(),
                    neutral_badge("skipped").render(),
                ],
                justify="start",
                gap=0.5,
            ),
            mo.hstack(
                [
                    good_badge("pass", emphasis=ToneEmphasis.SOLID).render(),
                    bad_badge("fail", emphasis=ToneEmphasis.SOLID).render(),
                    neutral_badge("skipped", emphasis=ToneEmphasis.SOLID).render(),
                ],
                justify="start",
                gap=0.5,
            ),
            mo.hstack(
                [
                    bool_badge(True, true_label="done", false_label="skipped").render(),
                    bool_badge(
                        False,
                        true_label="done",
                        false_label="skipped",
                        false_tone=SemanticTone.NEUTRAL,
                    ).render(),
                ],
                justify="start",
                gap=0.5,
            ),
        ],
        gap=0.5,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Escape hatch: `klass=` override and `styles.py`

    Tailwind classes live in `marimo_utils.ui.styles` — layout
    (`DivLayouts`, `SpanLayouts`), typography, sizing (`IconSize`,
    `CardWidth`, `Padding`), and surface tokens (`BORDER`, `Background`,
    `BadgeVariant`). Components compose them via `cn()` (tailwind-merge).
    Pass extra utilities through `klass=` — they merge last and win within
    each Tailwind group. Only classes that were precompiled into `dr.css`
    (literals under `src/` / `nbs/`, or the safelist) actually render;
    arbitrary runtime strings are ignored.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            `Badge(klass="ring-2 ring-ring ring-offset-2")` appends extra
            utilities.             The ring color comes from `--ring` via the shadcn theme CSS,
            so the emphasis stays on-theme.
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
            `Card` they sit in a `DivLayouts.COL` section (`flex flex-col
            p-6 gap-1.5`) inside the card's `DivLayouts.COL_SHELL` stack.
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
            the same `calendar` icon at default, large.
            """),
            mo.md("---"),
            mo.hstack(
                [
                    LucideIcon(name="calendar").render(),
                    LucideIcon(name="calendar", size=IconSize.MEDIUM).render(),
                    LucideIcon(name="calendar", size=IconSize.LARGE).render(),
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
    ## Stamp builders
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
            `date_stamp(None)` renders the default empty placeholder (`---`).
            """),
            mo.md("---"),
            mo.hstack(
                [
                    date_stamp(datetime(2026, 4, 22)).render(),
                    date_stamp(None).render(),
                    project_stamp("demo-project").render(),
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


if __name__ == "__main__":
    app.run()
