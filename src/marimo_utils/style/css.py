from __future__ import annotations


def css(*fragments: str, **decls: str | None) -> str:
    """Build a CSS declaration string.

    Keyword arguments become `prop: value` declarations (underscores
    translate to hyphens, None values are skipped). Positional arguments
    are pre-formatted fragments (e.g. a joined ``LayoutToken`` string)
    appended after the keyword declarations.

    A single trailing semicolon is appended iff the result is non-empty;
    fragments are tolerant of their own trailing semicolons and extra
    whitespace.
    """
    parts: list[str] = [
        f"{k.replace('_', '-')}: {v}" for k, v in decls.items() if v is not None
    ]
    for fragment in fragments:
        if not fragment:
            continue
        stripped = fragment.strip().rstrip(";").rstrip()
        if stripped:
            parts.append(stripped)
    if not parts:
        return ""
    return "; ".join(parts) + ";"


__all__ = ["css"]
