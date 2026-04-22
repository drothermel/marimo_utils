import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")

with app.setup:
    import marimo as mo
    from pathlib import Path

    from pydantic import BaseModel

    from marimo_utils import add_marimo_display

    NOTEBOOK_PATH = Path(__file__).resolve()
    REPO_ROOT = NOTEBOOK_PATH.parent.parent
    SRC_ROOT = REPO_ROOT / "src"
    PACKAGE_ROOT = SRC_ROOT / "marimo_utils"


@app.class_definition
@add_marimo_display()
class DemoStyleComponent(BaseModel):
    name: str
    variant: str
    css_classes: list[str]
    notes: str
    repo_root: Path


@app.cell(column=1, hide_code=True)
def _():
    mo.md(r"""
    ## Style Components
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Starter notebook for exploring `marimo_utils` display behavior and styling
    ideas. The left column holds setup, paths, and reusable definitions. The
    center column is for previews and experiments.
    """)
    return


@app.cell(hide_code=True)
def _():
    DemoStyleComponent(
        name="SectionTitle",
        variant="headline",
        css_classes=["stack", "gap-2", "font-semibold"],
        notes="Starter object for testing marimo rich display in this notebook.",
        repo_root=REPO_ROOT,
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
