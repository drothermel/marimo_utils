# Foundation proof probe (#12): run with
#   marimo run nbs/probes/foundation_proof.py --headless --no-token -p 2719
# Playwright checks (manual):
#   - [data-tw-ready="true"] appears once styles load
#   - slider re-render updates badge label text in place
#   - [data-component="badge"] computed styles match legacy badge borders
#   - Plotly .js-plotly-plot has non-zero bounding box
#   - plotly CDN script tag appears once on the page
# Plain HTML verification:
#   - write plain_html_page(...) to /tmp/dr_foundation_probe.html and open in browser

import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")

with app.setup:
    import json
    import tempfile
    from pathlib import Path

    import marimo as mo

    from marimo_utils.ui import (
        Badge,
        BadgeVariant,
        BarChart,
        BarItem,
        Card,
        plain_html_page,
        setup_host,
        show,
    )

    LABELS = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]


@app.cell(hide_code=True)
def _():
    setup_host()
    return


@app.cell(hide_code=True)
def _():
    label_index = mo.ui.slider(
        0,
        len(LABELS) - 1,
        value=0,
        label="badge label index",
        show_value=True,
    )
    label_index
    return (label_index,)


@app.cell(hide_code=True)
def _(label_index):
    label = LABELS[label_index.value]
    badge = Badge(label=label, variant=BadgeVariant.SECONDARY)
    card = Card(
        title="Component card",
        description="Badge child rendered via **to_html()** composition.",
        content=Badge(label="nested", variant=BadgeVariant.OUTLINE),
    )
    plotly_card = Card(
        title="Plotly card",
        description="Legacy ActiveHtml chart path under setup_host().",
        content=BarChart(
            items=[
                BarItem(label="A", value=3),
                BarItem(label="B", value=5),
                BarItem(label="C", value=2),
            ],
            height=180,
        ),
    )
    page_html = plain_html_page(
        badge,
        card,
        title="Foundation proof probe",
        include_runtime=False,
    )
    probe_path = Path(tempfile.gettempdir()) / "dr_foundation_probe.html"
    probe_path.write_text(page_html, encoding="utf-8")

    mo.vstack(
        [
            mo.md("## Badge (static `to_html()` markup)"),
            mo.md(f"Selected label: **{label}**"),
            show(badge),
            mo.md("## Card + Badge (`to_html()` composition)"),
            show(card),
            mo.md("## Plotly card (legacy `.render()` / ActiveHtml)"),
            plotly_card.render(),
            mo.md(
                f"Plain-HTML probe written to `{probe_path}` "
                f"({len(page_html)} bytes). Open in a browser or drive with Playwright."
            ),
            mo.Html(
                f'<pre data-component="probe-meta" '
                f'data-props=\'{json.dumps({"path": str(probe_path)})}\'></pre>'
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
