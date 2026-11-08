"""洗衣时间模糊推理系统的论域、隶属函数和规则配置。"""

from __future__ import annotations


INPUT_RANGE = (0.0, 10.0)
OUTPUT_RANGE = (0.0, 60.0)
OUTPUT_STEP = 0.25

# 三角形用 (左端点, 顶点, 右端点) 表示；端点重合时形成肩形函数。
INPUT_TERMS = {
    "low": (0.0, 0.0, 5.0),
    "medium": (2.5, 5.0, 7.5),
    "high": (5.0, 10.0, 10.0),
}

OUTPUT_TERMS = {
    "short": (0.0, 0.0, 30.0),
    "medium": (15.0, 30.0, 45.0),
    "long": (30.0, 60.0, 60.0),
}

# (污渍程度, 油污程度, 洗涤时间)
RULES = (
    ("low", "low", "short"),
    ("low", "medium", "short"),
    ("low", "high", "medium"),
    ("medium", "low", "short"),
    ("medium", "medium", "medium"),
    ("medium", "high", "long"),
    ("high", "low", "medium"),
    ("high", "medium", "long"),
    ("high", "high", "long"),
)
