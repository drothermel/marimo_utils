import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    from pathlib import Path

    import marimo as mo

    from marimo_utils.tw import Badge, BadgeVariant, bootstrap_tailwind

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
    themed with shadcn/ui defaults. `bootstrap_tailwind()` injects three
    things into the document in order: shadcn's CSS variables on `:root`
    (zinc light mode), a Tailwind config extension that maps utilities
    like `bg-primary` and `border-border` to those variables, and the
    Tailwind CDN itself.

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
            mo.hstack(
                [
                    Badge(label="default", variant=BadgeVariant.DEFAULT).render(),
                    Badge(label="secondary", variant=BadgeVariant.SECONDARY).render(),
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
            mo.hstack(
                [
                    Badge(
                        label="emphasized",
                        variant=BadgeVariant.DEFAULT,
                        klass="ring-2 ring-ring ring-offset-2",
                    ).render()
                ],
                justify="start",
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
