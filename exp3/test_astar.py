"""A* 八数码实现的最小自动检查。"""

from __future__ import annotations

import unittest

from astar import astar_search
from puzzle import GOAL, inversion_count, manhattan, neighbors


class PuzzleTests(unittest.TestCase):
    def test_goal_heuristic_is_zero(self) -> None:
        self.assertEqual(manhattan(GOAL), 0)

    def test_inversion_ignores_blank(self) -> None:
        self.assertEqual(inversion_count((1, 2, 3, 4, 5, 6, 8, 7, 0)), 1)

    def test_center_blank_has_four_neighbors(self) -> None:
        board = (1, 2, 3, 4, 0, 5, 6, 7, 8)
        self.assertEqual(len(list(neighbors(board))), 4)


class AStarTests(unittest.TestCase):
    def test_one_step_solution(self) -> None:
        result = astar_search((1, 2, 3, 4, 5, 6, 7, 0, 8))
        self.assertEqual(result.cost, 1)
        self.assertEqual(result.moves, ("RIGHT",))
        self.assertEqual(result.boards[-1], GOAL)

    def test_default_case_reaches_goal(self) -> None:
        result = astar_search((1, 3, 6, 5, 0, 2, 4, 7, 8))
        self.assertEqual(result.boards[0], (1, 3, 6, 5, 0, 2, 4, 7, 8))
        self.assertEqual(result.boards[-1], GOAL)
        self.assertEqual(result.cost, len(result.moves))

    def test_unsolvable_case_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            astar_search((1, 2, 3, 4, 5, 6, 8, 7, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
