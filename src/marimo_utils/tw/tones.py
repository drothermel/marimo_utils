from __future__ import annotations

from enum import StrEnum


class Tone(StrEnum):
    NEUTRAL = "neutral"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


TONE_CLASSES: dict[Tone, dict[str, str]] = {
    Tone.NEUTRAL: {
        "bg": "bg-slate-100",
        "text": "text-slate-700",
        "border": "border-slate-500",
    },
    Tone.INFO: {
        "bg": "bg-blue-100",
        "text": "text-blue-700",
        "border": "border-blue-600",
    },
    Tone.SUCCESS: {
        "bg": "bg-teal-100",
        "text": "text-teal-700",
        "border": "border-teal-800",
    },
    Tone.WARNING: {
        "bg": "bg-orange-100",
        "text": "text-orange-800",
        "border": "border-orange-700",
    },
    Tone.DANGER: {
        "bg": "bg-red-100",
        "text": "text-red-700",
        "border": "border-red-700",
    },
}


TONE_HEX: dict[Tone, dict[str, str]] = {
    Tone.NEUTRAL: {"bg": "#f1f5f9", "text": "#334155", "border": "#64748b"},
    Tone.INFO: {"bg": "#dbeafe", "text": "#1d4ed8", "border": "#2563eb"},
    Tone.SUCCESS: {"bg": "#ccfbf1", "text": "#0f766e", "border": "#115e59"},
    Tone.WARNING: {"bg": "#ffedd5", "text": "#9a3412", "border": "#c2410c"},
    Tone.DANGER: {"bg": "#fee2e2", "text": "#b91c1c", "border": "#b91c1c"},
}


__all__ = ["TONE_CLASSES", "TONE_HEX", "Tone"]
