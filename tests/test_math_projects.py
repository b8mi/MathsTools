"""Tests for the mathematical calculations without opening any GUI windows."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arithmetic_series import sum_linear_terms
from lcm_calculator import least_common_multiple
from matrix_calculator import calculate
from parallel_line_distance import distance_between_parallel_lines
from triangle_calculator import triangle_properties, triangle_vertices
import coordinate_transformations as graph


class MathProjectTests(unittest.TestCase):
    def test_original_series_example(self):
        self.assertEqual(sum_linear_terms(3, 10), 224)
        self.assertEqual(sum_linear_terms(-2, 2, 2, 1), 5)
        with self.assertRaises(ValueError):
            sum_linear_terms(10, 3)

    def test_lcm(self):
        self.assertEqual(least_common_multiple([6, 3, 14, 56]), 168)
        self.assertEqual(least_common_multiple([7, 5]), 35)
        self.assertEqual(least_common_multiple([-4, 6]), 12)
        self.assertEqual(least_common_multiple([0, 9]), 0)
        with self.assertRaises(ValueError):
            least_common_multiple([])

    def test_matrix_operations(self):
        a = np.array([[1, 2], [3, 4]])
        b = np.array([[2, 0], [1, 2]])
        np.testing.assert_array_equal(calculate('add', a, b), a+b)
        np.testing.assert_array_equal(calculate('subtract', a, b), a-b)
        np.testing.assert_array_equal(calculate('multiply', a, b), a@b)
        np.testing.assert_array_equal(calculate('scalar', a, scalar=2), a*2)
        self.assertAlmostEqual(calculate('determinant', a), -2)
        np.testing.assert_allclose(calculate('inverse', a) @ a, np.eye(2), atol=1e-12)
        np.testing.assert_array_equal(calculate('transpose', a), a.T)
        with self.assertRaises(ValueError):
            calculate('add', a, np.ones((1, 3)))
        with self.assertRaises(ValueError):
            calculate('multiply', a, np.ones((4, 3)))
        with self.assertRaises(ValueError):
            calculate('determinant', np.ones((1, 2)))
        with self.assertRaises(ValueError):
            calculate('inverse', np.zeros((2, 2)))

    def test_triangle(self):
        import math
        a_angle = math.degrees(math.atan2(3, 4))
        b_angle = math.degrees(math.atan2(4, 3))
        c_angle, a, b, c = triangle_properties(a_angle, b_angle, 5)
        self.assertAlmostEqual(c_angle, 90)
        self.assertAlmostEqual(a, 3)
        self.assertAlmostEqual(b, 4)
        self.assertAlmostEqual(c, 5)
        pts = triangle_vertices(a_angle, b, c)
        self.assertAlmostEqual(math.dist(pts[1], pts[2]), a)
        self.assertAlmostEqual(math.dist(pts[0], pts[2]), b)
        with self.assertRaises(ValueError):
            triangle_properties(90, 90)
        with self.assertRaises(ValueError):
            triangle_properties(50, 60, 0)

    def test_line_distance(self):
        self.assertAlmostEqual(distance_between_parallel_lines(3, 4, 6, 16), 2)
        self.assertAlmostEqual(distance_between_parallel_lines(0, 1, -2, 4), 6)
        with self.assertRaises(ValueError):
            distance_between_parallel_lines(0, 0, 1, 2)

    def test_graph_transforms(self):
        graph.lines = [[(1, 2), (3, 4)]]
        graph.draw_lines = lambda: None
        graph.rotate_lines(90)
        self.assertEqual(graph.lines, [[(-2, 1), (-4, 3)]])
        graph.rotate_lines(-90)
        self.assertEqual(graph.lines, [[(1, 2), (3, 4)]])
        graph.y_plus_one()
        self.assertEqual(graph.lines, [[(1, 3), (3, 5)]])
        graph.y_minus_one()
        graph.x_plus_one()
        graph.x_minus_one()
        self.assertEqual(graph.lines, [[(1, 2), (3, 4)]])
        graph.mirror_lines_ony()
        self.assertEqual(graph.lines, [[(-1, 2), (-3, 4)]])
        graph.mirror_lines_onx()
        self.assertEqual(graph.lines, [[(-1, -2), (-3, -4)]])


if __name__ == '__main__':
    unittest.main()
