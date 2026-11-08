"""模糊推理系统的最小自动检查。"""

from __future__ import annotations

import unittest

import numpy as np

from fuzzy_system import infer_wash_time
from membership import triangular


class MembershipTests(unittest.TestCase):
    def test_triangle_key_points(self) -> None:
        actual = triangular(np.array([0.0, 2.5, 5.0]), 0.0, 2.5, 5.0)
        np.testing.assert_allclose(actual, np.array([0.0, 1.0, 0.0]))

    def test_left_shoulder(self) -> None:
        actual = triangular(np.array([0.0, 2.5, 5.0]), 0.0, 0.0, 5.0)
        np.testing.assert_allclose(actual, np.array([1.0, 0.5, 0.0]))


class FuzzySystemTests(unittest.TestCase):
    def test_clean_clothes_need_shorter_time(self) -> None:
        self.assertLess(infer_wash_time(1.0, 1.0).wash_time, 20.0)

    def test_dirty_clothes_need_longer_time(self) -> None:
        self.assertGreater(infer_wash_time(9.0, 9.0).wash_time, 40.0)

    def test_result_stays_in_output_range(self) -> None:
        result = infer_wash_time(6.5, 8.0)
        self.assertGreaterEqual(result.wash_time, 0.0)
        self.assertLessEqual(result.wash_time, 60.0)
        self.assertTrue(any(item.strength > 0 for item in result.activations))


if __name__ == "__main__":
    unittest.main(verbosity=2)
