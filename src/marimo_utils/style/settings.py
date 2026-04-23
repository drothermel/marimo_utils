from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TonePalette(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    bg: str
    border: str


class PaletteToneName(StrEnum):
    NEUTRAL = "neutral"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


class ColorPalette(BaseModel):
    model_config = ConfigDict(frozen=True)

    text_primary: str
    text_muted: str
    text_subtle: str
    surface_background: str
    surface_border: str
    surface_shadow: str
    neutral: TonePalette
    info: TonePalette
    success: TonePalette
    warning: TonePalette
    danger: TonePalette

    def tone(self, tone_name: PaletteToneName) -> TonePalette:
        return getattr(self, tone_name.value)

    @classmethod
    def default(cls) -> ColorPalette:
        return cls(
            text_primary="#0f172a",
            text_muted="#475569",
            text_subtle="#64748b",
            surface_background=(
                "linear-gradient(160deg, #f8fafc 0%, #eef4ff 62%, #fff7ed 100%)"
            ),
            surface_border="rgba(148, 163, 184, 0.18)",
            surface_shadow="0 10px 24px rgba(15, 23, 42, 0.07)",
            neutral=TonePalette(
                text="#334155",
                bg="#e2e8f0",
                border="#475569",
            ),
            info=TonePalette(
                text="#1d4ed8",
                bg="#dbeafe",
                border="#2563eb",
            ),
            success=TonePalette(
                text="#0f766e",
                bg="#ccfbf1",
                border="#115e59",
            ),
            warning=TonePalette(
                text="#9a3412",
                bg="#ffedd5",
                border="#c2410c",
            ),
            danger=TonePalette(
                text="#b91c1c",
                bg="#fee2e2",
                border="#b91c1c",
            ),
        )


class TextStyle(BaseModel):
    model_config = ConfigDict(frozen=True)

    font_size: str
    font_weight: int
    letter_spacing: str = "0"
    line_height: str = "1.2"
    text_transform: str | None = None

    def css(self, *, color: str | None = None) -> str:
        parts = [
            f"font-size: {self.font_size}",
            f"font-weight: {self.font_weight}",
            f"letter-spacing: {self.letter_spacing}",
            f"line-height: {self.line_height}",
        ]
        if self.text_transform is not None:
            parts.append(f"text-transform: {self.text_transform}")
        if color is not None:
            parts.append(f"color: {color}")
        return "; ".join(parts)


class IconStyle(BaseModel):
    model_config = ConfigDict(frozen=True)

    width: str
    height: str
    stroke_width: str
    flex: str = "0 0 auto"

    @classmethod
    def default(cls) -> IconStyle:
        return cls(
            width="14",
            height="14",
            stroke_width="2",
        )


class LayoutToken(StrEnum):
    FLEX = "display: flex"
    INLINE_FLEX = "display: inline-flex"
    INLINE_BLOCK = "display: inline-block"
    NOWRAP = "white-space: nowrap"
    FLEX_WRAP = "flex-wrap: wrap"
    ALIGN_CENTER = "align-items: center"

    @classmethod
    def css(cls, tokens: list[LayoutToken]) -> str:
        return "; ".join(token.value for token in tokens)


class Typography(BaseModel):
    model_config = ConfigDict(frozen=True)

    font_family: str
    title: TextStyle
    drop_title: TextStyle
    body: TextStyle
    meta: TextStyle
    badge: TextStyle
    label: TextStyle

    @classmethod
    def default(cls) -> Typography:
        return cls(
            font_family=("'IBM Plex Sans', 'Avenir Next', 'Segoe UI', sans-serif"),
            title=TextStyle(
                font_size="1.08rem",
                font_weight=700,
                letter_spacing="-0.015em",
                line_height="1.25",
            ),
            drop_title=TextStyle(
                font_size="0.68rem",
                font_weight=700,
                letter_spacing="0.12em",
                line_height="1.2",
                text_transform="uppercase",
            ),
            body=TextStyle(
                font_size="0.82rem",
                font_weight=600,
                line_height="1.25",
            ),
            meta=TextStyle(
                font_size="0.68rem",
                font_weight=600,
                letter_spacing="0.04em",
                line_height="1.2",
            ),
            badge=TextStyle(
                font_size="0.68rem",
                font_weight=600,
                line_height="1.2",
            ),
            label=TextStyle(
                font_size="0.68rem",
                font_weight=700,
                letter_spacing="0.06em",
                line_height="1.2",
                text_transform="uppercase",
            ),
        )


class SpacingScale(BaseModel):
    model_config = ConfigDict(frozen=True)

    xxs: str
    xs: str
    sm: str
    md: str
    lg: str
    xl: str
    xxl: str
    line_height_loose: str

    @classmethod
    def default(cls) -> SpacingScale:
        return cls(
            xxs="0.08rem",
            xs="0.12rem",
            sm="0.28rem",
            md="0.42rem",
            lg="0.55rem",
            xl="0.8rem",
            xxl="0.9rem",
            line_height_loose="1.8",
        )


class Style(BaseModel):
    model_config = ConfigDict(frozen=True)

    palette: ColorPalette
    typography: Typography
    spacing: SpacingScale
    icon_style: IconStyle = Field(default_factory=IconStyle.default)

    @classmethod
    def default(cls) -> Style:
        return cls(
            palette=ColorPalette.default(),
            typography=Typography.default(),
            spacing=SpacingScale.default(),
        )

    def plotly_layout(self) -> dict[str, object]:
        """Return a plain-dict plotly ``layout`` partial derived from tokens.

        Safe to splat into ``fig.update_layout(**style.plotly_layout())``.
        Does not import plotly — just returns strings/dicts/lists.
        """
        tones = (
            PaletteToneName.NEUTRAL,
            PaletteToneName.INFO,
            PaletteToneName.SUCCESS,
            PaletteToneName.WARNING,
            PaletteToneName.DANGER,
        )
        return {
            "font": {
                "family": self.typography.font_family,
                "color": self.palette.text_primary,
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "margin": {"l": 8, "r": 8, "t": 8, "b": 8},
            "showlegend": False,
            "colorway": [self.palette.tone(tone).border for tone in tones],
        }

    def tone_colorscale(self, tone: PaletteToneName) -> list[list[float | str]]:
        """Sequential two-stop colorscale derived from a palette tone.

        Maps ``0.0`` to the tone's ``bg`` (light) and ``1.0`` to its
        ``border`` (saturated). Intended for ``go.Heatmap`` / choropleth
        use where plotly expects ``list[[float, str]]``.
        """
        palette = self.palette.tone(tone)
        return [[0.0, palette.bg], [1.0, palette.border]]


__all__ = [
    "ColorPalette",
    "IconStyle",
    "LayoutToken",
    "PaletteToneName",
    "SpacingScale",
    "Style",
    "TextStyle",
    "TonePalette",
    "Typography",
]
