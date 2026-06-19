"""Tailwind readiness sentinel shared by marimo bootstrap and plain-HTML pages."""

from __future__ import annotations

TW_SENTINEL_ID = "dr-tw-sentinel"
DATA_TW_READY = "data-tw-ready"
TW_READY_SELECTOR = '[data-tw-ready="true"]'

TW_SENTINEL_HTML = f'<div id="{TW_SENTINEL_ID}" {DATA_TW_READY}="false" hidden></div>'

INSTALL_SENTINEL_AND_MARK_READY_JS = f"""
(function () {{
  let sentinel = document.getElementById("{TW_SENTINEL_ID}");
  if (!sentinel) {{
    sentinel = document.createElement("div");
    sentinel.id = "{TW_SENTINEL_ID}";
    sentinel.hidden = true;
    sentinel.dataset.twReady = "false";
    (document.body || document.documentElement).appendChild(sentinel);
  }}
  sentinel.dataset.twReady = "true";
}})();
"""

MARK_TW_READY_ON_STYLESHEET_JS = f"""
(function () {{
  function markReady() {{
    const sentinel = document.getElementById("{TW_SENTINEL_ID}");
    if (sentinel) {{
      sentinel.dataset.twReady = "true";
    }}
  }}
  if (document.getElementById("dr-styles")) {{
    markReady();
    return;
  }}
  const link = document.querySelector('link[data-dr-stylesheet="true"]');
  if (!link) {{
    markReady();
    return;
  }}
  if (link.sheet) {{
    markReady();
    return;
  }}
  link.addEventListener("load", markReady, {{ once: true }});
}})();
"""
