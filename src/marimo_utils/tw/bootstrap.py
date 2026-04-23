from __future__ import annotations

from dr_widget.inline import ActiveHtml

_SHADCN_THEME_CSS = r"""
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --card: 0 0% 100%;
  --card-foreground: 240 10% 3.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  --primary-foreground: 0 0% 98%;
  --secondary: 240 4.8% 95.9%;
  --secondary-foreground: 240 5.9% 10%;
  --muted: 240 4.8% 95.9%;
  --muted-foreground: 240 3.8% 46.1%;
  --accent: 240 4.8% 95.9%;
  --accent-foreground: 240 5.9% 10%;
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 0 0% 98%;
  --border: 240 5.9% 90%;
  --input: 240 5.9% 90%;
  --ring: 240 5.9% 10%;
  --radius: 0.5rem;
}

.bg-background { background-color: hsl(var(--background)); }
.bg-primary { background-color: hsl(var(--primary)); }
.bg-secondary { background-color: hsl(var(--secondary)); }
.bg-destructive { background-color: hsl(var(--destructive)); }
.bg-muted { background-color: hsl(var(--muted)); }
.bg-accent { background-color: hsl(var(--accent)); }
.bg-card { background-color: hsl(var(--card)); }
.bg-popover { background-color: hsl(var(--popover)); }

.text-foreground { color: hsl(var(--foreground)); }
.text-primary-foreground { color: hsl(var(--primary-foreground)); }
.text-secondary-foreground { color: hsl(var(--secondary-foreground)); }
.text-destructive-foreground { color: hsl(var(--destructive-foreground)); }
.text-muted-foreground { color: hsl(var(--muted-foreground)); }
.text-accent-foreground { color: hsl(var(--accent-foreground)); }
.text-card-foreground { color: hsl(var(--card-foreground)); }
.text-popover-foreground { color: hsl(var(--popover-foreground)); }

.border-border { border-color: hsl(var(--border)); }
.border-input { border-color: hsl(var(--input)); }
.ring-ring { --tw-ring-color: hsl(var(--ring)); }
.focus\:ring-ring:focus { --tw-ring-color: hsl(var(--ring)); }

.hover\:bg-primary\/80:hover { background-color: hsl(var(--primary) / 0.8); }
.hover\:bg-secondary\/80:hover { background-color: hsl(var(--secondary) / 0.8); }
.hover\:bg-destructive\/80:hover { background-color: hsl(var(--destructive) / 0.8); }
"""


_INJECT_JS = r"""
(function () {
  if (document.getElementById('shadcn-theme')) return;
  const style = document.createElement('style');
  style.id = 'shadcn-theme';
  style.textContent = __SHADCN_CSS__;
  document.head.appendChild(style);
})();
""".replace("__SHADCN_CSS__", "`" + _SHADCN_THEME_CSS + "`")


_CDN_URL = (
    "https://cdn.tailwindcss.com"
    "?plugins=forms,typography,aspect-ratio,line-clamp,container-queries"
)


_BOOTSTRAP_HTML = f'<script>{_INJECT_JS}</script><script src="{_CDN_URL}"></script>'


def bootstrap_tailwind() -> ActiveHtml:
    r"""Inject the shadcn/ui theme plus the Tailwind Play CDN.

    Two scripts, in order, inside a single `ActiveHtml` blob:
    1. An inline script appends a `<style id="shadcn-theme">` block to
       `document.head` containing shadcn's stock CSS variables (zinc
       light mode) **and** the handful of utility classes that depend
       on them (`bg-primary`, `text-*-foreground`, `border-border`,
       `ring-ring`, plus the `hover:bg-*\/80` variants). Defining these
       utilities as plain CSS rules sidesteps the Play CDN's config-
       extension path, which is fragile across CDN reinitialization.
    2. The Tailwind Play CDN is loaded (deduped by `ActiveHtml`'s
       `loadSrcOnce`). It handles all the built-in utilities
       (`inline-flex`, `rounded-md`, `px-2.5`, `text-xs`, etc.).

    The inline script touches the shared `document`, so the `<style>`
    block lands on the main document's head even though the script
    itself executes inside the anywidget shadow DOM.
    """
    return ActiveHtml(html=_BOOTSTRAP_HTML)


__all__ = ["bootstrap_tailwind"]
