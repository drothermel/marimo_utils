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

### `marimo_utils.ui` — Tailwind + shadcn primitives for marimo

Pydantic-backed UI primitives that render through Tailwind (Play CDN) themed with shadcn/ui defaults. The package ships small composable atoms (`Badge`, `CardTitle`, `CardDescription`, `DataItem`, `DateStamp`, `LabeledList`, `LucideIcon`, `ProjectStamp`), a flexible `Card` container, and a plotly-backed chart family (`BarChart`, `HeatmapChart`, `HistogramChart`, `LineChart`, `PieChart`, `ScatterChart`, `ViolinChart`) sharing a common `PlotlyChart` base. Call `bootstrap_tailwind()` once in a notebook to inject shadcn's CSS variables on `:root` plus the utility rules that depend on them, then load the Tailwind CDN.

```python
import marimo as mo
from marimo_utils.ui import (
    BarChart, BarItem, Card, ChartColor, bootstrap_tailwind,
)

bootstrap_tailwind()

Card(
    title="Class Distribution",
    description="Class counts across the training split",
    content=BarChart(
        items=[
            BarItem(label="Class A", value=5),
            BarItem(label="Class B", value=10),
            BarItem(label="Class C", value=5, color=ChartColor.THREE),
            BarItem(label="Class D", value=1),
        ],
        height=220,
    ),
    width="w-80",
).render()
```

Components use shadcn's stock variant names (`default`, `secondary`, `destructive`, `outline`). Charts cycle through the `--chart-1` → `--chart-5` palette by default; pin specific items with `color=ChartColor.X`. Every `PlotlyChart` subclass renders through the same contract: plotly HTML with `responsive: true` + `include_plotlyjs="cdn"`, a `.reactive()` opt-in for marimo-reactive widgets, and a `Card`-friendly transparent background. `<script>`-bearing HTML (plotly) is routed through `dr_widget.inline.ActiveHtml` so charts execute inside marimo's React tree.

See [`nbs/ui_components.py`](./nbs/ui_components.py) for a live demo of every atom, chart, and card variant side-by-side.

#### Styling conventions (`styles.py`)

Tailwind class strings are centralized in `marimo_utils.ui.styles` as `StrEnum` groups. Components compose them with `cn()` from `drhtml` (tailwind-merge); pass per-instance overrides through each component's `klass` prop last.

- **This pass:** `DivLayouts` (card sections, inline rows, key/value rows), `SpanLayouts` (label column, icon frame), and `BadgeVariant` (shadcn badge colors).
- **Planned next passes** in `styles.py`: `Surface` (border, background, shadow, radius), optional `Sizing` (named widths and icon sizes). `Typography` (text size/weight/color) is implemented.

Contributors and agents: avoid raw layout Tailwind in components; add or reuse a named enum instead.

## Changes

### 0.6.0 — Tailwind + shadcn UI package

- **Breaking:** removes `marimo_utils.style` (the inline-CSS design system) and renames the Tailwind implementation from `marimo_utils.tw` to the canonical `marimo_utils.ui`.
- Adds `ScatterChart` / `ScatterSeries` and `LineChart` / `LineSeries` (with solid/dotted/dashed styling via `LineDash`) — multi-series numeric-axis charts that accept `x_range` and `y_range`.
- Every chart section in `nbs/ui_components.py` now renders both a standalone chart and a Card-wrapped variant via `mo.hstack`, exercising the shadow-DOM embedding path uniformly.
- Renames the demo notebook from `nbs/style_components_tw.py` to `nbs/ui_components.py`.

**Migration from 0.5.x.** The rename is not purely syntactic — `marimo_utils.ui` uses shadcn's stock variant names (`default`, `secondary`, `destructive`, `outline`) instead of the old tone palette, and charts use `ChartColor.ONE..FIVE` instead of `PaletteToneName`. Common translations:

| 0.5.x (`marimo_utils.style`) | 0.6.0 (`marimo_utils.ui`) |
|---|---|
| `from marimo_utils.style import ...` | `from marimo_utils.ui import ...` |
| `Style.default()` / passing `style=...` | removed — call `bootstrap_tailwind()` once per notebook |
| `Title(drop_text=..., text=...)` | `CardTitle(text=...)` + `CardDescription(text=...)` |
| `PaletteToneName.SUCCESS` / `.WARNING` / `.DANGER` | `ChartColor.ONE..FIVE` (neutral categorical palette) |
| `Style.tone_colorscale(tone)` | `chart_colorscale(ChartColor.X)` |
| `Card(style=..., width="22rem", height="22rem", title=..., content=...)` | `Card(title=..., description=..., content=..., width="w-80").render()` (Tailwind width utilities) |
| Chart `height=None` for responsive fill inside a sized `Card` | Charts have fixed default heights; pass explicit `height=220` for in-card use |

See [`nbs/ui_components.py`](./nbs/ui_components.py) for current usage of every atom and chart.

### 0.5.0

- Adds four Card-ready chart primitives alongside `PieChart`: `BarChart` / `BarItem`, `HistogramChart`, `ViolinChart` / `ViolinGroup`, `HeatmapChart`. All share per-tone palette colors via `PaletteToneName` and plug into `Card` the same way `PieChart` does.
- Refactors the charts module into a subpackage with a shared `PlotlyChart` base that owns `_repr_html_`, `__str__`, `reactive()`, empty-state rendering, and dimension application. Subclasses implement only `_has_data` and `_build_figure`.
- Adds a two-stop `[bg → border]` sequential colorscale helper for heatmap / choropleth use.
- Turns on plotly responsive mode by default (`PlotlyChart.responsive = True`, config passed to `pio.to_html`). Charts now default to `width=None` (fill container) and resize with their wrapper.
- Adds `Card.height` so cards become a `display: flex; flex-direction: column` container and responsive charts fill the remaining vertical space.

### 0.4.0

- Routes `<script>`-bearing HTML fragments (notably Plotly) through `dr_widget.inline.ActiveHtml` so Plotly charts render inside a `Card` even though marimo's React tree strips inline scripts.
- Drops the local `_active_html.py` copy; `ActiveHtml` now lives in the `dr-widget` package.
- Adds `dr-widget` as a dependency.

### 0.3.0

- Hard-cuts the design package to a notebook-native render contract for marimo notebooks.
- Keeps `mohtml` as the HTML authoring layer for styled atoms while making `Card` slots compatible with native notebook outputs.
- Adds reusable pie-chart primitives (`PieChart`, `PieSlice`) for chart-in-card composition.
