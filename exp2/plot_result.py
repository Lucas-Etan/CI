"""绘制输入隶属函数和模糊推理输出。"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import INPUT_RANGE, INPUT_TERMS
from fuzzy_system import FuzzyResult
from membership import triangular


def save_result_plot(result: FuzzyResult, output_path: Path) -> None:
    input_x = np.linspace(INPUT_RANGE[0], INPUT_RANGE[1], 201)
    figure, axes = plt.subplots(1, 3, figsize=(13, 4))

    for axis, value, title in (
        (axes[0], result.stain, "Stain level"),
        (axes[1], result.grease, "Grease level"),
    ):
        for term, points in INPUT_TERMS.items():
            axis.plot(input_x, triangular(input_x, *points), label=term)
        axis.axvline(value, color="black", linestyle="--", label=f"input={value:.2f}")
        axis.set(title=title, xlabel="level", ylabel="membership", ylim=(-0.05, 1.05))
        axis.legend()

    axes[2].plot(result.output_x, result.aggregated, color="tab:blue")
    # FILL-07：在输出图中标出 wash_time 的竖线。
    axes[2].axvline(
        result.wash_time,
        color="tab:red",
        linestyle="--",
        label=f"{result.wash_time:.2f} min",
    )
    axes[2].set(
        title="Aggregated wash time",
        xlabel="minutes",
        ylabel="membership",
        ylim=(-0.05, 1.05),
    )
    axes[2].legend()
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160)
    plt.close(figure)
