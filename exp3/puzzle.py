"""八数码状态表示、合法性检查、启发函数和后继生成。"""

from __future__ import annotations

from collections.abc import Iterator


Board = tuple[int, ...]
SIZE = 3
GOAL: Board = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = (
    ("UP", -1, 0),
    ("DOWN", 1, 0),
    ("LEFT", 0, -1),
    ("RIGHT", 0, 1),
)


def validate_board(board: Board) -> None:
    # FILL-01：检查长度为 9，且数字 0～8 各出现一次。
    if (
        len(board) != SIZE * SIZE
        or sorted(board) != list(range(SIZE * SIZE))
    ):
        raise ValueError("棋盘必须由数字 0～8 各一次组成")


def inversion_count(board: Board) -> int:
    """统计忽略空格 0 后的逆序对数量。"""

    # FILL-02：用双重循环统计前大后小的数对。
    values = [value for value in board if value != 0]
    return sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )


def is_solvable(start: Board, goal: Board = GOAL) -> bool:
    validate_board(start)
    validate_board(goal)
    return inversion_count(start) % 2 == inversion_count(goal) % 2


def manhattan(board: Board, goal: Board = GOAL) -> int:
    """计算所有非零数字到目标位置的曼哈顿距离之和。"""

    # FILL-03：建立目标位置表，并累计横纵坐标距离；不要计算空格 0。
    goal_positions = {
        value: divmod(index, SIZE)
        for index, value in enumerate(goal)
    }
    distance = 0
    for index, value in enumerate(board):
        if value == 0:
            continue
        row, column = divmod(index, SIZE)
        goal_row, goal_column = goal_positions[value]
        distance += abs(row - goal_row) + abs(column - goal_column)
    return distance


def neighbors(board: Board) -> Iterator[tuple[str, Board]]:
    """按 UP、DOWN、LEFT、RIGHT 的固定顺序生成合法后继。"""

    # FILL-04：定位空格，尝试四个方向，交换后生成不可变元组。
    blank = board.index(0)
    row, column = divmod(blank, SIZE)
    for move, delta_row, delta_column in MOVES:
        next_row = row + delta_row
        next_column = column + delta_column
        if not (0 <= next_row < SIZE and 0 <= next_column < SIZE):
            continue

        target = next_row * SIZE + next_column
        values = list(board)
        values[blank], values[target] = values[target], values[blank]
        yield move, tuple(values)


def format_board(board: Board) -> str:
    symbols = [" " if value == 0 else str(value) for value in board]
    rows = [" ".join(symbols[i : i + SIZE]) for i in range(0, len(symbols), SIZE)]
    return "\n".join(rows)
