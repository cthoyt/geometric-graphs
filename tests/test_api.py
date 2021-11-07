# -*- coding: utf-8 -*-

"""Tests for knowledge graph factories."""

import unittest

from geometric_graphs.api import ChainFactory, _hex_grid_helper


class TestFactories(unittest.TestCase):
    """A test case for knowledge graph factories."""

    def test_hex_rows(self):
        """Test generating a two dimensional hexagonal grid graph."""
        for rows, columns, expected in [
            # one row
            (
                1,
                1,
                [[0], [1, 2], [3, 4], [5]],
            ),
            (1, 2, [[0, 1], [2, 3, 4], [5, 6, 7], [8, 9]]),
            (
                1,
                3,
                [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9, 10], [11, 12, 13]],
            ),
            # two rows
            (
                2,
                1,
                [
                    [0],
                    [1, 2],
                    [3, 4],
                    [5, 6, 7],
                    [8, 9, 10],
                    [11, 12],
                ],
            ),
            (
                2,
                2,
                [
                    [0, 1],
                    [2, 3, 4],
                    [5, 6, 7],
                    [8, 9, 10, 11],
                    [12, 13, 14, 15],
                    [16, 17, 18],
                ],
            ),
            (
                2,
                3,
                [
                    [0, 1, 2],
                    [3, 4, 5, 6],
                    [7, 8, 9, 10],
                    [11, 12, 13, 14, 15],
                    [16, 17, 18, 19, 20],
                    [21, 22, 23, 24],
                ],
            ),
            # three rows
            (
                3,
                1,
                [
                    [0],
                    [1, 2],
                    [3, 4],
                    [5, 6, 7],
                    [8, 9, 10],
                    [11, 12],
                    [13, 14],
                    [15],
                ],
            ),
            (
                3,
                2,
                [
                    [0, 1],
                    [2, 3, 4],
                    [5, 6, 7],
                    [8, 9, 10, 11],
                    [12, 13, 14, 15],
                    [16, 17, 18],
                    [19, 20, 21],
                    [22, 23],
                ],
            ),
            (
                3,
                3,
                [
                    [0, 1, 2],
                    [3, 4, 5, 6],
                    [7, 8, 9, 10],
                    [11, 12, 13, 14, 15],
                    [16, 17, 18, 19, 20],
                    [21, 22, 23, 24],
                    [25, 26, 27, 28],
                    [29, 30, 31],
                ],
            ),
            # four rows
            (
                4,
                1,
                [
                    [0],
                    [1, 2],
                    [3, 4],
                    [5, 6, 7],
                    [8, 9, 10],
                    [11, 12],
                    [13, 14],
                    [15, 16, 17],
                    [18, 19, 20],
                    [21, 22],
                ],
            ),
        ]:
            with self.subTest(rows=rows, columns=columns):
                grid = _hex_grid_helper(rows=rows, columns=columns)
                self.assertEqual(columns, len(grid[0]), msg="first row have length of columns")
                self.assertEqual(
                    columns + (rows + 1) % 2,
                    len(grid[-1]),
                    msg="# rows even -> columns + 1 in last row; odd -> columns in last row",
                )
                self.assertEqual(
                    2 * (1 + rows),
                    len(expected),
                    msg="test data is wrong: grid should be 2 * (1 + rows) long",
                )
                self.assertEqual(len(expected), len(grid), msg="grid should be 2 * (1 + rows) long")
                self.assertEqual(expected, grid)

    def test_chain(self):
        """Test the chain factory."""
        factory = ChainFactory(length=3, width=1, heterogeneous=False)
        triples = [
            (0, 0, 1),
            (0, 0, 2),
            (1, 0, 3),
            (2, 0, 3),
            (3, 0, 4),
            (3, 0, 5),
            (4, 0, 6),
            (5, 0, 6),
        ]
        self.assertEqual(triples, list(factory.get_triples()))

        factory = ChainFactory(length=3, width=2, heterogeneous=False)
        triples = [
            (0, 0, 1),
            (0, 0, 2),
            (1, 0, 3),
            (2, 0, 4),
            (3, 0, 5),
            (4, 0, 5),
            (5, 0, 6),
            (5, 0, 7),
            (6, 0, 8),
            (7, 0, 9),
            (8, 0, 10),
            (9, 0, 10),
        ]
        self.assertEqual(triples, list(factory.get_triples()))
