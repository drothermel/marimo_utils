import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    from pathlib import Path

    import marimo as mo

    from marimo_utils.tw import Badge, Tone, bootstrap_tailwind

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
    # Tailwind spike — `marimo_utils.tw`
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Parallel implementation of the style package using Tailwind via the
    Play CDN (`mohtml.tailwind_css()`). No token layer — pure Tailwind
    defaults. Foundation iteration renders `Badge` only, to validate that
    the CDN plus `klass=` pipeline actually applies styles end-to-end in
    marimo. The existing inline-CSS version lives in `style_components.py`
    for A/B comparison against the same demo ideas.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Control: unstyled `<span>` with Tailwind classes
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Sanity check that the CDN loaded at all — a raw `mo.Html` span
            with a handful of Tailwind utilities. If this renders as a blue
            pill, Tailwind is live in the document.
            """),
            mo.hstack(
                [
                    mo.Html(
                        '<span class="inline-block rounded-full border '
                        "border-blue-600 bg-blue-100 px-2 py-0.5 text-xs "
                        'font-semibold text-blue-700">'
                        "plain mo.Html span</span>"
                    )
                ],
                justify="start",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Badge — one per tone
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
            Five pill-shaped labels, one per tone (neutral / info / success
            / warning / danger). Tones map to Tailwind's stock color scales
            via `TONE_CLASSES` in `tw/tones.py`.
            """),
            mo.hstack(
                [
                    Badge(label="neutral", tone=Tone.NEUTRAL).render(),
                    Badge(label="info", tone=Tone.INFO).render(),
                    Badge(label="success", tone=Tone.SUCCESS).render(),
                    Badge(label="warning", tone=Tone.WARNING).render(),
                    Badge(label="danger", tone=Tone.DANGER).render(),
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
            `Badge(klass="ring-2 ring-offset-2 ring-indigo-500")` appends
            extra Tailwind utilities to the base class string. Useful for
            one-off emphasis without extending the tone system.
            """),
            mo.hstack(
                [
                    Badge(
                        label="emphasized",
                        tone=Tone.INFO,
                        klass="ring-2 ring-offset-2 ring-indigo-500",
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
