# marimo-utils

Utilities for working with marimo notebooks.

## Installation

```bash
pip install marimo-utils
```

## Usage

### `@add_marimo_display()` decorator

Adds a `_display_` method to Pydantic models for rich rendering in marimo notebooks.

```python
from pydantic import BaseModel
from marimo_utils import add_marimo_display

@add_marimo_display()
class MyConfig(BaseModel):
    name: str
    value: int
```

When a `MyConfig` instance is the last expression in a marimo cell, it renders with the class name, source file path, and all field values.

### `marimo_utils.style` — notebook-native design primitives

A small design-system for rendering Pydantic-backed inspection cards in marimo notebooks. The style system is notebook-native: components return marimo renderables, cards can host both styled HTML fragments and native notebook outputs, and [`mohtml`](https://github.com/koaning/mohtml) remains the HTML authoring tool for the styled atoms. The package includes tokens (`Style`, `ColorPalette`, `Typography`, `SpacingScale`), atoms (`Badge`, `Title`, `DataItem`, `DateStamp`, `ProjectStamp`, `LabeledList`, `MetaStamp`), a flexible `Card` container, and a plotly-backed chart family (`PieChart`, `BarChart`, `HistogramChart`, `ViolinChart`, `HeatmapChart`) that share a common `PlotlyChart` base.

```python
from marimo_utils.style import (
    BarChart, BarItem, Card, PaletteToneName, Style, Title,
)

style = Style.default()

card = Card(
    style=style,
    width="22rem",
    height="22rem",  # optional; omit for unconstrained height
    title=Title(
        style=style,
        drop_text="Bar Card",
        text="Class Distribution",
    ).render(),
    content=BarChart(
        style=style,
        height=None,  # responsive: fills remaining vertical space in the card
        items=[
            BarItem(label="Samples", value=120, tone=PaletteToneName.SUCCESS),
            BarItem(label="Pending", value=18, tone=PaletteToneName.WARNING),
            BarItem(label="Failed", value=3, tone=PaletteToneName.DANGER),
        ],
    ),
).render()
```

Every `PlotlyChart` subclass renders through the same contract: plotly HTML with `responsive: true` + `include_plotlyjs="cdn"`, a `.reactive()` opt-in for marimo-reactive widgets, and a tone-driven palette (`PaletteToneName`) that unifies colors across atoms and charts. `Style.tone_colorscale(tone)` provides a matching sequential gradient for heatmaps. `Card` accepts any `HtmlRenderable` as `content`; `<script>`-bearing HTML (plotly) is routed through `dr_widget.inline.ActiveHtml` so charts execute inside marimo's React tree.

**Sizing model.** Charts default to `width=None` (fill container) with `responsive=True`, and each chart type keeps a sensible fixed `height`. Pass explicit ints to pin either dimension; pass `height=None` to let plotly fill a constrained `Card(height=...)` vertically.

See [`nbs/style_components.py`](./nbs/style_components.py) for a live demo of every atom, chart, and card variant, and [`IMPORT_STYLE.md`](./IMPORT_STYLE.md) for design notes on the mohtml leverage points and CSS helper.

## Changes

### 0.5.0

- Adds four Card-ready chart primitives alongside `PieChart`: `BarChart` / `BarItem`, `HistogramChart`, `ViolinChart` / `ViolinGroup`, `HeatmapChart`. All share per-tone palette colors via `PaletteToneName` and plug into `Card` the same way `PieChart` does.
- Refactors `marimo_utils.style.charts` into a subpackage with a shared `PlotlyChart` base that owns `_repr_html_`, `__str__`, `reactive()`, empty-state rendering, and dimension application. Subclasses implement only `_has_data` and `_build_figure`. Public imports are unchanged — everything is still re-exported from `marimo_utils.style`.
- Adds `Style.tone_colorscale(tone)` — a two-stop `[bg → border]` sequential colorscale for heatmap / choropleth use.
- Turns on plotly responsive mode by default (`PlotlyChart.responsive = True`, config passed to `pio.to_html`). Charts now default to `width=None` (fill container) and resize with their wrapper.
- Adds `Card.height: str | None = None` (CSS value). When set, the card becomes a `display: flex; flex-direction: column` container and wraps its content region with `flex: 1 1 auto; min-height: 0` so a responsive chart (`height=None`) fills the remaining vertical space below the title and header.

### 0.4.0

- Routes `<script>`-bearing HTML fragments (notably Plotly) through `dr_widget.inline.ActiveHtml` so Plotly charts render inside a `Card` even though marimo's React tree strips inline scripts.
- Drops the local `_active_html.py` copy; `ActiveHtml` now lives in the `dr-widget` package.
- Adds `dr-widget` as a dependency.

### 0.3.0

- Hard-cuts `marimo_utils.style` to a notebook-native render contract for marimo notebooks.
- Keeps `mohtml` as the HTML authoring layer for styled atoms while making `Card` slots compatible with native notebook outputs.
- Adds reusable pie-chart primitives (`PieChart`, `PieSlice`) for chart-in-card composition.
