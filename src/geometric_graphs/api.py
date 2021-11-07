# -*- coding: utf-8 -*-

"""Main code."""

from class_resolver import Resolver

from .generators import (
    BarbellGenerator,
    ChainGenerator,
    CircleGenerator,
    HexagonalGrid2DGenerator,
    LineGenerator,
    LollipopGenerator,
    SquareGrid2DGenerator,
    StarGenerator,
    TadpoleGenerator,
    WheelGenerator,
)
from .util import Generator

__all__ = [
    "generator_resolver",
    # quick functions
    "line_factory",
    "circle_factory",
    "chain_factory",
    "square_grid_factory",
    "hex_grid_factory",
    "star_factory",
    "wheel_factory",
    "barbell_factory",
    "tadpole_factory",
    "lollipop_factory",
]

generator_resolver = Resolver.from_subclasses(Generator)


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
    return LineGenerator(num_entities).to_pykeen(create_inverse_triples=create_inverse_triples)


def circle_factory(num_entities: int, create_inverse_triples: bool = False):
    """Create a triples factory on a line of ``num_entities`` elements.

    :param num_entities: the number of entities in the line
    :param create_inverse_triples: Should inverse triples be created?
    :returns: A PyKEEN triples factory
    """
    return CircleGenerator(num_entities).to_pykeen(create_inverse_triples=create_inverse_triples)


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
    return SquareGrid2DGenerator(rows, columns).to_pykeen(
        create_inverse_triples=create_inverse_triples
    )


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
    return HexagonalGrid2DGenerator(rows=rows, columns=columns).to_pykeen(
        create_inverse_triples=create_inverse_triples
    )


def chain_factory(
    length: int,
    width: int = 1,
    leaves: int = 2,
    heterogeneous: bool = True,
    create_inverse_triples: bool = False,
):
    """Create a chain."""
    return ChainGenerator(
        length=length, width=width, leaves=leaves, heterogeneous=heterogeneous
    ).to_pykeen(create_inverse_triples=create_inverse_triples)


def star_factory(
    spokes: int,
    sink: bool = False,
    create_inverse_triples: bool = False,
):
    """Create a star graph of the given size."""
    return StarGenerator(
        spokes=spokes,
        sink=sink,
    ).to_pykeen(create_inverse_triples=create_inverse_triples)


def wheel_factory(
    spokes: int,
    sink: bool = False,
    create_inverse_triples: bool = False,
):
    """Create a wheel graph of the given size."""
    return WheelGenerator(
        spokes=spokes,
        sink=sink,
    ).to_pykeen(create_inverse_triples=create_inverse_triples)


def barbell_factory(
    n: int,
    create_inverse_triples: bool = False,
):
    """Create a barbell graph of the given size."""
    return BarbellGenerator(
        n=n,
    ).to_pykeen(create_inverse_triples=create_inverse_triples)


def tadpole_factory(m: int, n: int, sink: bool = False, create_inverse_triples: bool = False):
    """Create a tadpole graph."""
    return TadpoleGenerator(
        m=m,
        n=n,
        sink=sink,
    ).to_pykeen(create_inverse_triples=create_inverse_triples)


def lollipop_factory(m: int, n: int, sink: bool = False, create_inverse_triples: bool = False):
    """Create a lollipop graph."""
    return LollipopGenerator(
        m=m,
        n=n,
        sink=sink,
    ).to_pykeen(create_inverse_triples=create_inverse_triples)
