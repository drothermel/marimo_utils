# Changelog

All notable changes to this project are documented here.

## Unreleased

- Adds semantic badge builders — `good_badge()`, `bad_badge()`, `neutral_badge()`, and `bool_badge()` — that consume Phase 2 tone tokens via `tone_surface()`.
- Splits the monolithic `nbs/ui_components.py` demo into `nbs/components/{primitives,cards,charts,color_themes}.py` and extracts seed-42 synthetic fixtures into `nbs/fixtures/synthetic.py`.
- Adds semantic tone tokens (`good` / `bad` / `neutral` × `soft` / `solid`) as scoped CSS variables and precompiled utilities in `dr.css`, with `SemanticTone`, `ToneEmphasis`, `ToneSurface`, `ToneBorder`, and lookup helpers in `styles.py`.
- Adds foundation proof (probe #1): static `Badge.to_html()` → pure markup with `data-component="badge"`, `Card.to_html()` composition, and `nbs/probes/foundation_proof.py` validating web + marimo + re-render under `setup_host()`. Plotly-in-Card still uses legacy `ActiveHtml` (`dr-plotly` deferred).
- Adds host adapters: `setup_host()`, `show()` (`mo.Html(c.to_html())`), and `plain_html_page()` for web reuse and Playwright verification.
- Adds component markup contract (`HtmlComponent`, `MarkupComponent`, `data-component` hooks) and a `data-tw-ready` readiness sentinel in bootstrap and plain-HTML pages.
- **Breaking:** replaces the Tailwind Play CDN with a precompiled, scoped `dr.css` shipped in the wheel (Preflight off; all utilities and shadcn rules scoped under `.dr-scope`). `bootstrap_tailwind()` injects the bundled stylesheet once per page instead of loading `cdn.tailwindcss.com`.
- Defines `w-100` (25rem) and `w-160` (40rem) in the Tailwind build; `CardWidth.DEFAULT` / `.WIDE` now resolve correctly.
- Adds `styles/` build pipeline (`npm run build:css --prefix styles`) and `setup/stylesheet.py` for runtime loading and web-host path access.

## 0.8.1 — Style tokens, stamps, and surface chrome

- **Breaking:** removes `DateStamp` / `ProjectStamp` classes in favor of registry-backed builders — `date_stamp()`, `project_stamp()`, and `Stamp`. Empty values render `"---"` by default (was `"--- --"` on dates).
- **Breaking:** removes `BADGE_BASE`; badge chrome is composed from `BORDER`, `BADGE_FOCUS`, and `Padding.BADGE` in `badge.py`.
- Adds `Stamp`, `StampKind`, `STAMP_PRESETS`, and `@register_stamp` for import-time stamp presets.
- Adds `IconSize`, `CardWidth`, `Padding`, `Background`, `BORDER`, and `BADGE_FOCUS` to `styles.py`; `BadgeVariant` now aliases `Background` (including `outline` with accent hover).
- Cards and badges share `BORDER` chrome (`border-border`, `rounded-md`, `shadow-sm`); card default width is `CardWidth.DEFAULT` (`w-100`).
- Renames `theme.py` → `setup/shadcn_theme.py`; extends injected theme CSS with outline-badge hover utilities.
- `Card`, `CardTitle`, and `CardDescription` live in `components/card.py`; chart palette helpers live in `charts/colors.py`.

### Migration from 0.7.x

| 0.7.x | 0.8.0 |
|---|---|
| `DateStamp(value=dt).render()` | `date_stamp(dt).render()` |
| `ProjectStamp(project_name="x").render()` | `project_stamp("x").render()` |
| `from marimo_utils.ui import BADGE_BASE` | `BORDER`, `BADGE_FOCUS`, `Padding.BADGE` |
| `Card(..., width="w-72")` | `Card(..., width=CardWidth.DEFAULT)` or `CardWidth.NARROW` / `.WIDE` |
| `LucideIcon(size="h-4 w-4")` | `LucideIcon(size=IconSize.SMALL)` (default unchanged) |

See the demo notebooks under [`nbs/components/`](./nbs/components/) for current usage of every atom and chart.

## 0.6.0 — Tailwind + shadcn UI package

- **Breaking:** removes `marimo_utils.style` (the inline-CSS design system) and renames the Tailwind implementation from `marimo_utils.tw` to the canonical `marimo_utils.ui`.
- Adds `ScatterChart` / `ScatterSeries` and `LineChart` / `LineSeries` (with solid/dotted/dashed styling via `LineDash`) — multi-series numeric-axis charts that accept `x_range` and `y_range`.
- Every chart section in the demo notebooks under `nbs/components/` now renders both a standalone chart and a Card-wrapped variant via `mo.hstack`, exercising the shadow-DOM embedding path uniformly.
- Renames the demo notebook from `nbs/style_components_tw.py` to `nbs/ui_components.py` (later split into `nbs/components/*` in Phase 1).

### Migration from 0.5.x

The rename is not purely syntactic — `marimo_utils.ui` uses shadcn's stock variant names (`default`, `secondary`, `destructive`, `outline`) instead of the old tone palette, and charts use `ChartColor.ONE..FIVE` instead of `PaletteToneName`. Common translations:

| 0.5.x (`marimo_utils.style`) | 0.6.0 (`marimo_utils.ui`) |
|---|---|
| `from marimo_utils.style import ...` | `from marimo_utils.ui import ...` |
| `Style.default()` / passing `style=...` | removed — call `bootstrap_tailwind()` once per notebook |
| `Title(drop_text=..., text=...)` | `CardTitle(text=...)` + `CardDescription(text=...)` |
| `PaletteToneName.SUCCESS` / `.WARNING` / `.DANGER` | `ChartColor.ONE..FIVE` (neutral categorical palette) |
| `Style.tone_colorscale(tone)` | `chart_colorscale(ChartColor.X)` |
| `Card(style=..., width="22rem", height="22rem", title=..., content=...)` | `Card(title=..., description=..., content=..., width=CardWidth.NARROW).render()` |
| Chart `height=None` for responsive fill inside a sized `Card` | Charts have fixed default heights; pass explicit `height=220` for in-card use |

See the demo notebooks under [`nbs/components/`](./nbs/components/) for current usage of every atom and chart.

## 0.5.0

- Adds four Card-ready chart primitives alongside `PieChart`: `BarChart` / `BarItem`, `HistogramChart`, `ViolinChart` / `ViolinGroup`, `HeatmapChart`. All share per-tone palette colors via `PaletteToneName` and plug into `Card` the same way `PieChart` does.
- Refactors the charts module into a subpackage with a shared `PlotlyChart` base that owns `_repr_html_`, `__str__`, `reactive()`, empty-state rendering, and dimension application. Subclasses implement only `_has_data` and `_build_figure`.
- Adds a two-stop `[bg → border]` sequential colorscale helper for heatmap / choropleth use.
- Turns on plotly responsive mode by default (`PlotlyChart.responsive = True`, config passed to `pio.to_html`). Charts now default to `width=None` (fill container) and resize with their wrapper.
- Adds `Card.height` so cards become a `display: flex; flex-direction: column` container and responsive charts fill the remaining vertical space.

## 0.4.0

- Routes `<script>`-bearing HTML fragments (notably Plotly) through `dr_widget.inline.ActiveHtml` so Plotly charts render inside a `Card` even though marimo's React tree strips inline scripts.
- Drops the local `_active_html.py` copy; `ActiveHtml` now lives in the `dr-widget` package.
- Adds `dr-widget` as a dependency.

## 0.3.0

- Hard-cuts the design package to a notebook-native render contract for marimo notebooks.
- Keeps `mohtml` as the HTML authoring layer for styled atoms while making `Card` slots compatible with native notebook outputs.
- Adds reusable pie-chart primitives (`PieChart`, `PieSlice`) for chart-in-card composition.
