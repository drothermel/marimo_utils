from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from marimo_utils.ui.core.drhtml import cn, div, html_block
from marimo_utils.ui.styles import (
    BADGE_FOCUS,
    BORDER,
    BadgeVariant,
    DivLayouts,
    Padding,
    SemanticTone,
    ToneEmphasis,
    Typography,
    tone_surface,
)

if TYPE_CHECKING:
    import marimo as mo
    from dr_widget.inline import ActiveHtml


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    variant: BadgeVariant = BadgeVariant.DEFAULT
    klass: str | None = None

    def _class_name(self) -> str:
        return cn(
            DivLayouts.INLINE_ROW,
            BORDER,
            BADGE_FOCUS,
            Padding.BADGE,
            Typography.BODY_SEMIBOLD,
            self.variant,
            self.klass,
        )

    def to_html(self) -> str:
        return str(
            div(
                self.label,
                klass=self._class_name(),
                data_component="badge",
            )
        )

    def render(self) -> mo.Html | ActiveHtml:
        return html_block(
            div(
                self.label,
                klass=self._class_name(),
            )
        )


def _tone_badge(
    tone: SemanticTone,
    label: str,
    *,
    emphasis: ToneEmphasis = ToneEmphasis.SOFT,
    klass: str | None = None,
) -> Badge:
    return Badge(
        label=label,
        variant=BadgeVariant.OUTLINE,
        klass=cn(tone_surface(tone, emphasis), klass),
    )


def good_badge(
    label: str,
    *,
    emphasis: ToneEmphasis = ToneEmphasis.SOFT,
    klass: str | None = None,
) -> Badge:
    return _tone_badge(SemanticTone.GOOD, label, emphasis=emphasis, klass=klass)


def bad_badge(
    label: str,
    *,
    emphasis: ToneEmphasis = ToneEmphasis.SOFT,
    klass: str | None = None,
) -> Badge:
    return _tone_badge(SemanticTone.BAD, label, emphasis=emphasis, klass=klass)


def neutral_badge(
    label: str,
    *,
    emphasis: ToneEmphasis = ToneEmphasis.SOFT,
    klass: str | None = None,
) -> Badge:
    return _tone_badge(SemanticTone.NEUTRAL, label, emphasis=emphasis, klass=klass)


def bool_badge(
    value: bool,
    *,
    good_when_true: bool = True,
    true_label: str = "Yes",
    false_label: str = "No",
    true_tone: SemanticTone | None = None,
    false_tone: SemanticTone | None = None,
    emphasis: ToneEmphasis = ToneEmphasis.SOFT,
    klass: str | None = None,
) -> Badge:
    good_tone = SemanticTone.GOOD if good_when_true else SemanticTone.BAD
    bad_tone = SemanticTone.BAD if good_when_true else SemanticTone.GOOD
    if value:
        tone = good_tone if true_tone is None else true_tone
        label = true_label
    else:
        tone = bad_tone if false_tone is None else false_tone
        label = false_label
    return _tone_badge(tone, label, emphasis=emphasis, klass=klass)
