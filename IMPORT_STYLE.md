# IMPORT_STYLE — Planning doc

Opportunities to simplify `dr-llm/src/dr_llm/style/` by leveraging `mohtml`
more fully and cleaning up the CSS-string-assembly layer. Also captures
notes on introducing a typing `Protocol` to remove the `# type: ignore`
burden around mohtml.

Context recap: `dr_llm.style` is a small design-system module (tokens →
atoms → `Card` → `PoolCard`) built on `mohtml` (thin HTML DSL that
stringifies Python objects to HTML) and rendered into marimo via
`mo.Html`. Most verbosity in the module lives in f-string CSS assembly,
not in the HTML-construction layer; mohtml itself is ~60 lines and
mostly gets out of the way.

## Priority summary

| # | Opportunity | Effort | Value | Risk |
|---|-------------|--------|-------|------|
| 1 | Drop `render_html()` / `mo.Html(str(...))` wrapper | S | M | L |
| 2 | `css(**decls)` style-builder helper | S | H | L |
| 3 | Standardize trailing-`;` convention in token `.css()` | XS | M | L |
| 4 | Custom semantic tags via `mohtml.anything` | S | L-M | L |
| 5 | Typing `Protocol` for mohtml elements | S-M | M | L |
| 6 | Single `<style>` block + `klass=` per card | L | H | M |

Recommended first pass: **#1 + #2 + #3 + #5**. Revisit #6 when a second
card type exists. #4 is optional sugar.

---

## 1. Drop `render_html()` / `mo.Html(str(...))` wrapping

**Observation.** mohtml tag classes define `_repr_html_` (it returns
`__repr__`, which is the serialized HTML). Marimo's output pipeline
picks up `_repr_html_` on whatever a cell returns, so the extra
`mo.Html(str(self.render()))` layer may be redundant.

**Proposed change.** In `pool_card.py`:

```python
# Today
def render(self) -> div: ...
def render_html(self) -> mo.Html:
    return mo.Html(str(self.render()))

# Proposed
def render(self) -> div: ...   # cells can return this directly
```

**Verification required before deleting.** Smoke-test in a marimo cell:

```python
card = PoolCard(pool=..., palette=ColorPalette.default())
card.render()   # last expression in a cell
```

If it renders correctly, `render_html()` can go. Keep `mo.Html` usage
anywhere a card needs to be embedded inside an f-string with other
marimo markup — that pathway still needs the wrapper.

**Why it's worth doing.** Removes a layer of indirection, eliminates a
marimo-specific import from the innermost rendering code, and makes
`PoolCard` render-target-agnostic. The only coupling to marimo then
lives at the call site of the cell.

---

## 2. `css(**decls)` style-builder helper

**Observation.** The current pattern is f-string concatenation of CSS
fragments, repeated ~10 times across `components.py` and `card.py`:

```python
style=(
    f"margin-top: {self.spacing.sm}; "
    f"gap: {self.spacing.md}; "
    f"{LayoutToken.css(self.display_styles)}"
)
```

This is hard to scan, trailing-`;` rules are subtle, and `None` /
absent values require more f-string gymnastics.

**Proposed helper.**

```python
# style/settings.py (or a new style/css.py)
def css(*fragments: str, **decls: str | None) -> str:
    """Build a CSS declaration string.

    Accepts keyword declarations (underscores → hyphens, None skipped)
    and positional raw fragments (already-formatted `prop: value`
    strings such as LayoutToken values). Emits a canonical trailing
    semicolon iff there is content.
    """
    parts: list[str] = [
        f"{k.replace('_', '-')}: {v}"
        for k, v in decls.items()
        if v is not None
    ]
    parts.extend(f.rstrip(";").strip() for f in fragments if f)
    return "; ".join(parts) + ";" if parts else ""
```

**Impact on call sites.** The pattern above collapses to:

```python
style=css(
    margin_top=self.spacing.sm,
    gap=self.spacing.md,
    *(tok.value for tok in self.display_styles),
)
```

Each component's `render()` gets 3–6 lines shorter and an entire class
of trailing-`;` and spacing bugs goes away.

**Scope of changes.** Every call site in `card.py`, `components.py`,
and `pool_card.py` that currently assembles a `style="..."` string.
Counted occurrences: ~10–12.

---

## 3. Standardize trailing-`;` in token `.css()` methods

**Observation.** There is inconsistency today:

- `TextStyle.css(...)` → returns `"...;"` (trailing semicolon).
- `IconStyle.css(...)` → returns `"...;"` (trailing semicolon).
- `LayoutToken.css(tokens)` → returns `"...;"` iff non-empty, `""`
  otherwise.

Call sites handle this differently; some embed with a space before the
next fragment, some not. This is what creates the need for the
trailing `;` handling in the `css()` helper above.

**Proposed convention.** `.css()` methods return **CSS fragments
without trailing `;`** (e.g., `"font-size: 1rem; font-weight: 700"`).
The `css(**decls, *fragments)` builder is the one place that adds the
final `;`. This makes every `.css()` method composable.

**Files touched.** `style/settings.py` only (3 methods). Depends on #2
landing first so call sites have a unifier.

---

## 4. Custom semantic tags via `mohtml.anything`

**Observation.** `mohtml/anything.py` exposes `__getattr__` that mints
an arbitrary-named tag class on first access. You can write:

```python
from mohtml.anything import pool_card, data_item, status_badge
```

and get `<pool-card>...</pool-card>` in the HTML. Browsers render
unknown block/inline elements as generic containers (no behavioral
change), but devtools and saved HTML become dramatically more readable
— `<pool-card>` instead of `<div><div><div>...`.

**Proposed change.** Minor, cosmetic. Replace the outermost wrapper
`div` of each component with a matching semantic tag:

