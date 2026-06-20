"""Verification seam constants for the GOAL three-channel loop."""

from __future__ import annotations

from marimo_utils.ui.core.component import DATA_COMPONENT
from marimo_utils.ui.host.tw_ready import TW_READY_SELECTOR

COMPONENT_SELECTOR = f"[{DATA_COMPONENT}]"


def selectors_for_dump() -> tuple[str, ...]:
    """CSS selectors automation should wait on before property dumps.

    ``data-tw-ready`` means the stylesheet is applied, not that ``<dr-*>``
    custom elements have upgraded. Wait on element content separately for
    runtime-dependent dumps.
    """
    return (TW_READY_SELECTOR, COMPONENT_SELECTOR)
