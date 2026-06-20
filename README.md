# marimo-utils

Utilities for working with marimo notebooks.

## Installation

```bash
pip install marimo-utils
```

## Usage

### `marimo_utils.pydantic` — Pydantic model display in marimo

Adds marimo's `_display_` protocol to Pydantic models so the last expression in a cell renders class name, source path, and field values.

```python
from pydantic import BaseModel
from marimo_utils import add_marimo_display

@add_marimo_display()
class MyConfig(BaseModel):
    name: str
    value: int
```

When a `MyConfig` instance is the last expression in a marimo cell, it renders with the class name, source file path, and all field values.

#### Package layout (`marimo_utils`)

| Path | Role |
|---|---|
| `pydantic/` | Pydantic ↔ marimo integration — `add_marimo_display()`, `render_model()` |
| `ui/` | Styled widget + chart toolkit (see below) |

Import from `marimo_utils` or `marimo_utils.pydantic` in notebooks; internal paths may change between releases.

### `marimo_utils.ui` — Tailwind + shadcn primitives for marimo

Pydantic-backed UI primitives that render through a precompiled Tailwind stylesheet (Preflight off, scoped via `.dr-scope`) themed with shadcn/ui defaults. The package ships card components (`Card`, `CardTitle`, `CardDescription`), small composable atoms (`Badge`, `DataItem`, `Stamp`, `date_stamp`, `project_stamp`, `LabeledList`, `LucideIcon`), and a plotly-backed chart family (`BarChart`, `HeatmapChart`, `HistogramChart`, `LineChart`, `PieChart`, `ScatterChart`, `ViolinChart`) sharing a common `PlotlyChart` base. Call `bootstrap_tailwind()` once in a notebook to inject the bundled stylesheet (utilities, shadcn tokens, and scoped reset).

```python
import marimo as mo
from marimo_utils.ui import (
    BarChart,
    BarItem,
    Card,
    CardWidth,
    ChartColor,
    bootstrap_tailwind,
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
    width=CardWidth.NARROW,
).render()
```

Components use shadcn's stock variant names (`default`, `secondary`, `destructive`, `outline`). Meta rows use registry-backed stamp builders — `date_stamp()` and `project_stamp()` return a `Stamp` with configurable empty text, spacing, and icons. Charts cycle through the `--chart-1` → `--chart-5` palette by default; pin specific items with `color=ChartColor.X`. Every `PlotlyChart` subclass renders through the same contract: plotly HTML with `responsive: true` + `include_plotlyjs="cdn"`, a `.reactive()` opt-in for marimo-reactive widgets, and a `Card`-friendly transparent background. `<script>`-bearing HTML (plotly) is routed through `dr_widget.inline.ActiveHtml` so charts execute inside marimo's React tree.

See [`nbs/ui_components.py`](./nbs/ui_components.py) for a live demo of every atom, chart, and card variant side-by-side.

#### Host adapters (custom-element path)

For the light-DOM custom-element system, call `setup_host()` once per notebook to load the dr_widget runtime and precompiled styles (including a `data-tw-ready` readiness sentinel for stylesheet load — not custom-element upgrade). Render markup with `show(component)` — `mo.Html` wrapped in `.dr-scope` for parity with `plain_html_page()` and legacy `html_block()` — or build a standalone verification page with `plain_html_page(...)`.

```python
from marimo_utils.ui import MarkupComponent, plain_html_page, setup_host, show

setup_host()

hello = MarkupComponent(
    html='<dr-hello name="Ada"></dr-hello>',
    component="dr-hello",
)
show(hello)

page_html = plain_html_page(hello, title="probe")
```

Every component should expose `to_html()` and emit a `data-component` hook for verification dumps. Legacy `.render()` components remain available until migrated.

`Badge` and `Card` are the first migrated components: `Badge.to_html()` emits a `<dr-badge>` custom element; `Card.to_html()` composes `HtmlComponent` children (e.g. nested badges). Plotly charts still use `.render()` / `ActiveHtml` during migration — see the foundation proof probe.

See [`nbs/probes/host_adapters.py`](./nbs/probes/host_adapters.py) for a minimal dual-host probe and [`nbs/probes/foundation_proof.py`](./nbs/probes/foundation_proof.py) for Badge, Card composition, and Plotly-in-Card under `setup_host()`.

#### Styling conventions (`styles.py`)

Tailwind class strings are centralized in `marimo_utils.ui.styles` as named enums and constants. Components compose them with `cn()` from `drhtml` (tailwind-merge); pass per-instance overrides through each component's `klass` prop last.

| Group | Symbols | Role |
|---|---|---|
| Layout | `DivLayouts`, `SpanLayouts` | Card sections, inline rows, key/value rows, icon frame |
| Typography | `Typography` | Text size, weight, and color |
| Sizing | `IconSize`, `CardWidth`, `Padding` | Icon dimensions, card widths, badge padding |
| Surface | `BORDER`, `BADGE_FOCUS`, `Background` | Shared border/radius/shadow, focus ring, fills and hovers |
| Badges | `BadgeVariant` | Shadcn badge variants (static; no hover) |

Contributors and agents: avoid raw layout Tailwind in components; add or reuse a named enum or shared constant instead.

#### Precompiled styles (important)

Utilities are **precompiled** into `dr.css` at build time (`npm run build:css --prefix styles`). Only literal class strings scanned from `src/` and `nbs/` (plus a small safelist for documented `klass=` overrides) are included. **Arbitrary runtime `klass=` values are not compiled** unless you add them to `styles.py`, `nbs/`, or `styles/tailwind.config.js` safelist and rebuild.

To add new styling: extend `styles.py` or components (preferred), rebuild CSS, and commit the updated `dr.css`.

#### Package layout (`marimo_utils.ui`)

| Path | Role |
|---|---|
| `setup/` | Notebook bootstrap — `bootstrap_tailwind()`, `setup_host()`, and precompiled `dr.css` injection |
| `host/` | Host adapters — `show()`, `plain_html_page()`, verification seam constants |
| `core/` | HTML DSL — `drhtml` tag builders, `cn()`, `component` markup contract, `rendering` helpers |
| `styles.py` | Shared Tailwind token enums and constants |
| `components/` | UI widgets (`Card`, `Badge`, `Stamp`, …) |
| `charts/` | Plotly chart family and `colors` palette helpers |

Import from `marimo_utils.ui` in notebooks; internal paths may change between releases.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for release notes and migration guides.
