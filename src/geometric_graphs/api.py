# -*- coding: utf-8 -*-

"""Main code."""

from dataclasses import dataclass
from itertools import count, repeat
from typing import Iterable

from more_itertools import chunked, pairwise

from .util import Factory

__all__ = [
    # Lines
    "line_factory",
    "LineFactory",
    # Circles
    "circle_factory",
    "CircleFactory",
    # Chain
    "ChainFactory",
    "chain_factory",
    # Square grid
    "square_grid_factory",
    "SquareGrid2DFactory",
    # Hexagonal grid
    "hex_grid_factory",
    "HexagonalGrid2DFactory",
]


def line_factory(num_entities: int, create_inverse_triples: bool = False):
    """Create a triples factory on a line of ``num_entities`` elements.

    :param num_entities: the number of entities in the line
    :param create_inverse_triples: Should inverse triples be created?
    :rtype: pykeen.triples.CoreTriplesFactory
    :returns: A PyKEEN triples factory

    If you run ``line_factory(5)``, you will get the following knowledge graph:

    .. code-block::

        E_0 -[R_0]-> E_1 -[R_0]-> E_2 -[R_0]-> E_3 -[R_0]-> E_4

    If you run ``line_factory(5, create_inverse_triples=True)``, you will get the following knowledge graph:

    .. code-block::

             [R_0]        [R_0]        [R_0]        [R_0]
           /       ⬊     /       ⬊    /       ⬊    /       ⬊
        E_0          E_1          E_2          E_3          E_4
           ⬉       /     ⬉       /    ⬉       /   ⬉       /
             [R_1]        [R_1]        [R_1]        [R_1]
    """
    return LineFactory(num_entities).to_pykeen(create_inverse_triples=create_inverse_triples)


@dataclass
class LineFactory(Factory):
    """A factory for a one-dimensional line."""

    #: Number of elements in the line
    n: int

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a one-dimensional line."""
        for head, tail in pairwise(range(self.n)):
            yield head, 0, tail


def circle_factory(num_entities: int, create_inverse_triples: bool = False):
    """Create a triples factory on a line of ``num_entities`` elements.

    :param num_entities: the number of entities in the line
    :param create_inverse_triples: Should inverse triples be created?
    :returns: A PyKEEN triples factory
    """
    return CircleFactory(num_entities).to_pykeen(create_inverse_triples=create_inverse_triples)


@dataclass
class CircleFactory(LineFactory):
    """A factory for a circle.

    An extension of a line factory that includes an additional
    triple to close the loop between the first and last elements.
    """

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a circle."""
        yield from super().iterate_triples()
        # Finally, close the loop
        yield self.n - 1, 0, 0


def square_grid_factory(rows: int, columns: int, create_inverse_triples: bool = False):
    """Create a two-dimensional square grid of the given number of rows and columns.

    :param rows: The number of rows in the square grid
    :param columns: The number of columns in the square grid
    :param create_inverse_triples: Should inverse triples be created?
    :rtype: pykeen.triples.CoreTriplesFactory
    :returns: A PyKEEN triples factory

    If you run ``mesh_factory(2, 5)``, you will get the following knowledge graph:

    .. code-block::

         E_0 -[R_0]-> E_1 -[R_0]-> E_2 -[R_0]-> E_3 -[R_0]-> E_4
          |            |            |            |            |
        [R_1]        [R_1]        [R_1]        [R_1]        [R_1]
          ↓            ↓            ↓            ↓            ↓
         E_5 -[R_0]-> E_6 -[R_0]-> E_7 -[R_0]-> E_8 -[R_0]-> E_2
    """
    return SquareGrid2DFactory(rows, columns).to_pykeen(
        create_inverse_triples=create_inverse_triples
    )


@dataclass
class SquareGrid2DFactory(Factory):
    """A factory for a two-dimensional square grid."""

    #: Number of rows in the grid
    rows: int
    #: Number of columns in the grid
    columns: int

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for a two-dimensional square grid."""
        num_entities = self.rows * self.columns

        chunks = list(chunked(range(num_entities), self.rows))
        for chunk in chunks:
            for head, tail in pairwise(chunk):
                yield head, 0, tail

        for chunk in zip(*chunks):
            for head, tail in pairwise(chunk):
                yield head, 1, tail


def hex_grid_factory(rows: int, columns: int, create_inverse_triples: bool = False):
    """Create a hexagonal grid in 2D of the given number of rows and columns.

    :param rows: The number of hexagon rows (if odd, the final row will be a minor row and if even the final row
        will be an even row
    :param columns: The minor row width (major rows have rows + 1)
    :param create_inverse_triples: Should inverse triples be created?
    :rtype: pykeen.triples.CoreTriplesFactory
    :returns: A PyKEEN triples factory

    If you run ``hex_factory(rows=1, columns=3)``, you will get the following knowledge graph:

    .. code-block::

                    E_0                     E_1                     E_2
                  ⬋     ⬊                 ⬋     ⬊                 ⬋     ⬊
             [R_0]       [R_1]       [R_0]       [R_1]       [R_0]       [R_1]
            ⬋                 ⬊     ⬋                 ⬊     ⬋                 ⬊
        E_4                     E_5                     E_6                     E_7
         |                       |                       |                       |
       [R_3]                   [R_3]                   [R_3]                   [R_3]
         ↓                       ↓                       ↓                       ↓
        E_8                     E_9                     E_10                    E_11
            ⬊                 ⬋     ⬊                 ⬋     ⬊                 ⬋
             [R_1]       [R_0]       [R_1]       [R_0]       [R_1]       [R_0]
                 ⬊     ⬋                 ⬊     ⬋                 ⬊     ⬋
                   E_12                    E_13                    E_14
    """
    return HexagonalGrid2DFactory(rows=rows, columns=columns).to_pykeen(
        create_inverse_triples=create_inverse_triples
    )


@dataclass
class HexagonalGrid2DFactory(Factory):
    """A factory for a two-dimensional hexagonal grid."""

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


def chain_factory(
    length: int,
    width: int = 1,
    leaves: int = 2,
    heterogeneous: bool = True,
    create_inverse_triples: bool = False,
):
    """Create a chain."""
    return ChainFactory(
        length=length, width=width, leaves=leaves, heterogeneous=heterogeneous
    ).to_pykeen(create_inverse_triples=create_inverse_triples)


@dataclass
class ChainFactory(Factory):
    """A factory for a chain."""

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
