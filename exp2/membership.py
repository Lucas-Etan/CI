"""可复用的三角形与肩形隶属度函数。"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def triangular(x: ArrayLike, a: float, b: float, c: float) -> NDArray[np.float64]:
    """计算三角形隶属度；a=b 或 b=c 时分别表示左肩或右肩。"""

    if not a <= b <= c or a == c:
        raise ValueError("需要满足 a <= b <= c，且 a 与 c 不能相等")
    values = np.asarray(x, dtype=float)

    # FILL-01：分别计算上升边、下降边，再取较小值并裁剪到 [0, 1]。
    rising = (
        np.ones_like(values)
        if a == b
        else (values - a) / (b - a)
    )
    falling = (
        np.ones_like(values)
        if b == c
        else (c - values) / (c - b)
    )
    return np.clip(np.minimum(rising, falling), 0.0, 1.0)
