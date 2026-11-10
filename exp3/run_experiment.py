"""运行 A* 八数码实验，并与无启发信息的统一代价搜索比较。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from astar import astar_search
from puzzle import Board, GOAL, format_board
from student_identity import display_identity, load_identity


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def parse_board(raw: str) -> Board:
    # FILL-09：把英文逗号分隔的文本转换为整数元组。
    try:
        return tuple(int(item.strip()) for item in raw.split(","))
    except ValueError as exc:
        raise ValueError("棋盘需要使用英文逗号分隔的整数") from exc


def zero_heuristic(_board: Board, _goal: Board) -> int:
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="A* 求解八数码")
    parser.add_argument("--start", default="1,3,6,5,0,2,4,7,8")
    args = parser.parse_args()

    identity = load_identity()
    start = parse_board(args.start)
    informed = astar_search(start, GOAL)
    uninformed = astar_search(start, GOAL, heuristic=zero_heuristic)

    print("初始状态：")
    print(format_board(start))
    print(f"A* 路径长度：{informed.cost}")
    print(f"A* 扩展节点：{informed.stats.expanded}")
    print(f"统一代价搜索扩展节点：{uninformed.stats.expanded}")
    print("动作序列：", " -> ".join(informed.moves))
    print("目标状态：")
    print(format_board(informed.boards[-1]))

    payload = {
        "start": list(start),
        "goal": list(GOAL),
        "cost": informed.cost,
        "moves": list(informed.moves),
        "boards": [list(board) for board in informed.boards],
        "astar_stats": informed.stats.__dict__,
        "uniform_cost_stats": uninformed.stats.__dict__,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / "solution.json"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    text_path = OUTPUT_DIR / "solution.txt"
    text_path.write_text(
        "\n\n".join(
            f"Step {index}\n{format_board(board)}"
            for index, board in enumerate(informed.boards)
        ),
        encoding="utf-8",
    )
    print(f"结果文件：{json_path}")
    print(f"路径文件：{text_path}")
    display_identity(identity, stage="final-astar-search")


if __name__ == "__main__":
    main()
