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

### `marimo_utils.style` — design-system primitives

A small design-system for rendering Pydantic-backed "inspection cards" in marimo notebooks, built on [`mohtml`](https://github.com/koaning/mohtml). Tokens (`ColorPalette`, `Typography`, `SpacingScale`), atoms (`Badge`, `Title`, `DataItem`, `DateStamp`, `ProjectStamp`, `LabeledList`, `MetaStamp`), a `Card` composer, a `css()` style-builder helper, and an `HtmlRenderable` protocol for typing mohtml-produced values.

```python
import marimo as mo
from marimo_utils.style import (
    Badge, Card, ColorPalette, PaletteToneName,
    SpacingScale, Title, Typography,
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
    ),
    header=Badge(
        palette=palette,
        typography=typography,
        spacing=spacing,
        label="complete",
        tone=PaletteToneName.SUCCESS,
    ).render(),
)

mo.Html(str(card.render()))
```

See [`IMPORT_STYLE.md`](./IMPORT_STYLE.md) for design notes on the mohtml leverage points and CSS helper.

## Changes

### 0.2.0

- Adds `marimo_utils.style` submodule (`Card`, tokens, atoms, `css()` helper, `HtmlRenderable` protocol).
- Adds `mohtml>=0.1.11` runtime dependency.
