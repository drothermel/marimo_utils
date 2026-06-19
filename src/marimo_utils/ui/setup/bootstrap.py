from __future__ import annotations

import json

from dr_widget.inline import ActiveHtml

from marimo_utils.ui.setup.stylesheet import DR_CSS

# `json.dumps` produces a proper JS string literal — backslashes in the CSS
# (Tailwind-escaped class names like `.hover\:bg-primary\/80`) survive JS
# parsing. A backtick template literal would eat the `\:` and `\/` escapes,
# silently collapsing selectors to invalid ones like `.hover:bg-primary/80`.
_BOOTSTRAP_JS = f"""
(function () {{
  if (document.getElementById('dr-styles')) return;
  const style = document.createElement('style');
  style.id = 'dr-styles';
  style.appendChild(document.createTextNode({json.dumps(DR_CSS)}));
  document.head.appendChild(style);
}})();
"""

_BOOTSTRAP_HTML = f"<script>{_BOOTSTRAP_JS}</script>"


def bootstrap_tailwind() -> ActiveHtml:
    """Inject the precompiled component stylesheet once per page.

    An inline script appends a ``<style id="dr-styles">`` block to
    ``document.head`` with the bundled utilities, shadcn theme tokens, and
    ``.dr-scope`` reset (Preflight off). The script touches the shared
    ``document``, so the block lands on the main document even though the
    script itself executes inside the anywidget shadow DOM.
    """
    return ActiveHtml(html=_BOOTSTRAP_HTML)
