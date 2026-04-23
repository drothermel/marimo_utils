from __future__ import annotations

import json

from dr_widget.inline import ActiveHtml

from marimo_utils.ui.theme import SHADCN_THEME_CSS

# `json.dumps` produces a proper JS string literal — backslashes in the CSS
# (Tailwind-escaped class names like `.hover\:bg-primary\/80`) survive JS
# parsing. A backtick template literal would eat the `\:` and `\/` escapes,
# silently collapsing selectors to invalid ones like `.hover:bg-primary/80`.
_BOOTSTRAP_JS = f"""
(function () {{
  if (document.getElementById('shadcn-theme')) return;
  const style = document.createElement('style');
  style.id = 'shadcn-theme';
  style.appendChild(document.createTextNode({json.dumps(SHADCN_THEME_CSS)}));
  document.head.appendChild(style);
}})();
"""


_CDN_URL = (
    "https://cdn.tailwindcss.com"
    "?plugins=forms,typography,aspect-ratio,line-clamp,container-queries"
)


_BOOTSTRAP_HTML = f'<script>{_BOOTSTRAP_JS}</script><script src="{_CDN_URL}"></script>'


def bootstrap_tailwind() -> ActiveHtml:
    """Inject the shadcn/ui theme plus the Tailwind Play CDN.

    Two scripts, in order, inside a single `ActiveHtml` blob:

    1. An inline script appends a `<style id="shadcn-theme">` block to
       `document.head` with shadcn's CSS variables (zinc light mode) plus
       the utility classes that depend on them — `bg-primary`,
       `text-*-foreground`, `border-border`, `ring-ring`, `hover:bg-*/80`,
       and the `bg-chart-N` / `text-chart-N` chart palette utilities.
       Defining these as plain CSS sidesteps the Play CDN's config-
       extension path, which is fragile across CDN reinitialization.
    2. The Tailwind Play CDN is loaded (deduped by `ActiveHtml`'s
       `loadSrcOnce`). It handles every built-in utility (`inline-flex`,
       `rounded-md`, `px-2.5`, `text-xs`, etc.).

    The inline script touches the shared `document`, so the `<style>`
    block lands on the main document even though the script itself
    executes inside the anywidget shadow DOM.
    """
    return ActiveHtml(html=_BOOTSTRAP_HTML)


__all__ = ["bootstrap_tailwind"]
