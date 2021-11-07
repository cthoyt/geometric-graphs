# -*- coding: utf-8 -*-

"""Generator classes."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations, count, repeat
from typing import Iterable, Optional

from more_itertools import chunked, pairwise

from .util import Generator

__all__ = [
    "LineGenerator",
    "CircleGenerator",
    "SquareGrid2DGenerator",
    "HexagonalGrid2DGenerator",
    "ChainGenerator",
    "StarGenerator",
    "WheelGenerator",
    "BarbellGenerator",
    "TadpoleGenerator",
    "LollipopGenerator",
]


@dataclass
class LineGenerator(Generator):
    """A generator for a one-dimensional line."""

    #: Number of elements in the line
    n: int

    def number_of_nodes(self) -> int:
        """Return the number of nodes for a path of length ``n``."""
        return self.n

    def number_of_edges(self) -> int:  # noqa:D102
        """Return the number of edges for a path of length ``n``."""
        return self.n - 1

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a one-dimensional line."""
        for head, tail in pairwise(range(self.n)):
            yield head, 0, tail


@dataclass
class CircleGenerator(LineGenerator):
    """A generator for a circle.

    An extension of a line generator that includes an additional
    triple to close the loop between the first and last elements.
    """

    def number_of_edges(self) -> int:  # noqa:D102
        """Return the number of edges for a circle of size ``n``."""
        return self.n

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a circle."""
        yield from super().iterate_triples()
        # Finally, close the loop
        yield self.n - 1, 0, 0


@dataclass
class SquareGrid2DGenerator(Generator):
    """A generator for a two-dimensional square grid."""

    #: Number of rows in the grid
    rows: int
    #: Number of columns in the grid
    columns: int

    def number_of_nodes(self) -> Optional[int]:
        """Return the number of nodes for the two-dimensional square grid."""
        return self.rows * self.columns

    def number_of_edges(self) -> Optional[int]:
        """Return the number of edges for the two-dimensional square grid."""
        return self.rows * self.columns

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the two-dimensional square grid."""
        num_entities = self.rows * self.columns

        chunks = list(chunked(range(num_entities), self.rows))
        for chunk in chunks:
            for head, tail in pairwise(chunk):
                yield head, 0, tail

        for chunk in zip(*chunks):
            for head, tail in pairwise(chunk):
                yield head, 1, tail


@dataclass
class HexagonalGrid2DGenerator(Generator):
    """A generator for a two-dimensional hexagonal grid."""

    rows: int
    columns: int
    labels: tuple[int, int, int] = (0, 1, 2)

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a two-dimensional hexagonal grid."""
        left, right, vert = self.labels
        for r1, r2 in pairwise(_hex_grid_helper(self.rows, self.columns)):
            if len(r1) == len(r2):  # minor/minor or major/major
                yield from zip(r1, repeat(vert), r2)
            elif len(r1) < len(r2):  # minor/major
                yield from zip(r1, repeat(left), r2)
                yield from zip(r1, repeat(right), r2[1:])
            else:  # major/minor
                yield from zip(r1, repeat(right), r2)
                yield from zip(r1[1:], repeat(left), r2)


def _hex_grid_helper(rows: int, columns: int) -> list[list[int]]:
    rv = []
    counter = count()

    def _append_row(n: int) -> None:
        rv.append([next(counter) for _ in range(n)])

    # First row is special - always is the first quarter of a minor row
    _append_row(columns)

    for row in range(rows):
        for _ in range(2):  # double up rows for cross beams
            _append_row(columns + 1 + row % 2)

    # Last row is special, is columns + 1 if # rows is even, else columns
    _append_row(columns + (1 + rows) % 2)

    return rv


@dataclass
class ChainGenerator(Generator):
    """A generator for a chain."""

    #: Number of main elements in the chain
    length: int
    #: Number of sub elements in each loop of the chain
    width: int = 1
    #: Number of prong in each loop (2 corresponds to an actual chain)
    leaves: int = 2
    #: Should the different edge types be given different labels?
    heterogeneous: bool = True

    def __post_init__(self):
        """Check the arguments are valid."""
        if self.length < 2:
            raise ValueError(
                "Length of a chain must be 2 or greater. A chain of length 1 is just a single node"
            )
        if self.width < 1:
            raise ValueError(
                "Width of a chain must be 1 or greater. A chain with length 0 is just a line"
            )
        if self.leaves < 2:
            # Then it would just be a line
            raise ValueError(
                "Number of leaves must be 2 or greater. A chain with a single leaf is just a line."
            )

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a chain."""
        if self.heterogeneous:
            begin, cont, end = 0, 1, 2
        else:
            begin, cont, end = 0, 0, 0

        c = 0
        for _ in range(self.length - 1):
            first = c
            lasts = []
            for _ in range(self.leaves):
                c += 1
                lasts.append(c)
                yield first, begin, c

            for _ in range(self.width - 1):
                nexts = []
                for _ in range(self.leaves):
                    c += 1
                    nexts.append(c)
                for left, right in zip(lasts, nexts):
                    yield left, cont, right
                lasts = nexts
            c += 1
            for last in lasts:
                yield last, end, c


