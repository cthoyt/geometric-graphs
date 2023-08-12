# -*- coding: utf-8 -*-

"""Benchmark CLI."""

import json
from hashlib import md5
from typing import Any, Mapping, Optional

import click
import matplotlib.pyplot as plt
import pandas as pd
import pystow
import seaborn as sns
from pykeen.losses import loss_resolver
from pykeen.models import model_resolver
from pykeen.pipeline import pipeline
from tqdm import tqdm, trange
from tqdm.contrib.logging import tqdm_logging_redirect

from .api import generator_resolver
from .util import Generator

__all__ = [
    "benchmark",
]

DEFAULT_METRIC = "adjusted_arithmetic_mean_rank_index"
DEFAULT_TRIALS = 13
MODULE = pystow.module("pykeen", "geobenchmark")
DEFAULT_EXPERIMENTS: list[dict[str, Any]] = [
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 5, "columns": 5},
        "inverse": False,
    },
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 30, "columns": 30},
        "inverse": True,
    },
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 30, "columns": 30},
        "inverse": False,
    },
]

models: list[tuple[str, dict[str, Any], str]] = [
    (
        "TransE",
        dict(
            scoring_fct_norm=1,
            embedding_dim=2,
            entity_constrainer=None,
            relation_constrainer="normalize",
        ),
        "SoftPlus",
    ),
    (
        "TransD",
        dict(
            embedding_dim=2,
        ),
        "SoftPlus",
    ),
    (
        "PairRE",
        dict(
            embedding_dim=2,
        ),
        "SoftPlus",
    ),
    (
        "FixedModel",
        dict(
            embedding_dim=2,
        ),
        "SoftPlus",
    ),
]


def get_digest(experiment, length: int = 8) -> str:
    """Get a hexdigest for a dictionary of a given length."""
    return md5(json.dumps(experiment, sort_keys=True).encode()).hexdigest()[:length]  # noqa:S303


def run(
    experiment: dict[str, Any],
    *,
    trials: int = DEFAULT_TRIALS,
    device: str = "mps",
    force: bool = False,
    model: str = "PairRE",
    model_kwargs: Optional[dict[str, Any]] = None,
    loss: str = "SoftPlus",
    metric: str = DEFAULT_METRIC,
):
    """Run a single benchmark experiment."""
    digest = get_digest(experiment)
    model = model_resolver.normalize(model)
    loss = loss_resolver.normalize(loss)
    submodule = MODULE.module("experiments", digest, model, loss)

    generator = generator_resolver.make_from_kwargs(experiment, "generator")
    factory = generator.to_pykeen(create_inverse_triples=experiment["inverse"])
    rv: list[tuple[str, Generator, Mapping[str, Any]]] = []
    for trial in trange(trials, desc="Trials"):
        trial_directory = submodule.join("trials", f"{trial:03}")
        results_path = trial_directory.joinpath("results.json")
        if results_path.is_file() and not force:
            rv.append((digest, generator, json.loads(results_path.read_text())))
            continue
        train, test, valid = factory.split([0.90, 0.05, 0.05], random_state=trial)
        res = pipeline(
            training=train,
            testing=test,
            validation=valid,
            model=model,
            model_kwargs=model_kwargs,
            loss=loss,
            stopper="early",
            stopper_kwargs=dict(metric=metric),
            epochs=200,
            random_seed=trial,
            device=device,
            training_loop_kwargs=dict(automatic_memory_optimization=False),
            training_kwargs=dict(batch_size=2048, checkpoint_name=None),
            evaluator_kwargs=dict(automatic_memory_optimization=False, batch_size=2048),
            evaluation_kwargs=dict(batch_size=2048),
        )
        res.save_to_directory(
            trial_directory,
            save_metadata=False,
        )
        rv.append((digest, generator, res._get_results()))
    return rv


def run_many(experiments, trials: int, device, force: bool, metric: str):
    """Run a group of benchmark experiments."""
    rows = []
    experiment_it = tqdm(experiments, desc="Experiments")
    for experiment in experiment_it:
        experiment_it.set_postfix(type=experiment["generator"])
        model_it = tqdm(models, desc="Models")
        for model, model_kwargs, loss in model_it:
            model_it.set_postfix(model=model, loss=loss)
            results = run(
                experiment=experiment,
                model=model,
                model_kwargs=model_kwargs,
                loss=loss,
                trials=trials,
                device=device,
                force=force,
                metric=metric,
            )
            for digest, generator, result in results:
                rows.append(
                    (
                        digest,
                        repr(generator),
                        model_resolver.normalize(model),
                        loss_resolver.normalize(loss),
                        round(result["metrics"]["both"]["realistic"][metric], 3),
                    )
                )

    results_path = MODULE.join(name="results.tsv")
    df = pd.DataFrame(rows, columns=["digest", "generator", "model", "loss", metric])
    df.to_csv(results_path, sep="\t", index=False)
    click.echo(f"Wrote collated results to {results_path}")

    chart_path = MODULE.join(name="chart.png")
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axhline(0.0, alpha=0.3, color="grey", linestyle="--")
    sns.boxplot(data=df, x="digest", hue="model", y=metric, ax=ax)
    ax.set_ylim([-1.0, 1.0])

    fig.savefig(chart_path, dpi=400)
    click.echo(f"Wrote chart to {chart_path}")

    return rows


@click.command()
@click.option("--trials", type=int, default=DEFAULT_TRIALS, show_default=True)
@click.option("--device", default="mps", show_default=True)
@click.option("--metric", default=DEFAULT_METRIC, show_default=True)
@click.option("-f", "--force", is_flag=True)
def benchmark(trials: int, device: str, force: bool, metric: str):
    """Run PyKEEN benchmark."""
    with tqdm_logging_redirect():
        run_many(DEFAULT_EXPERIMENTS, trials=trials, device=device, force=force, metric=metric)


if __name__ == "__main__":
    benchmark()
