"""Verification seam constants for the GOAL three-channel loop."""

from __future__ import annotations

from marimo_utils.ui.core.component import DATA_COMPONENT
from marimo_utils.ui.host.tw_ready import DATA_TW_READY, TW_READY_SELECTOR

COMPONENT_SELECTOR = f"[{DATA_COMPONENT}]"

__all__ = [
    "COMPONENT_SELECTOR",
    "DATA_COMPONENT",
    "DATA_TW_READY",
    "TW_READY_SELECTOR",
]


def selectors_for_dump() -> tuple[str, ...]:
    """CSS selectors automation should wait on before property dumps."""
    return (TW_READY_SELECTOR, COMPONENT_SELECTOR)
