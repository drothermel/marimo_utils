"""Host-agnostic component markup contract."""

from __future__ import annotations

import html
import json
from typing import Protocol

from pydantic import BaseModel, ConfigDict

DATA_COMPONENT = "data-component"
DATA_PROPS = "data-props"
DR_SCOPE_CLASS = "dr-scope"


def wrap_dr_scope(markup: str) -> str:
    """Wrap markup so precompiled styles and design tokens apply."""
    return f'<div class="{DR_SCOPE_CLASS}">{markup}</div>'


class HtmlComponent(Protocol):
    """Pure markup producer for marimo and plain-HTML hosts."""

    def to_html(self) -> str: ...


def verification_attrs(*, component: str, **extra: str) -> dict[str, str]:
    """Build ``data-component`` and optional verification ``data-*`` hooks."""
    attrs = {DATA_COMPONENT: component}
    attrs.update(extra)
    return attrs


def format_data_attrs(attrs: dict[str, str]) -> str:
    """Serialize verification attrs for embedding in an HTML opening tag."""
    return " ".join(
        f'{key}="{html.escape(value, quote=True)}"' for key, value in attrs.items()
    )


def data_props_attr(props: dict[str, object]) -> str:
    """JSON-encode small props for a ``data-props`` attribute value."""
    return json.dumps(props, separators=(",", ":"))


class MarkupComponent(BaseModel):
    """Frozen wrapper for raw custom-element markup during probes and migration."""

    model_config = ConfigDict(frozen=True)

    html: str
    component: str | None = None

    def to_html(self) -> str:
        if self.component is None:
            return self.html
        marker = f'{DATA_COMPONENT}="{html.escape(self.component, quote=True)}"'
        if self.html.startswith("<") and ">" in self.html:
            tag_end = self.html.index(">")
            opening = self.html[:tag_end]
            if marker in opening:
                return self.html
            rest = self.html[tag_end:]
            if opening.endswith("/"):
                insert_at = len(opening) - 1
                opening = f"{opening[:insert_at]} {marker}{opening[insert_at:]}"
            else:
                opening = f"{opening} {marker}"
            return opening + rest
        return f"<div {marker}>{self.html}</div>"
