# -*- coding: utf-8 -*-

"""Command line interface for :mod:`geometric_graphs`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m geometric_graphs`` python will execute``__main__.py`` as a script.
  That means there won't be any ``geometric_graphs.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``geometric_graphs.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import logging

import click

from .benchmark import benchmark

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main():
    """CLI for geometric_graphs."""


main.add_command(benchmark)

if __name__ == "__main__":
    main()
