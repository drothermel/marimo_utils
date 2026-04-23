from __future__ import annotations

import anywidget
import traitlets

_ACTIVE_HTML_ESM = """\
// ActiveHtml mounts HTML and activates embedded <script> tags. Because
// marimo-anywidget hosts us inside a shadow DOM, any embedded script that
// calls document.getElementById(id) on an element inside our el will fail
// (document lookups don't pierce shadow roots). We patch document.getElementById
// once per page to walk shadow roots as a fallback. This is transparent to
// callers that pass real document ids and fixes script-bearing HTML fragments
// whose authors assumed a flat document (plotly, bokeh, mermaid, etc.).
(function patchGetElementByIdOnce() {
  if (document.__activeHtmlGetByIdPatched) return;
  const orig = document.getElementById.bind(document);
  document.getElementById = function (id) {
    const direct = orig(id);
    if (direct) return direct;
    function walk(root) {
      if (root !== document && root.getElementById) {
        const hit = root.getElementById(id);
        if (hit) return hit;
      }
      const hosts = root.querySelectorAll ? root.querySelectorAll("*") : [];
      for (const h of hosts) {
        if (h.shadowRoot) {
          const hit = walk(h.shadowRoot);
          if (hit) return hit;
        }
      }
      return null;
    }
    return walk(document);
  };
  document.__activeHtmlGetByIdPatched = true;
})();

const srcLoads = (window.__activeHtmlSrcLoadPromises ||= new Map());

function loadSrcOnce(src, attrs) {
  if (srcLoads.has(src)) return srcLoads.get(src);
  const p = new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${CSS.escape(src)}"]`)) {
      resolve();
      return;
    }
    const s = document.createElement("script");
    for (const [k, v] of Object.entries(attrs)) s.setAttribute(k, v);
    s.src = src;
    s.async = false;
    s.addEventListener("load", () => resolve());
    s.addEventListener("error", () => reject(new Error(`load failed: ${src}`)));
    document.head.appendChild(s);
  });
  srcLoads.set(src, p);
  return p;
}

async function render({ model, el }) {
  el.innerHTML = model.get("html");
  const scripts = Array.from(el.querySelectorAll("script"));
  for (const old of scripts) {
    if (old.src) {
      const attrs = {};
      for (const a of old.attributes) {
        if (a.name !== "src") attrs[a.name] = a.value;
      }
      try {
        await loadSrcOnce(old.src, attrs);
      } catch (e) {
        console.error("[ActiveHtml]", e);
      }
      old.remove();
    } else {
      const fresh = document.createElement("script");
      for (const a of old.attributes) fresh.setAttribute(a.name, a.value);
      fresh.textContent = old.textContent;
      old.replaceWith(fresh);
    }
  }
}

export default { render };
"""


class ActiveHtml(anywidget.AnyWidget):
    """HTML mount that executes embedded ``<script>`` tags.

    ``mo.Html`` runs through React's html-react-parser, which silently drops
    inline ``<script>`` content. Libraries like plotly ship HTML fragments
    that depend on those scripts executing. ``ActiveHtml`` mounts the HTML
    into its own element and then clone-replaces every ``<script>`` tag so
    the browser treats them as fresh, executable nodes. ``src``-bearing
    scripts are deduplicated across widget instances via a
    ``window``-scoped Promise cache so, e.g., the plotly CDN is fetched at
    most once per page even when many cards are on screen.
    """

    html = traitlets.Unicode("").tag(sync=True)
    _esm = _ACTIVE_HTML_ESM

    def __str__(self) -> str:
        return self.html

    def _repr_html_(self) -> str:
        return self.html


__all__ = ["ActiveHtml"]
