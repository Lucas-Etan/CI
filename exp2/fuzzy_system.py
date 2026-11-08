"""Mamdani 洗衣时间模糊推理。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from config import (
    INPUT_RANGE,
    INPUT_TERMS,
    OUTPUT_RANGE,
    OUTPUT_STEP,
    OUTPUT_TERMS,
    RULES,
)
from membership import triangular


@dataclass(frozen=True)
class RuleActivation:
    stain_term: str
    grease_term: str
    output_term: str
    strength: float


@dataclass(frozen=True)
class FuzzyResult:
    stain: float
    grease: float
    stain_memberships: dict[str, float]
    grease_memberships: dict[str, float]
    activations: tuple[RuleActivation, ...]
    output_x: NDArray[np.float64]
    aggregated: NDArray[np.float64]
    wash_time: float


def fuzzify(value: float) -> dict[str, float]:
    """把一个精确输入转换成 low、medium、high 三个隶属度。"""

    # FILL-02：遍历 INPUT_TERMS，并调用 triangular 计算每个隶属度。
    return {
        term: float(triangular(np.array([value]), *points)[0])
        for term, points in INPUT_TERMS.items()
    }


def centroid(x: NDArray[np.float64], membership: NDArray[np.float64]) -> float:
    """用离散重心法把聚合后的模糊集合转换为精确时间。"""

    # FILL-05：检查分母，并计算 sum(x * membership) / sum(membership)。
    denominator = float(np.sum(membership))
    if denominator <= 0.0:
        raise ValueError("聚合输出为空，无法执行解模糊")
    return float(np.sum(x * membership) / denominator)


def infer_wash_time(stain: float, grease: float) -> FuzzyResult:
    """完成模糊化、规则激活、输出聚合和解模糊。"""

    low, high = INPUT_RANGE
    if not (low <= stain <= high and low <= grease <= high):
        raise ValueError(f"污渍和油污程度都必须位于 [{low}, {high}]")

    stain_mu = fuzzify(stain)
    grease_mu = fuzzify(grease)
    output_x = np.arange(OUTPUT_RANGE[0], OUTPUT_RANGE[1] + OUTPUT_STEP, OUTPUT_STEP)
    aggregated = np.zeros_like(output_x)
    activations: list[RuleActivation] = []

    for stain_term, grease_term, output_term in RULES:
        # FILL-03：用 min 合取两个前件隶属度，得到规则激活强度。
        strength = min(
            stain_mu[stain_term],
            grease_mu[grease_term],
        )
        activations.append(
            RuleActivation(stain_term, grease_term, output_term, strength)
        )

        output_shape = triangular(output_x, *OUTPUT_TERMS[output_term])
        clipped = np.minimum(strength, output_shape)
        # FILL-04：用 max 把当前规则的截断输出合并到 aggregated。
        aggregated = np.maximum(aggregated, clipped)

    # FILL-06：调用 centroid，返回包含全部中间结果的 FuzzyResult。
    wash_time = centroid(output_x, aggregated)
    return FuzzyResult(
        stain,
        grease,
        stain_mu,
        grease_mu,
        tuple(activations),
        output_x,
        aggregated,
        wash_time,
    )
