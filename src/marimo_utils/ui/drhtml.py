"""HTML tag builders and marimo output routing.

Adapted from mohtml (MIT License):
https://github.com/koaning/mohtml

The tag factory follows the upstream implementation; child serialization
uses ``format(child, "")`` so nested ``mo.Html`` fragments compose correctly
inside parent tags. ``klass=`` values are merged with ``tailwind-merge`` so
later utilities win within each Tailwind group (same principle as shadcn
``cn()``).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

import marimo as mo
from dr_widget.inline import ActiveHtml
from tailwind_merge import TailwindMerge

from marimo_utils.ui.theme import SHADCN_STYLE_BLOCK

_twm = TailwindMerge()

html_tags = [
    "a",
    "p",
    "i",
    "b",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "div",
    "span",
    "pre",
    "blockquote",
    "q",
    "ul",
    "ol",
    "li",
    "dl",
    "dt",
    "dd",
    "table",
    "thead",
    "tbody",
    "tfoot",
    "tr",
    "th",
    "td",
    "caption",
    "form",
    "label",
    "select",
    "option",
    "textarea",
    "button",
    "fieldset",
    "legend",
    "article",
    "section",
    "nav",
    "aside",
    "header",
    "footer",
    "main",
    "figure",
    "figcaption",
    "strong",
    "em",
    "mark",
    "code",
    "samp",
    "kbd",
    "var",
    "time",
    "abbr",
    "dfn",
    "sub",
    "sup",
    "audio",
    "video",
    "picture",
    "canvas",
    "details",
    "summary",
    "dialog",
    "script",
    "noscript",
    "template",
    "style",
    "html",
    "head",
    "body",
    "svg",
    "g",
]

self_closing_tags = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
    "circle",
    "rect",
    "ellipse",
    "line",
    "polyline",
    "polygon",
    "path",
]


def _merge_class_attr(*values: object) -> str:
    """Merge Tailwind class strings; later utilities win within each group."""
    parts = [value for value in values if isinstance(value, str) and value.strip()]
    if not parts:
        return ""
    return _twm.merge(*parts)


class HtmlTag:
    """A tree node that renders to an HTML element string."""

    __slots__ = ("args", "html_name", "kwargs")

    html_name: str
    args: tuple[object, ...]
    kwargs: dict[str, object]

    def __init__(self, html_name: str, *args: object, **kwargs: object) -> None:
        if args and html_name in self_closing_tags:
            msg = (
                f"{html_name} element cannot have *args because it represents "
                "self closing html tag."
            )
            raise RuntimeError(msg)
        self.html_name = html_name
        self.args = args
        kw = dict(kwargs)
        class_values: list[object] = []
        if "klass" in kw:
            class_values.append(kw.pop("klass"))
        if "class" in kw:
            class_values.append(kw.pop("class"))
        if class_values:
            kw["class"] = _merge_class_attr(*class_values)
        self.kwargs = kw

    def __str__(self) -> str:
        return self._to_html()

    def __repr__(self) -> str:
        return self._to_html()

    def _repr_html_(self) -> str:
        return self._to_html()

    def _to_html(self) -> str:
        class_name = self.html_name
        if class_name in self_closing_tags:
            elem = f"<{class_name}/>"
        else:
            elem = f"<{class_name}>"
        if self.kwargs:
            kwargs_str = " ".join(
                f'{k.replace("_", "-")}="{v}"' for k, v in self.kwargs.items()
            )
            if class_name in self_closing_tags:
                elem = f"<{class_name} {kwargs_str}/>"
            else:
                elem = f"<{class_name} {kwargs_str}>"
        for arg in self.args:
            elem += _child_html(arg)
        if class_name not in self_closing_tags:
            elem += f"</{class_name}>"
        return elem


def _child_html(child: object) -> str:
    """Serialize a tag child; ``format`` handles nested ``mo.Html`` correctly."""
    return format(child, "")


def _make_tag(name: str) -> Callable[..., HtmlTag]:
    def tag(*args: object, **kwargs: object) -> HtmlTag:
        return HtmlTag(name, *args, **kwargs)

    tag.__name__ = name
    tag.__doc__ = f"Object that represents `<{name}>` HTML element."
    return tag


for _class_name in html_tags + self_closing_tags:
    globals()[_class_name] = _make_tag(_class_name)


class HtmlRenderable(Protocol):
    def __str__(self) -> str: ...


def html_block(fragment: HtmlRenderable) -> mo.Html | ActiveHtml:
    """Render HTML fragment; routes through ActiveHtml when contains scripts.

    `mo.Html` silently drops inline `<script>` tags via its react html-parser,
    so anything with scripts (Tailwind Play CDN, plotly) must go through
    `ActiveHtml`, which re-executes script nodes after mount.

    When routing through `ActiveHtml` the payload is prepended with
    `SHADCN_STYLE_BLOCK`. `ActiveHtml` mounts its content inside a shadow
    DOM, and styles in `document.head` don't cascade into shadow roots —
    so a Card-with-plotly-chart would lose its Tailwind chrome without
    the local style injection.
    """
    html = str(fragment)
    if "<script" in html.lower():
        return ActiveHtml(html=SHADCN_STYLE_BLOCK + html)
    return mo.Html(html)
