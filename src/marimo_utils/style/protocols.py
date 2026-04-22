from typing import Protocol, runtime_checkable


@runtime_checkable
class HtmlRenderable(Protocol):
    """A value that stringifies to HTML and exposes an HTML mime repr.

    Matches any ``mohtml`` tag instance (which implements ``__str__`` and
    ``_repr_html_`` as HTML serialization), plus any custom class that
    follows the same convention.
    """

    def __str__(self) -> str: ...

    def _repr_html_(self) -> str: ...


__all__ = ["HtmlRenderable"]
