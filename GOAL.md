# GOAL: Light-DOM Custom-Element Component System

A reusable UI component system that renders **identically on a plain web page and
in a marimo notebook**, survives marimo's reactive re-rendering, and is
**observable enough to debug visually without guesswork**. This is the foundation
for a year of work centered on code modification, viewing, diffing, and manual
data labeling.

## Why

Prior versions of this system have been rebuilt several times; each new component
type surfaces a new class of issue (styling, layering, clipping, script
execution, state loss on re-render). The root causes:

- Host concerns (style loading, script execution, display wrapping) are tangled
  *into* components instead of living at the boundary.
- The marimo rendering path forces a tradeoff: `mo.Html` is light DOM but strips
  scripts; anywidget runs scripts but inside a **shadow DOM** that blocks global
  styles and `getElementById` (requiring re-injection hacks).
- The debug loop is an unobservable multi-stage pipeline (perceive → goal → diff
  → diagnose → fix), so a wrong result can't be localized to a stage.

## Architecture

**Custom elements rendered into light DOM, behind a host-agnostic boundary, with
one shared runtime loaded once per host.**

```
Component (Python)  →  to_html()  →  "<dr-code data-props='...'>...</dr-code>"   [pure markup]
Runtime (React, built once)        →  defines <dr-*>, mounts React in light DOM   [behavior]
marimo host  →  load runtime once + show(c) = mo.Html(c.to_html())
web host     →  <script>runtime</script> + <link>css</link> + the same markup
```

- **Markup is the interface.** Components emit plain HTML strings with `<dr-*>`
  custom-element tags + `data-*` attributes. The same markup works in both hosts.
- **Custom elements are the boundary, React is the implementation.** Each element
  is a thin React mount point: `connectedCallback` creates a React root in its own
  light-DOM children; `attributeChangedCallback` re-renders with new props;
  `disconnectedCallback` unmounts. Libraries (Shiki, CodeMirror 6, dnd-kit) live
  inside, behind a consistent component family + engine-adapter seam.
- **Web Components à la carte:** we use the *Custom Elements* API and deliberately
  **skip Shadow DOM** (default) so global styles cascade and there is no clipping
  confound. Shadow DOM remains an optional per-component opt-in for CSS isolation.
- **dr_widget** hosts the runtime: a tiny inline "define-once loader" plus a
  React bundled workspace (Vite/bun). dr_widget is ours to change.

## Verified findings (from spikes)

All confirmed by live `marimo run` + Playwright against Chrome:

- `mo.Html` renders into **light DOM** (`getElementById` reaches it); custom
  elements, `data-*`, classes, SVG, and nested content all survive
  `html-react-parser`. Inline `<script>` does **not** execute via `mo.Html`.
- Custom elements **upgrade live** under marimo reactivity; a define-once global
  loader from a single `ActiveHtml` registers in the window-global registry.
- On a reactive re-render, **React patches the existing node in place** and updates
  `data-*` as real attributes — it does **not** recreate the element.
- Plotly works as a light-DOM custom element: draws, sizes correctly,
  `getElementById` finds its node natively (the shadow-walk patch is unnecessary).
- Components **depend on Tailwind Preflight** (without it, `border` utilities render
  `border-style:none` → invisible borders; box model shifts to content-box). The
  Play CDN **silently ignores** `corePlugins.preflight:false`.
- Web ↔ marimo **visual parity** of the same markup is confirmed (colors, borders,
  radius, box-sizing, typography match).

## Design rules

1. **Render from `attributeChangedCallback` (+ declare `observedAttributes`), never
   only `connectedCallback`.** React reuses the node across re-renders, so
   `connectedCallback` fires once; prop changes arrive only as attribute changes.
2. **Never measure geometry in `connectedCallback`** (`clientWidth` can be 0 before
   layout). Defer via `requestAnimationFrame` / `ResizeObserver`.
3. **Transient view-state (page index, scroll, selection, expand) lives in the
   component (JS), never as a marimo UI element** — otherwise navigation
   re-executes Python and tears the component down.
4. **Keep page navigation client-side; deliver data via a side channel** that pushes
   into the live component without a full re-render.

## Styling system