| Component             | Tag                 |
|-----------------------|---------------------|
| `Card.render()`       | `<dr-card>`         |
| `Title.render()`      | `<dr-card-title>`   |
| `Badge.render()`      | `<dr-badge>`        |
| `DataItem.render()`   | `<dr-data-item>`    |
| `MetaStamp` subclass  | `<dr-meta-stamp>`   |
| `LabeledList.render()`| `<dr-labeled-list>` |
| `PoolCard.header()`   | `<dr-card-header>`  |

Prefix (`dr-`) matters only if this will ever coexist with real web
components on the page.

**Why maybe not.** Adds no runtime value — it's developer-ergonomic
only, and the mohtml return type annotation becomes `div | <new class>`
which fights with the typing work in #5. Consider doing this *after*
#5 so the `Protocol` return type absorbs the change for free.

---

## 5. Typing `Protocol` for mohtml elements

**Observation.** mohtml's dynamically generated tag classes are opaque
to type checkers (`ty`, `mypy`, pyright). The `dr_llm.style` module
currently works around this with:

- `# type: ignore` on every `from mohtml import ...`
- `model_config = ConfigDict(arbitrary_types_allowed=True)` on
  `Card` and `LabeledList` (because they hold mohtml instances).
- Annotations like `-> div` that describe a dynamically-built class
  the type checker does not actually know about.

**Proposed change.** Introduce a tiny structural `Protocol` and use it
everywhere instead of concrete mohtml classes in annotations. The
protocol encodes *exactly* what the renderer relies on: string-
convertibility and `_repr_html_`.

```python
# style/protocols.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class HtmlRenderable(Protocol):
    """Anything mohtml-like: stringifies to HTML and exposes _repr_html_."""
    def __str__(self) -> str: ...
    def _repr_html_(self) -> str: ...
```

Adopt it in annotations:

```python
# Before
def render(self) -> div: ...
def icon(self) -> svg: ...
header: div | None = None

# After
def render(self) -> HtmlRenderable: ...
def icon(self) -> HtmlRenderable: ...
header: HtmlRenderable | None = None
```

**Secondary improvement.** Provide a single typed re-export module so
`# type: ignore` lives in exactly one place, not per import:

```python
# style/_mohtml.py
# Single place that absorbs the mohtml import warts.
from mohtml import (  # type: ignore[import-untyped]
    div, span, p, svg, path, rect,
)

__all__ = ["div", "span", "p", "svg", "path", "rect"]
```

Then `components.py` / `card.py` / `pool_card.py` import from
`dr_llm.style._mohtml` instead of `mohtml` directly.

**Compatibility with Pydantic.** `arbitrary_types_allowed=True` is
still required on models that *hold* mohtml instances as fields
(because Pydantic looks at the runtime class, not the annotation).
The `Protocol` is purely a type-checker affordance; it does not
satisfy Pydantic's field validation. So:

- `Card.header: HtmlRenderable | None` **still needs**
  `arbitrary_types_allowed=True`.
- `.render() -> HtmlRenderable` method annotations are pure wins.

**Open question.** Should this `Protocol` live in `dr_llm.style` or
upstream in `mohtml` itself? If it lives in mohtml, every downstream
consumer benefits. Worth raising with that repo — mohtml is small
enough that a PR adding `mohtml.HtmlRenderable` plus `py.typed` would
unblock a lot of typing pain at source.

---

## 6. Single `<style>` block + `klass=` per card (bigger refactor)

**Observation.** Every `DataItem`, `Badge`, `MetaStamp` instance
re-emits the same inline-style string on every render. This works but:

- It is the biggest chunk of the serialized HTML.
- Inline styles cannot express `:hover`, `:focus`, `@media`, or
  `light-dark()`.
- It couples visual polish to Python string assembly.

**Proposed change.** mohtml exposes a `style` tag and `klass=`
attribute. Emit one scoped `<style>` block at the top of each card
with real CSS rules, and tag elements with classes:

```python
def stylesheet(self) -> style:
    return style(f"""
      .dr-card {{ ... }}
      .dr-card-title {{ ... }}
      .dr-badge.tone-info {{ background: {self.palette.info.bg}; ... }}
      .dr-badge.tone-info:hover {{ ... }}
    """)

def render(self) -> div:
    return div(self.stylesheet(), ..., klass="dr-card")
```

**Tradeoffs.**

- **Pro:** Shorter HTML output, access to pseudo-classes and media
  queries, easier dark-mode via `light-dark()`, easier to hand-inspect.
- **Con:** CSS scoping becomes a real concern. Multiple cards on a
  page share the global stylesheet namespace; you either accept that
  `.dr-badge` is shared (good: deduplication; bad: first card's palette
  wins) or generate per-instance class suffixes (uglier).
- **Con:** Loses the current property that `PoolCard` renders to a
  totally self-contained string with no global side effects.

**Recommendation.** Defer until a second card type exists. At that
point the duplication cost is concrete and the scoping decision is
better informed by actual usage.

---

## Suggested ordering

1. #3 standardize token `.css()` return shape (tiny, enables #2).
2. #2 introduce `css()` helper, migrate all call sites.
3. #5 add `HtmlRenderable` protocol + `_mohtml.py` re-export module,
   retype signatures.
4. #1 verify marimo picks up `_repr_html_` on raw mohtml objects; if
   so, delete `render_html()`.
5. #4 (optional) swap outer `div`s for custom semantic tags.
6. #6 revisit after a second card type appears.

## Out of scope for this doc

- Any actual *new* card types (`EvalRunCard`, etc.) — covered elsewhere.
- Theming/dark-mode — enabled by #6 but not required by it.
- Replacing mohtml with another HTML DSL (FastHTML, htpy, etc.) —
  would invalidate most of the above.
