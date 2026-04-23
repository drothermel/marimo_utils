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

A small design-system for rendering Pydantic-backed inspection cards in marimo notebooks. The style system is notebook-native: components return marimo renderables, cards can host both styled HTML fragments and native notebook outputs, and [`mohtml`](https://github.com/koaning/mohtml) remains the HTML authoring tool for the styled atoms. The package includes tokens (`ColorPalette`, `Typography`, `SpacingScale`), atoms (`Badge`, `Title`, `DataItem`, `DateStamp`, `ProjectStamp`, `LabeledList`, `MetaStamp`), a flexible `Card` container, and reusable chart primitives (`PieChart`, `PieSlice`).

```python
import marimo as mo
from marimo_utils.style import (
    Badge, Card, ColorPalette, PaletteToneName,
    PieChart, PieSlice, SpacingScale, Title, Typography,
)

palette = ColorPalette.default()
typography = Typography.default()
spacing = SpacingScale.default()

card = Card(
    palette=palette,
    typography=typography,
    spacing=spacing,
    title=Title(
        palette=palette,
        typography=typography,
        spacing=spacing,
        drop_text="Pool Card",
        text="demo pool",
    ).render(),
    header=Badge(
        palette=palette,
        typography=typography,
        spacing=spacing,
        label="complete",
        tone=PaletteToneName.SUCCESS,
    ).render(),
    content=PieChart(
        palette=palette,
        slices=[
            PieSlice(label="Samples", value=120, tone=PaletteToneName.SUCCESS),
            PieSlice(label="Pending", value=18, tone=PaletteToneName.WARNING),
            PieSlice(label="Failed", value=3, tone=PaletteToneName.DANGER),
        ],
    ).render(),
)

card.render()
```

See [`IMPORT_STYLE.md`](./IMPORT_STYLE.md) for design notes on the mohtml leverage points and CSS helper.

## Changes

### 0.4.0

- Routes `<script>`-bearing HTML fragments (notably Plotly) through `dr_widget.inline.ActiveHtml` so Plotly charts render inside a `Card` even though marimo's React tree strips inline scripts.
- Drops the local `_active_html.py` copy; `ActiveHtml` now lives in the `dr-widget` package.
- Adds `dr-widget` as a dependency.

### 0.3.0

- Hard-cuts `marimo_utils.style` to a notebook-native render contract for marimo notebooks.
- Keeps `mohtml` as the HTML authoring layer for styled atoms while making `Card` slots compatible with native notebook outputs.
- Adds reusable pie-chart primitives (`PieChart`, `PieSlice`) for chart-in-card composition.