Stop using the Tailwind Play CDN for production (it ships global Preflight you
can't disable and restyles the whole notebook). Instead:

- **Precompile Tailwind** (CLI) with Preflight off, only the classes we use, into
  one static stylesheet shipped to both hosts.
- Add a scoped reset under `.dr-scope` that re-supplies the three behaviors our
  components rely on: `box-sizing:border-box`, `border-width:0; border-style:solid`,
  and heading/`p` margin resets.
- Fix the non-standard `w-100` utility (Tailwind's scale stops at `w-96`).

## Data delivery

- **Small data** → JSON in a `data-*` attribute, parsed in `attributeChangedCallback`.
- **Large/structured data** (e.g. ~200 `Output`s) → a JS-side data channel: Python
  emits a small id/handle; the runtime holds the payload. Avoid stuffing megabytes
  of JSON into DOM attributes. This is the same channel the Python-paged carousel uses.

## Verification loop

Manual now, designed for eventual automation. Three perception channels:

1. **Deterministic property dump** — computed styles / classes on a `data-component`
   element. No vision needed; a weak agent can read it.
2. **Geometric / clip audit** — `getBoundingClientRect` + `overflow` + `border-radius`
   + stacking context across the ancestor chain. Distinguishes clip vs sizing vs
   layering bugs (the "introspection looks fine but it's visibly wrong" class).
3. **Vision** — only for genuinely aesthetic judgment (spacing, balance).

Seams to bake in: `data-*` hooks on every component, a `data-tw-ready` readiness
sentinel, and a **plain-HTML render adapter** (dual purpose: web reuse + the
verification surface; rendering both ways isolates component vs embedding bugs).

## Probe suite + acceptance bar

The system is validated by building a diverse set of probes. Each must work
**on web and in marimo**, and **survive re-render** — defined as: (i) does not
visually break, (ii) preserves transient view-state where it should, (iii)
unmounts with no leaks.

| Probe | Axis stressed |
| --- | --- |
| Plotly card | third-party script draw + sizing + CDN dedup |
| Shiki code viewer | data → static highlighted DOM + theming (+ shadow opt-in) |
| CodeMirror 6 display editor | client-only mutable state surviving re-render |
| DnD good/bad sorter | heavy pointer interaction, cross-region, global listeners |
| Paginated OutputCard carousel | transient view-state + data across the Python boundary; nesting; scale |

The carousel is **content-agnostic** (paginates arbitrary children, page-of-N,
client-owned page index); OutputCards are its first payload. Client-windowed first
(immediately useful), Python-paged second (the sync-seam test). The carousel /
windowing is also the real answer to the original "render overload" problem.

## Phased plan

Migration is **additive/incremental**: the new runtime coexists with existing
`mo.Html` components, which keep rendering untouched while we migrate one at a time.

- **Phase 0 — Foundation:** dr_widget runtime host (loader + React build);
  custom-element base pattern + data contract; styling swap (precompiled Tailwind
  + `.dr-scope`); host adapters + verification seams; prove via Badge + Plotly.
- **Phase 1 — Notebook reorg:** `nbs/components/{primitives,charts,cards,color_themes}.py`
  + shared fixtures.
- **Phase 2 — Semantic tokens:** good/bad/neutral × soft/solid color tokens;
  semantic badge builders + `bool_badge`.
- **Phase 3 — Probe suite:** Shiki viewer; carousel mechanism; OutputCard; ReportV0
  client-windowed carousel; CM6 editor; DnD sorter.
- **Phase 4 — Python sync:** comm-bridge design/spike; Python-paged carousel mode.
- **Phase 5 — Migration & cleanup:** port remaining charts; residual boundary/styling
  cleanup.

## Deferred / open

- **Python state-sync bridge** (single anywidget comm channel) — first used by
  Python-paged pagination; the foundation for future labeling/config-building.
  Design before the labeling phase; tension between anywidget (clean sync, but
  per-instance shadow DOM) and light-DOM React (needs a custom event bridge).
- **Shadow-DOM opt-in** for components whose library CSS proves unruly.
- **Engine consolidation:** design for pluggable code engines, but prefer
  standardizing on CodeMirror 6 where possible to limit bundle size and maintenance.
