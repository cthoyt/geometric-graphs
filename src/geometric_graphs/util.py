# -*- coding: utf-8 -*-

"""Utilities for geometric graphs."""

from typing import Iterable, Tuple, cast

__all__ = [
    "Factory",
    "from_tuples",
]


class Factory:
    """A base factory for generating triples for a geometric graph."""

    def iterate_triples(self) -> Iterable[tuple[int, int, int]]:
        """Yield triples for the graph."""
        raise NotImplementedError

    def to_pykeen(self, *, create_inverse_triples: bool = False):
        """Generate a :mod:`pykeen` triples factory for the graph.."""
        return from_tuples(
            self.iterate_triples(),
            create_inverse_triples=create_inverse_triples,
        )


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
