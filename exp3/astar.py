"""使用优先队列实现 A* 搜索。"""

from __future__ import annotations

import heapq
import itertools
from collections.abc import Callable
from dataclasses import dataclass

from puzzle import Board, GOAL, is_solvable, manhattan, neighbors, validate_board


Heuristic = Callable[[Board, Board], int]


@dataclass(frozen=True)
class SearchStats:
    expanded: int
    generated: int
    frontier_peak: int


@dataclass(frozen=True)
class SearchResult:
    boards: tuple[Board, ...]
    moves: tuple[str, ...]
    cost: int
    stats: SearchStats


def reconstruct_path(
    came_from: dict[Board, tuple[Board, str]], current: Board
) -> tuple[tuple[Board, ...], tuple[str, ...]]:
    boards = [current]
    moves: list[str] = []
    # FILL-08：沿 came_from 逆向回溯，再把两个列表翻转为正向顺序。
    while current in came_from:
        current, move = came_from[current]
        boards.append(current)
        moves.append(move)

    boards.reverse()
    moves.reverse()
    return tuple(boards), tuple(moves)


def astar_search(
    start: Board, goal: Board = GOAL, heuristic: Heuristic = manhattan
) -> SearchResult:
    validate_board(start)
    validate_board(goal)
    if not is_solvable(start, goal):
        raise ValueError("该初始状态与目标状态的奇偶性不同，无解")

    counter = itertools.count()
    start_h = heuristic(start, goal)
    # FILL-05：建立 frontier、g_score 与 came_from；堆元素保存 f、h、序号、g、状态。
    frontier: list[tuple[int, int, int, int, Board]] = [
        (start_h, start_h, next(counter), 0, start)
    ]
    g_score = {start: 0}
    came_from: dict[Board, tuple[Board, str]] = {}

    expanded = 0
    generated = 1
    frontier_peak = 1

    while frontier:
        # FILL-06：弹出 f 最小状态；跳过过期条目；命中目标时回溯并返回。
        _f, _h, _order, current_g, current = heapq.heappop(frontier)
        if current_g != g_score.get(current):
            continue

        if current == goal:
            boards, moves = reconstruct_path(came_from, current)
            return SearchResult(
                boards,
                moves,
                current_g,
                SearchStats(expanded, generated, frontier_peak),
            )

        expanded += 1
        for move, next_board in neighbors(current):
            tentative_g = current_g + 1
            # FILL-07：仅在路径更短时更新 g_score、父节点并压入堆。
            if tentative_g >= g_score.get(next_board, float("inf")):
                continue

            g_score[next_board] = tentative_g
            came_from[next_board] = (current, move)
            next_h = heuristic(next_board, goal)
            heapq.heappush(
                frontier,
                (
                    tentative_g + next_h,
                    next_h,
                    next(counter),
                    tentative_g,
                    next_board,
                ),
            )
            generated += 1

        frontier_peak = max(frontier_peak, len(frontier))

    raise RuntimeError("搜索队列耗尽，未找到目标状态")
