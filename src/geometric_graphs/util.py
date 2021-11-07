# -*- coding: utf-8 -*-

"""Utilities for geometric graphs."""

import os
import pathlib
from typing import Iterable, Iterator, Optional, Union, cast

__all__ = [
    "Generator",
    "from_tuples",
]


class Generator:
    """A base generator for triples for a geometric graph."""

    def get_triples(self) -> list[tuple[int, int, int]]:
        """List triples for the graph."""
        return list(self.iterate_triples())

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the graph."""
        raise NotImplementedError

    def number_of_nodes(self) -> Optional[int]:
        """Calculate the number of nodes based on the parameters of the generator."""
        # FIXME make not optional later

    def number_of_edges(self) -> Optional[int]:
        """Calculate the number of edges based on the parameters of the generator."""
        # FIXME make not optional later

    def __iter__(self) -> Iterator[tuple[int, int, int]]:
        """Yield triples for the graph."""
        yield from self.iterate_triples()

    @classmethod
    def demo(
        cls,
        *args,
        path: Union[str, pathlib.Path, os.PathLike],
        name: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Demo this generator with the given arguments (e.g., by drawing to the path)."""
        inst = cls(*args, **kwargs)  # type:ignore
        inst.draw(path=path, name=name)

    def draw(self, path: Union[str, pathlib.Path, os.PathLike], name: Optional[str] = None) -> None:
        """Draw the graph using GraphViz to the given file."""
        draw(self, path=path, name=name)

    def to_pykeen(self, *, create_inverse_triples: bool = False):
        """Generate a :mod:`pykeen` triples factory for the graph.

        :param create_inverse_triples: Should inverse triples be created?
        :rtype: pykeen.triples.CoreTriplesFactory
        :returns: A PyKEEN triples factory
        """
        return from_tuples(
            self,
            create_inverse_triples=create_inverse_triples,
        )


def from_tuples(triples: Iterable[tuple[int, int, int]], create_inverse_triples: bool = False):
    """Create a PyKEEN triples factory from tuples.

    :param triples: An iterable of integer triples
    :param create_inverse_triples: Should inverse triples be created?
    :rtype: pykeen.triples.CoreTriplesFactory
    :returns: A PyKEEN triples factory
    """
    import torch
    from pykeen.triples import CoreTriplesFactory

    mapped_triples = cast(torch.LongTensor, torch.as_tensor(list(triples), dtype=torch.long))
    return CoreTriplesFactory.create(mapped_triples, create_inverse_triples=create_inverse_triples)


COLORS = ["red", "blue", "green", "purple"]


def draw(
    triples: Iterable[tuple[int, int, int]], path, name: Optional[str] = None, prog: str = "dot"
) -> None:
    """Draw a graph using GraphViz."""
    import pygraphviz as pgv

    triples = list(triples)
    relations = sorted(set(r for _, r, _ in triples))
    relation_colors = dict(zip(relations, COLORS))

    graph = pgv.AGraph(name=name or "", directed=True)
    for h, r, t in triples:
        graph.add_edge(h, t, color=relation_colors[r])

    graph.draw(path, prog=prog)
