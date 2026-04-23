from __future__ import annotations

import altair as alt
import marimo as mo
from pydantic import BaseModel, ConfigDict, Field, computed_field

from marimo_utils.style.settings import ColorPalette, PaletteToneName, Typography


class PieSlice(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: int = Field(ge=0)
    tone: PaletteToneName = PaletteToneName.NEUTRAL
    color: str | None = None


class PieChart(BaseModel):
    model_config = ConfigDict(frozen=True)

    palette: ColorPalette
    typography: Typography = Field(default_factory=Typography.default)
    slices: list[PieSlice]
    width: int = 220
    height: int = 220
    outer_radius: int = 88
    label_radius: int = 56
    stroke_width: int = 2
    label_color: str = "#f8fafc"

    @computed_field
    @property
    def visible_slices(self) -> list[PieSlice]:
        return [slice_ for slice_ in self.slices if slice_.value > 0]

    @computed_field
    @property
    def total(self) -> int:
        return sum(slice_.value for slice_ in self.visible_slices)

    def color_for_slice(self, slice_: PieSlice) -> str:
        if slice_.color is not None:
            return slice_.color
        return self.palette.tone(slice_.tone).border

    def chart_rows(self) -> list[dict[str, str | int]]:
        return [
            {
                "label": slice_.label,
                "value": slice_.value,
                "value_label": f"{slice_.value:,}",
                "order": idx,
                "color": self.color_for_slice(slice_),
            }
            for idx, slice_ in enumerate(self.visible_slices)
        ]

    def empty_state(self) -> mo.Html:
        return mo.md("_No slice data available._")

    def render(self) -> object:
        rows = self.chart_rows()
        if not rows:
            return self.empty_state()

        domain = [row["label"] for row in rows]
        colors = [row["color"] for row in rows]
        font = self.typography.font_family.split(",")[0].strip().strip("'\"")

        base = alt.Chart(alt.Data(values=rows)).encode(
            theta=alt.Theta("value:Q", stack=True),
            color=alt.Color(
                "label:N",
                scale=alt.Scale(domain=domain, range=colors),
                legend=None,
            ),
            order=alt.Order("order:Q"),
            tooltip=[
                alt.Tooltip("label:N", title="Slice"),
                alt.Tooltip("value:Q", title="Count", format=","),
            ],
        )

        pie = base.mark_arc(
            outerRadius=self.outer_radius,
            stroke=self.label_color,
            strokeWidth=self.stroke_width,
        )
        labels = base.mark_text(
            radius=self.label_radius,
            color=self.label_color,
            font=font,
            fontSize=13,
            fontWeight="bold",
        ).encode(text="value_label:N")

        return (
            alt.layer(pie, labels)
            .properties(width=self.width, height=self.height)
            .configure_view(stroke=None)
        )


__all__ = ["PieChart", "PieSlice"]
