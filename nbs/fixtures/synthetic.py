"""Deterministic synthetic demo data for component notebooks (seed=42)."""

from __future__ import annotations

import random

DEFAULT_SEED = 42


def _build(seed: int = DEFAULT_SEED) -> dict[str, object]:
    rng = random.Random(seed)
    loss_values = [rng.gauss(0.4, 0.12) for _ in range(180)]
    group_train = [rng.gauss(0.35, 0.10) for _ in range(120)]
    group_val = [rng.gauss(0.45, 0.14) for _ in range(120)]
    group_test = [rng.gauss(0.52, 0.11) for _ in range(120)]
    scatter_a_x = [rng.gauss(2.0, 0.6) for _ in range(60)]
    scatter_a_y = [rng.gauss(2.5, 0.6) for _ in range(60)]
    scatter_b_x = [rng.gauss(3.5, 0.6) for _ in range(60)]
    scatter_b_y = [rng.gauss(1.5, 0.6) for _ in range(60)]
    line_steps = [float(i) for i in range(30)]
    line_train_loss = [0.9 * (0.92**i) + rng.gauss(0.0, 0.015) for i in range(30)]
    line_val_loss = [
        0.95 * (0.94**i) + 0.05 + rng.gauss(0.0, 0.025) for i in range(30)
    ]
    return {
        "LOSS_VALUES": loss_values,
        "GROUP_TRAIN": group_train,
        "GROUP_VAL": group_val,
        "GROUP_TEST": group_test,
        "CONFUSION_Z": [[42, 3, 1], [4, 38, 2], [2, 5, 33]],
        "CONFUSION_LABELS": ["cat", "dog", "bird"],
        "SCATTER_A_X": scatter_a_x,
        "SCATTER_A_Y": scatter_a_y,
        "SCATTER_B_X": scatter_b_x,
        "SCATTER_B_Y": scatter_b_y,
        "LINE_STEPS": line_steps,
        "LINE_TRAIN_LOSS": line_train_loss,
        "LINE_VAL_LOSS": line_val_loss,
    }


_data = _build()
LOSS_VALUES: list[float] = _data["LOSS_VALUES"]  # type: ignore[assignment]
GROUP_TRAIN: list[float] = _data["GROUP_TRAIN"]  # type: ignore[assignment]
GROUP_VAL: list[float] = _data["GROUP_VAL"]  # type: ignore[assignment]
GROUP_TEST: list[float] = _data["GROUP_TEST"]  # type: ignore[assignment]
CONFUSION_Z: list[list[int]] = _data["CONFUSION_Z"]  # type: ignore[assignment]
CONFUSION_LABELS: list[str] = _data["CONFUSION_LABELS"]  # type: ignore[assignment]
SCATTER_A_X: list[float] = _data["SCATTER_A_X"]  # type: ignore[assignment]
SCATTER_A_Y: list[float] = _data["SCATTER_A_Y"]  # type: ignore[assignment]
SCATTER_B_X: list[float] = _data["SCATTER_B_X"]  # type: ignore[assignment]
SCATTER_B_Y: list[float] = _data["SCATTER_B_Y"]  # type: ignore[assignment]
LINE_STEPS: list[float] = _data["LINE_STEPS"]  # type: ignore[assignment]
LINE_TRAIN_LOSS: list[float] = _data["LINE_TRAIN_LOSS"]  # type: ignore[assignment]
LINE_VAL_LOSS: list[float] = _data["LINE_VAL_LOSS"]  # type: ignore[assignment]
