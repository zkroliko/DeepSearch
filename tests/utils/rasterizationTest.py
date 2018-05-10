import unittest

import acoAlgorithm.utils.TriangleRasterization as tr
import numpy as np
import matplotlib.pyplot as plt


class TestRasterization(unittest.TestCase):
    def test_visual(self):
        triangle = np.array([[0, 5], [4, 4], [9, 5]])
        points = tr.rasterize_triangle(triangle)

        array = np.zeros([20, 20])
        array[points[:, 1], points[:, 0]] = 1

        plt.imshow(array, interpolation='none')
        plt.scatter(*triangle.T, c='white')

    def test_validity1(self):
        triangle = np.array([[0, 0], [5, 0], [0, 5]])
        fields = tr.rasterize_triangle(triangle)

        expected = [[0, 4], [1, 4], [0, 3], [1, 3], [2, 3], [0, 2], [1, 2],
                    [2, 2], [3, 2], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1],
                    [1, 0], [2, 0], [3, 0], [4, 0]]

        self.assertTrue((fields==expected).all())

    def test_validity2(self):
        triangle = np.array([[1, 1], [5, 1], [1, 5]])
        fields = tr.rasterize_triangle(triangle)

        expected = [[1, 4], [2, 4], [1, 3], [2, 3], [3, 3], [1, 2], [2, 2],
                    [3, 2], [4, 2], [2, 1], [3, 1], [4, 1]]

        self.assertTrue((fields==expected).all())