@dataclass
class StarGenerator(Generator):
    """A generator for the star graph."""

    #: Number of spokes in the star
    spokes: int
    #: If true, make all edges point towards centers.
    sink: bool = False

    def number_of_nodes(self) -> Optional[int]:
        """Return the number of nodes for the star."""
        return self.spokes + 1

    def number_of_edges(self) -> Optional[int]:
        """Return the number of edges for the star."""
        return self.spokes

    def __post_init__(self) -> None:
        """Check the arguments are valid."""
        if self.spokes < 3:
            raise ValueError("There must be at least 3 spokes.")

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for stars."""
        for spoke in range(1, self.spokes + 1):
            if self.sink:
                yield spoke, 0, 0
            else:
                yield 0, 0, spoke


@dataclass
class WheelGenerator(StarGenerator):
    """A generator for the wheel graph."""

    def number_of_edges(self) -> Optional[int]:
        """Return the number of edges for the wheel."""
        return 2 * self.spokes

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the wheel graph."""
        yield from super().iterate_triples()
        for left, right in pairwise(range(1, self.spokes + 1)):
            yield left, 1, right
        yield self.spokes, 1, 1


@dataclass
class BarbellGenerator(Generator):
    """A generator for a barbell graph.

    .. seealso:: https://en.wikipedia.org/wiki/Barbell_graph
    """

    #: The size of the barbell
    n: int

    def number_of_nodes(self) -> int:
        """Return the number of nodes for the barbell."""
        return self.n * 2

    def number_of_edges(self) -> int:
        """Return the number of edges for the barbell."""
        return 2 * math.comb(self.n, 2) + 1

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the barbell graph."""
        west = range(self.n)
        east = range(self.n, 2 * self.n)
        for head, tail in combinations(west, 2):
            yield head, 0, tail
        for head, tail in combinations(east, 2):
            yield head, 0, tail
        yield 0, 1, self.n
        # TODO make a more balanced clique generator that
        # goes in a loop, then goes in a loop for 2-negihbors
        # then 3 neighbors, then so on until all connected.


@dataclass
class TadpoleGenerator(Generator):
    """A generator for a tadpole graph.

    .. seealso:: https://en.wikipedia.org/wiki/Tadpole_graph
    """

    #: The size of the cycle
    m: int
    #: The length of the path
    n: int
    #: If true, the path edges point towards the cycle
    sink: bool = False

    def number_of_nodes(self) -> int:
        """Return the number of nodes for the tadpole."""
        return self.m + self.n

    def number_of_edges(self) -> int:
        """Return the number of edges for the tadpole."""
        return self.m + self.n

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the tadpole graph."""
        for head, tail in pairwise(range(self.m)):
            yield head, 0, tail
        yield self.m - 1, 0, 0
        for head, tail in pairwise(range(self.m - 1, self.m + self.n)):
            if self.sink:
                yield tail, 1, head
            else:
                yield head, 1, tail


@dataclass
class LollipopGenerator(Generator):
    """A generator for a lollipop graph.

    .. seealso:: https://en.wikipedia.org/wiki/Lollipop_graph
    """

    #: The size of the clique
    m: int
    #: The length of the path
    n: int
    #: If true, the path edges point towards the cycle
    sink: bool = False

    @classmethod
    def special(cls, k: int, sink: bool = False) -> LollipopGenerator:
        r"""Generate a special lollipop graph from a single parameter.

        This parametrization achieves maximal
        `hitting time <https://en.wikipedia.org/wiki/Hitting_time>`_.

        :param k: The standard parameters are calculated by $m = \frac{2}{3}k$
            and $n=\frac{1/3}k$.
        :param sink: If true, the path edges point towards the cycle
        :return: A lollipop generator.
        :raises ValueError: if $k$ is not divisible by 3
        """
        if k % 3 != 0:
            raise ValueError("value must be divisible by 3")
        return cls(m=2 * k // 3, n=k // 3, sink=sink)

    def number_of_nodes(self) -> int:
        """Return the number of nodes for the lollipop graph."""
        return self.m + self.n

    def number_of_edges(self) -> int:
        """Return the number of edges for the lollipop graph."""
        return math.comb(self.m, 2) + self.n

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the lollipop graph."""
        for head, tail in combinations(range(self.m), 2):
            yield head, 0, tail  # FIXME more balanced clique generation
        for head, tail in pairwise(range(self.m - 1, self.m + self.n)):
            if self.sink:
                yield tail, 1, head
            else:
                yield head, 1, tail
