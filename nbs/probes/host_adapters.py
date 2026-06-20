# Host adapter probe (#11): run with
#   marimo run nbs/probes/host_adapters.py --headless --no-token -p 2718
# Playwright checks (manual):
#   - customElements.get("dr-hello") is defined after setup_host()
#   - [data-tw-ready="true"] appears once styles load
#   - slider re-render updates dr-hello name attribute in place
# Plain HTML verification:
#   - write plain_html_page(...) to /tmp/dr_probe.html and open in browser

import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")

with app.setup:
    import json
    import tempfile
    from pathlib import Path

    import marimo as mo

    from marimo_utils.ui import MarkupComponent, plain_html_page, setup_host, show

    NAMES = ["Ada", "Grace", "Alan", "Katherine", "Tim", "World"]


@app.cell(hide_code=True)
def _():
    setup_host()
    return


@app.cell(hide_code=True)
def _():
    name_index = mo.ui.slider(
        0,
        len(NAMES) - 1,
        value=0,
        label="name index",
        show_value=True,
    )
    name_index
    return (name_index,)


@app.cell(hide_code=True)
def _(name_index):
    name = NAMES[name_index.value]
    hello = MarkupComponent(
        html=f'<dr-hello name="{name}"></dr-hello>',
        component="dr-hello",
    )
    page_html = plain_html_page(hello, title="Host adapter probe", include_runtime=True)
    probe_path = Path(tempfile.gettempdir()) / "dr_host_adapter_probe.html"
    probe_path.write_text(page_html, encoding="utf-8")

    mo.vstack(
        [
            mo.md(f"Selected name: **{name}**"),
            show(hello),
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
