# -*- coding: utf-8 -*-

"""Main code."""

from itertools import count, repeat
from typing import Any, Iterable, List, Tuple, cast

from more_itertools import chunked, pairwise

__all__ = [
    "from_tuples",
    # Lines
    "line_factory",
    # 2D squares
    "square_grid_factory",
    "iter_square_grid_triples",
    # 2D hexagons
    "hex_grid_factory",
    "iter_hex_grid_triples",
]


def from_tuples(triples: Iterable[Tuple[int, int, int]], create_inverse_triples: bool = False):
    """Create a PyKEEN triples factory from tuples.

    :param triples: An iterable of integer triples
    :param create_inverse_triples: Should inverse triples be created?
    :returns: A PyKEEN triples factory
    """
    import torch
    from pykeen.triples import CoreTriplesFactory

    mapped_triples = cast(torch.LongTensor, torch.as_tensor(list(triples), dtype=torch.long))
    return CoreTriplesFactory.create(mapped_triples, create_inverse_triples=create_inverse_triples)


def line_factory(num_entities: int, create_inverse_triples: bool = False):
    """Create a triples factory on a line of ``num_entities`` elements.

    :param num_entities: the number of entities in the line
    :param create_inverse_triples: Should inverse triples be created?
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
    triples = []
    for head, tail in pairwise(range(num_entities)):
        triples.append((head, 0, tail))
    return from_tuples(triples, create_inverse_triples)


def square_grid_factory(rows: int, columns: int, create_inverse_triples: bool = False):
    """Create a two-dimensional square grid of the given number of rows and columns.

    :param rows: The number of rows in the square grid
    :param columns: The number of columns in the square grid
    :param create_inverse_triples: Should inverse triples be created?
    :returns: A PyKEEN triples factory

    If you run ``mesh_factory(2, 5)``, you will get the following knowledge graph:

    .. code-block::

         E_0 -[R_0]-> E_1 -[R_0]-> E_2 -[R_0]-> E_3 -[R_0]-> E_4
          |            |            |            |            |
        [R_1]        [R_1]        [R_1]        [R_1]        [R_1]
          ↓            ↓            ↓            ↓            ↓
         E_5 -[R_0]-> E_6 -[R_0]-> E_7 -[R_0]-> E_8 -[R_0]-> E_2
    """
    triples = iter_square_grid_triples(rows=rows, columns=columns)
    return from_tuples(triples, create_inverse_triples=create_inverse_triples)


def iter_square_grid_triples(rows: int, columns: int) -> Iterable[Tuple[int, int, int]]:
    """Iterate over triples for a two dimensional square grid.

    :param rows: The number of rows in the square grid
    :param columns: The number of columns in the square grid
    :yields: Triples over a two-dimensional square grid
    """
    num_entities = rows * columns

    chunks = list(chunked(range(num_entities), rows))
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
    triples = iter_hex_grid_triples(rows=rows, columns=columns)
    return from_tuples(triples, create_inverse_triples=create_inverse_triples)


def iter_hex_grid_triples(
    rows: int,
    columns: int,
    labels: Tuple[Any, Any, Any] = (0, 1, 2),
) -> Iterable[Tuple[int, int, int]]:
    """Iterate over triples for a two-dimensional hexagonal grid.

    :param rows: The number of hexagon rows (if odd, the final row will be a minor row and if even the final row
        will be an even row
    :param columns: The minor row width (major rows have rows + 1)
    :param labels: The labels for the left, right, and vertical relation.
    :yields: Triples over a two-dimensional hexagonal grid
    """
    left, right, vert = labels
    for r1, r2 in pairwise(_hex_grid_helper(rows, columns)):
        if len(r1) == len(r2):  # minor/minor or major/major
            yield from zip(r1, repeat(vert), r2)
        elif len(r1) < len(r2):  # minor/major
            yield from zip(r1, repeat(left), r2)
            yield from zip(r1, repeat(right), r2[1:])
        else:  # major/minor
            yield from zip(r1, repeat(right), r2)
            yield from zip(r1[1:], repeat(left), r2)


def _hex_grid_helper(rows: int, columns: int) -> List[List[int]]:
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
