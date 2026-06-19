from __future__ import annotations

import re

from marimo_utils.ui.core.drhtml import br, strong

_BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")


def auto_render(obj: object) -> object:
    """Call `.render()` if present; otherwise pass through.

    Tag builders concatenate children via ``format()``, so ``mo.Html`` /
    ``ActiveHtml`` / raw strings all compose once rendered.
    """
    render_fn = getattr(obj, "render", None)
    if callable(render_fn):
        return render_fn()
    return obj


def render_inline(text: str) -> list[object]:
    """Render a description string as HTML tag child nodes.

    Splits on ``\\n`` (rendered as ``<br/>``) and parses ``**text**`` as
    ``<strong>``. Deliberately narrow — just line breaks and bold, no
    full-markdown support — so the rendering is predictable inside a
    Card's ``<p>`` element.
    """
    children: list[object] = []
    for i, line in enumerate(text.split("\n")):
        if i > 0:
            children.append(br())
        pos = 0
        for match in _BOLD_PATTERN.finditer(line):
            if match.start() > pos:
                children.append(line[pos : match.start()])
            children.append(strong(match.group(1)))
            pos = match.end()
        if pos < len(line):
            children.append(line[pos:])
    return children
