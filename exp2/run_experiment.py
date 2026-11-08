"""运行洗衣机模糊推理并保存数值与图像结果。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fuzzy_system import infer_wash_time
from plot_result import save_result_plot
from student_identity import display_identity, load_identity


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    parser = argparse.ArgumentParser(description="洗衣机模糊推理")
    parser.add_argument("--stain", type=float, default=6.5, help="污渍程度 0～10")
    parser.add_argument("--grease", type=float, default=8.0, help="油污程度 0～10")
    args = parser.parse_args()

    identity = load_identity()
    result = infer_wash_time(args.stain, args.grease)
    active = [item for item in result.activations if item.strength > 0]

    print(f"输入：stain={result.stain:.2f}, grease={result.grease:.2f}")
    print("污渍隶属度：", result.stain_memberships)
    print("油污隶属度：", result.grease_memberships)
    print("被激活的规则：")
    for item in active:
        print(
            f"  IF stain={item.stain_term} AND grease={item.grease_term} "
            f"THEN time={item.output_term}; strength={item.strength:.3f}"
        )
    print(f"建议洗涤时间：{result.wash_time:.2f} 分钟")

    # FILL-08：组织输入、隶属度、激活规则和最终时间，写入 JSON。
    payload: dict[str, object] = {
        "input": {
            "stain": result.stain,
            "grease": result.grease,
        },
        "memberships": {
            "stain": result.stain_memberships,
            "grease": result.grease_memberships,
        },
        "active_rules": [item.__dict__ for item in active],
        "wash_time_minutes": result.wash_time,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "fuzzy_result.json"
    result_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    plot_path = OUTPUT_DIR / "fuzzy_result.png"
    save_result_plot(result, plot_path)
    print(f"结果文件：{result_path}")
    print(f"结果图：{plot_path}")
    display_identity(identity, stage="final-fuzzy-inference")


if __name__ == "__main__":
    main()
