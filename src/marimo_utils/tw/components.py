from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import span  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.tw._rendering import html_block
from marimo_utils.tw.tones import TONE_CLASSES, Tone


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    tone: Tone = Tone.INFO
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        t = TONE_CLASSES[self.tone]
        base = (
            "inline-block whitespace-nowrap rounded-full border "
            "px-2 py-0.5 text-xs font-semibold "
            f"{t['bg']} {t['text']} {t['border']}"
        )
        classes = f"{base} {self.klass}" if self.klass else base
        return html_block(span(self.label, klass=classes))


__all__ = ["Badge"]
