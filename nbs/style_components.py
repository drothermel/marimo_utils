import marimo

__generated_with = "0.23.2"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    from pathlib import Path

    from pydantic import BaseModel

    from marimo_utils import add_marimo_display, render_model

    return BaseModel, Path, add_marimo_display, mo


@app.cell
def _(Path):
    notebook_path = Path(__file__).resolve()
    repo_root = notebook_path.parent.parent
    src_root = repo_root / "src"
    package_root = src_root / "marimo_utils"
    return notebook_path, package_root, repo_root


@app.cell
def _(BaseModel, Path, add_marimo_display):
    @add_marimo_display()
    class DemoStyleComponent(BaseModel):
        name: str
        variant: str
        css_classes: list[str]
        notes: str
        repo_root: Path

    return (DemoStyleComponent,)


@app.cell(column=2)
def _(DemoStyleComponent, mo, repo_root):
    is_script_mode = mo.app_meta().mode == "script"

    demo_component = DemoStyleComponent(
        name="SectionTitle",
        variant="headline",
        css_classes=["stack", "gap-2", "font-semibold"],
        notes="Starter object for testing marimo rich display in this notebook.",
        repo_root=repo_root,
    )
    return demo_component, is_script_mode


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # style_components

    Starter notebook for exploring `marimo_utils` display behavior and styling
    ideas. The left column holds setup, paths, and reusable definitions. The
    center column is for previews and experiments.
    """)
    return


@app.cell(hide_code=True)
def _(demo_component):
    demo_component
    return


@app.cell(hide_code=True)
def _(is_script_mode, notebook_path, package_root, repo_root):
    {
        "mode": "script" if is_script_mode else "interactive",
        "notebook_path": notebook_path.relative_to(repo_root),
        "package_root": package_root.relative_to(repo_root),
    }
    return


@app.cell(column=3, hide_code=True)
def _():
    spacer_column = 3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    leave space
    """)
    return


if __name__ == "__main__":
    app.run()
